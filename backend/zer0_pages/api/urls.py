"""
API URL configuration.
"""
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from zer0_pages.api.views import HealthCheckView, SystemStatusView

urlpatterns = [
    # Health check
    path("health/", HealthCheckView.as_view(), name="health-check"),
    path("status/", SystemStatusView.as_view(), name="system-status"),
    
    # Authentication
    path("auth/token/", TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("auth/token/verify/", TokenVerifyView.as_view(), name="token-verify"),
]
