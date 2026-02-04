from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from content.models import SiteSettings
from django.core.files.storage import default_storage

class SiteSettingsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        settings = SiteSettings.objects.first()
        if not settings:
            settings = SiteSettings.objects.create()
        
        data = {
            'site_name': settings.site_name,
            'site_description': settings.site_description,
            'github_repo': settings.github_repo,
            'analytics_enabled': settings.analytics_enabled,
            'ai_enabled': settings.ai_enabled,
            'enable_registration': settings.enable_registration,
        }
        return Response(data)

    def post(self, request):
        if request.user.role != 'admin':
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        settings = SiteSettings.objects.first()
        if not settings:
            settings = SiteSettings.objects.create()
            
        settings.site_name = request.data.get('site_name', settings.site_name)
        settings.site_description = request.data.get('site_description', settings.site_description)
        settings.github_repo = request.data.get('github_repo', settings.github_repo)
        settings.analytics_enabled = request.data.get('analytics_enabled', settings.analytics_enabled)
        settings.ai_enabled = request.data.get('ai_enabled', settings.ai_enabled)
        settings.enable_registration = request.data.get('enable_registration', settings.enable_registration)
        settings.save()
        
        return self.get(request)

class MediaUploadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        file_name = default_storage.save(file.name, file)
        file_url = default_storage.url(file_name)
        
        return Response({'url': file_url, 'name': file_name})

