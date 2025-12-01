"""
CMS API views.
"""
import logging
import mimetypes
import os

from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from zer0_pages.cms.models import (
    Category,
    Content,
    ContentVersion,
    Media,
    PRD,
    SiteSettings,
    Tag,
)
from zer0_pages.cms.serializers import (
    CategorySerializer,
    ContentDetailSerializer,
    ContentListSerializer,
    ContentVersionSerializer,
    MediaSerializer,
    PRDSerializer,
    SiteSettingsSerializer,
    TagSerializer,
)

logger = logging.getLogger(__name__)


class ContentPagination(PageNumberPagination):
    """Pagination for content lists."""
    
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class ContentViewSet(viewsets.ModelViewSet):
    """ViewSet for content management."""
    
    queryset = Content.objects.all().order_by("-created_at")
    permission_classes = [IsAuthenticated]
    pagination_class = ContentPagination
    lookup_field = "slug"
    
    def get_serializer_class(self):
        if self.action == "list":
            return ContentListSerializer
        return ContentDetailSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by content type
        content_type = self.request.query_params.get("type")
        if content_type:
            queryset = queryset.filter(content_type=content_type)
        
        # Filter by status
        status_filter = self.request.query_params.get("status")
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by author
        author = self.request.query_params.get("author")
        if author:
            queryset = queryset.filter(author__username=author)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=["post"])
    def publish(self, request, slug=None):
        """Publish content."""
        content = self.get_object()
        content.status = "published"
        content.published_at = timezone.now()
        content.save()
        
        serializer = self.get_serializer(content)
        return Response(serializer.data)
    
    @action(detail=True, methods=["post"])
    def unpublish(self, request, slug=None):
        """Unpublish content."""
        content = self.get_object()
        content.status = "draft"
        content.save()
        
        serializer = self.get_serializer(content)
        return Response(serializer.data)
    
    @action(detail=True, methods=["get"])
    def versions(self, request, slug=None):
        """Get content versions."""
        content = self.get_object()
        versions = content.versions.all()
        serializer = ContentVersionSerializer(versions, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=["post"])
    def create_version(self, request, slug=None):
        """Create a new version of the content."""
        content = self.get_object()
        
        # Get the latest version number
        latest_version = content.versions.order_by("-version_number").first()
        version_number = (latest_version.version_number + 1) if latest_version else 1
        
        # Create version
        version = ContentVersion.objects.create(
            content=content,
            version_number=version_number,
            title=content.title,
            body=content.body,
            change_summary=request.data.get("change_summary", ""),
            created_by=request.user,
        )
        
        serializer = ContentVersionSerializer(version)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostViewSet(ContentViewSet):
    """ViewSet for blog posts."""
    
    queryset = Content.objects.filter(content_type="post").order_by("-created_at")
    
    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            # Allow public access to published posts
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Non-authenticated users only see published posts
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(status="published")
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user, content_type="post")


class PageViewSet(ContentViewSet):
    """ViewSet for static pages."""
    
    queryset = Content.objects.filter(content_type="page").order_by("-created_at")
    
    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(status="published")
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user, content_type="page")


class PRDViewSet(viewsets.ModelViewSet):
    """ViewSet for PRDs."""
    
    queryset = PRD.objects.all()
    serializer_class = PRDSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        status_filter = self.request.query_params.get("status")
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset
    
    @action(detail=True, methods=["post"])
    def enhance(self, request, pk=None):
        """Enhance PRD using AI."""
        prd = self.get_object()
        
        # This would integrate with the AI engine
        # For now, return the PRD as-is
        serializer = self.get_serializer(prd)
        return Response(serializer.data)
    
    @action(detail=True, methods=["get"])
    def export(self, request, pk=None):
        """Export PRD in various formats."""
        prd = self.get_object()
        format_type = request.query_params.get("format", "markdown")
        
        if format_type == "markdown":
            # Generate markdown
            markdown = f"""# {prd.product_name}

**Version**: {prd.version}
**Status**: {prd.status}

## Executive Summary

{prd.executive_summary}

## Problem Statement

{prd.problem_statement}

## Goals

{prd.goals}
"""
            return Response({"format": "markdown", "content": markdown})
        
        return Response(
            {"error": f"Format '{format_type}' not supported"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for categories."""
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"


class TagViewSet(viewsets.ModelViewSet):
    """ViewSet for tags."""
    
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"


class MediaViewSet(viewsets.ModelViewSet):
    """ViewSet for media files."""
    
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def perform_create(self, serializer):
        file = self.request.FILES.get("file")
        
        extra_data = {
            "uploaded_by": self.request.user,
        }
        
        if file:
            # Get file info
            extra_data["file_size"] = file.size
            extra_data["mime_type"] = mimetypes.guess_type(file.name)[0] or ""
            
            # Determine file type
            mime_type = extra_data["mime_type"]
            if mime_type:
                if mime_type.startswith("image/"):
                    extra_data["file_type"] = "image"
                    # Try to get image dimensions
                    try:
                        from PIL import Image
                        img = Image.open(file)
                        extra_data["width"], extra_data["height"] = img.size
                        file.seek(0)  # Reset file pointer
                    except Exception:
                        pass
                elif mime_type.startswith("video/"):
                    extra_data["file_type"] = "video"
                elif mime_type.startswith("audio/"):
                    extra_data["file_type"] = "audio"
                elif mime_type.startswith("application/"):
                    extra_data["file_type"] = "document"
        
        serializer.save(**extra_data)


class SiteSettingsViewSet(viewsets.ViewSet):
    """ViewSet for site settings."""
    
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        """Get site settings."""
        settings = SiteSettings.get_settings()
        serializer = SiteSettingsSerializer(settings)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        """Update site settings."""
        settings = SiteSettings.get_settings()
        serializer = SiteSettingsSerializer(settings, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
