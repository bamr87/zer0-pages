"""
zer0pages URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from api.views import SiteSettingsView, MediaUploadView

schema_view = get_schema_view(
   openapi.Info(
      title="zer0-pages API",
      default_version='v1',
      description="API for zer0-pages CMS",
      terms_of_service="https://www.zer0-pages.dev/terms/",
      contact=openapi.Contact(email="contact@zer0-pages.dev"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Swagger
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # Apps
    path('api/content/', include('content.urls')),
    path('api/ai/', include('ai.urls')),
    path('api/github/', include('github.urls')),
    path('api/prd/', include('prd.urls')),
    path('api/analytics/', include('analytics.urls')),
    
    # Generic
    path('api/settings/', SiteSettingsView.as_view(), name='settings'),
    path('api/media/', MediaUploadView.as_view(), name='media'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
