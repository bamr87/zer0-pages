from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import AnalyticsEvent
from .services import AnalyticsService

class TrackEventView(APIView):
    permission_classes = [permissions.AllowAny] # Allow public site tracking

    def post(self, request):
        event_name = request.data.get('event')
        properties = request.data.get('properties', {})
        
        # 1. Store locally for privacy-first / backup
        # Handle anonymization if needed
        AnalyticsEvent.objects.create(
            event_name=event_name,
            path=properties.get('path', ''),
            properties=properties,
            ip_address=request.META.get('REMOTE_ADDR') # Hash this in production
        )
        
        # 2. Send to PostHog (server-side)
        service = AnalyticsService()
        user_id = request.user.id if request.user.is_authenticated else 'anonymous'
        service.track(user_id, event_name, properties)
        
        return Response({'status': 'tracked'})
