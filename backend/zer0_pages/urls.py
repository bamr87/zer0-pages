"""
zer0-pages URL Configuration
"""
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    
    # API endpoints
    path("api/", include("zer0_pages.api.urls")),
    path("api/ai/", include("zer0_pages.ai.urls")),
    path("api/github/", include("zer0_pages.github.urls")),
    path("api/cms/", include("zer0_pages.cms.urls")),
    path("api/analytics/", include("zer0_pages.analytics.urls")),
    
    # API Documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
