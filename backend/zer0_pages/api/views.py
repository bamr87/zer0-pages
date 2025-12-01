"""
API views for health checks and system status.
"""
import logging
from datetime import datetime, timezone

from django.conf import settings
from django.db import connection
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class HealthCheckView(APIView):
    """
    Health check endpoint for deployment verification.
    Returns 200 OK if the system is healthy.
    """
    
    permission_classes = [AllowAny]
    
    def get(self, request):
        """Return health status."""
        health_status = {
            "status": "healthy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "version": "1.0.0",
        }
        
        # Check database connection
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            health_status["database"] = "connected"
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            health_status["database"] = "disconnected"
            health_status["status"] = "degraded"
        
        return Response(health_status, status=status.HTTP_200_OK)


class SystemStatusView(APIView):
    """
    System status endpoint providing detailed information about the system.
    """
    
    permission_classes = [AllowAny]
    
    def get(self, request):
        """Return detailed system status."""
        system_status = {
            "name": "zer0-pages",
            "version": "1.0.0",
            "environment": "development" if settings.DEBUG else "production",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "components": {
                "django": {
                    "status": "operational",
                    "version": "4.2+",
                },
                "api": {
                    "status": "operational",
                    "endpoints": [
                        "/api/health/",
                        "/api/status/",
                        "/api/ai/",
                        "/api/github/",
                        "/api/cms/",
                        "/api/analytics/",
                    ],
                },
                "ai_providers": {
                    "openai": bool(settings.AI_PROVIDERS.get("openai", {}).get("api_key")),
                    "anthropic": bool(settings.AI_PROVIDERS.get("anthropic", {}).get("api_key")),
                    "xai": bool(settings.AI_PROVIDERS.get("xai", {}).get("api_key")),
                },
                "github": bool(settings.GITHUB_TOKEN),
                "analytics": settings.PRIVACY_ANALYTICS_ENABLED,
            },
        }
        
        return Response(system_status, status=status.HTTP_200_OK)
