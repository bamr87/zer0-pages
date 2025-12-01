"""
Analytics API views.
"""
import hashlib
import logging
from datetime import date, timedelta

from django.conf import settings
from django.db.models import Sum
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from zer0_pages.analytics.models import (
    AnalyticsEvent,
    ConsentRecord,
    ContentStats,
    DailyStats,
)
from zer0_pages.analytics.serializers import (
    AnalyticsEventSerializer,
    ConsentRecordSerializer,
    ConsentUpdateSerializer,
    ContentStatsSerializer,
    DailyStatsSerializer,
    TrackEventSerializer,
)

logger = logging.getLogger(__name__)


class ConsentView(APIView):
    """Manage user consent preferences."""
    
    permission_classes = [AllowAny]
    
    def get(self, request):
        """Get consent status for session."""
        session_id = request.query_params.get("session_id")
        if not session_id:
            return Response(
                {"error": "session_id required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        consents = ConsentRecord.objects.filter(session_id=session_id)
        
        return Response({
            "session_id": session_id,
            "consents": {
                c.consent_type: c.granted for c in consents
            },
        })
    
    def post(self, request):
        """Update consent preferences."""
        serializer = ConsentUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        session_id = data["session_id"]
        consents = data["consents"]
        
        # Hash IP for privacy
        ip = request.META.get("REMOTE_ADDR", "")
        ip_hash = hashlib.sha256(ip.encode()).hexdigest()[:16] if ip else ""
        
        for consent_type, granted in consents.items():
            ConsentRecord.objects.update_or_create(
                session_id=session_id,
                consent_type=consent_type,
                defaults={
                    "granted": granted,
                    "ip_hash": ip_hash,
                    "user_agent": request.META.get("HTTP_USER_AGENT", "")[:500],
                    "user": request.user if request.user.is_authenticated else None,
                },
            )
        
        return Response({
            "session_id": session_id,
            "consents": consents,
            "updated_at": timezone.now().isoformat(),
        })


class TrackEventView(APIView):
    """Track analytics events (privacy-compliant)."""
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        """Track an analytics event."""
        # Check if analytics is enabled
        if not settings.PRIVACY_ANALYTICS_ENABLED:
            return Response({"status": "analytics_disabled"})
        
        # Check DNT header
        dnt = request.META.get("HTTP_DNT", "0")
        if dnt == "1":
            return Response({"status": "dnt_respected"})
        
        serializer = TrackEventSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        
        # Check if user has consented to analytics
        analytics_consent = ConsentRecord.objects.filter(
            session_id=data["session_id"],
            consent_type="analytics",
            granted=True,
        ).exists()
        
        if not analytics_consent:
            return Response({"status": "consent_required"})
        
        # Parse user agent for device info
        user_agent = request.META.get("HTTP_USER_AGENT", "")
        device_type = self._detect_device(user_agent)
        browser = self._detect_browser(user_agent)
        
        # Create event
        event = AnalyticsEvent.objects.create(
            session_id=data["session_id"],
            user=request.user if request.user.is_authenticated else None,
            event_type=data["event_type"],
            event_name=data["event_name"],
            page_path=data["page_path"],
            referrer=data.get("referrer", ""),
            properties=data.get("properties", {}),
            device_type=device_type,
            browser=browser,
        )
        
        # Update content stats
        if data["event_type"] in ["page_view", "content_view"]:
            self._update_content_stats(data["page_path"], data["session_id"])
        
        return Response({
            "status": "tracked",
            "event_id": event.id,
        })
    
    def _detect_device(self, user_agent: str) -> str:
        """Detect device type from user agent."""
        ua_lower = user_agent.lower()
        if "mobile" in ua_lower or "android" in ua_lower:
            return "mobile"
        elif "tablet" in ua_lower or "ipad" in ua_lower:
            return "tablet"
        return "desktop"
    
    def _detect_browser(self, user_agent: str) -> str:
        """Detect browser from user agent."""
        ua_lower = user_agent.lower()
        if "chrome" in ua_lower and "edg" not in ua_lower:
            return "Chrome"
        elif "firefox" in ua_lower:
            return "Firefox"
        elif "safari" in ua_lower and "chrome" not in ua_lower:
            return "Safari"
        elif "edg" in ua_lower:
            return "Edge"
        return "Other"
    
    def _update_content_stats(self, page_path: str, session_id: str):
        """Update content statistics."""
        # Determine content type from path
        content_type = "page"
        if "/posts/" in page_path or "/blog/" in page_path:
            content_type = "post"
        elif "/docs/" in page_path:
            content_type = "documentation"
        
        stats, created = ContentStats.objects.get_or_create(
            content_slug=page_path,
            content_type=content_type,
        )
        
        stats.total_views += 1
        stats.last_viewed_at = timezone.now()
        stats.save()


class AnalyticsDashboardView(APIView):
    """Analytics dashboard data."""
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get analytics summary."""
        # Get date range
        end_date = date.today()
        days = int(request.query_params.get("days", 30))
        start_date = end_date - timedelta(days=days)
        
        # Get daily stats
        daily_stats = DailyStats.objects.filter(
            date__gte=start_date,
            date__lte=end_date,
        ).order_by("date")
        
        # Calculate totals
        totals = daily_stats.aggregate(
            total_views=Sum("page_views"),
            total_visitors=Sum("unique_visitors"),
            total_events=Sum("total_events"),
        )
        
        # Get top content
        top_content = ContentStats.objects.order_by("-total_views")[:10]
        
        return Response({
            "period": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat(),
                "days": days,
            },
            "totals": {
                "page_views": totals["total_views"] or 0,
                "unique_visitors": totals["total_visitors"] or 0,
                "total_events": totals["total_events"] or 0,
            },
            "daily_stats": DailyStatsSerializer(daily_stats, many=True).data,
            "top_content": ContentStatsSerializer(top_content, many=True).data,
        })


class DailyStatsViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for daily stats."""
    
    queryset = DailyStats.objects.all()
    serializer_class = DailyStatsSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")
        
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        return queryset


class ContentStatsViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for content stats."""
    
    queryset = ContentStats.objects.all()
    serializer_class = ContentStatsSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        content_type = self.request.query_params.get("content_type")
        if content_type:
            queryset = queryset.filter(content_type=content_type)
        
        return queryset
