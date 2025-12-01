"""
CMS serializers.
"""
from rest_framework import serializers

from zer0_pages.cms.models import (
    Category,
    Content,
    ContentVersion,
    Media,
    PRD,
    SiteSettings,
    Tag,
)


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""
    
    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for categories."""
    
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description", "parent", "created_at"]


class ContentVersionSerializer(serializers.ModelSerializer):
    """Serializer for content versions."""
    
    created_by_username = serializers.CharField(
        source="created_by.username", read_only=True
    )
    
    class Meta:
        model = ContentVersion
        fields = [
            "id",
            "version_number",
            "title",
            "body",
            "change_summary",
            "created_by",
            "created_by_username",
            "created_at",
        ]
        read_only_fields = ["version_number", "created_at"]


class ContentListSerializer(serializers.ModelSerializer):
    """Serializer for content list view."""
    
    author_username = serializers.CharField(source="author.username", read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    
    class Meta:
        model = Content
        fields = [
            "id",
            "title",
            "slug",
            "content_type",
            "excerpt",
            "status",
            "author",
            "author_username",
            "categories",
            "tags",
            "published_at",
            "created_at",
            "updated_at",
        ]


class ContentDetailSerializer(serializers.ModelSerializer):
    """Serializer for content detail view."""
    
    author_username = serializers.CharField(source="author.username", read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source="categories",
        many=True,
        write_only=True,
        required=False,
    )
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        source="tags",
        many=True,
        write_only=True,
        required=False,
    )
    
    class Meta:
        model = Content
        fields = [
            "id",
            "title",
            "slug",
            "content_type",
            "body",
            "excerpt",
            "status",
            "featured_image",
            "meta_title",
            "meta_description",
            "author",
            "author_username",
            "categories",
            "tags",
            "category_ids",
            "tag_ids",
            "published_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


class PRDSerializer(serializers.ModelSerializer):
    """Serializer for PRDs."""
    
    content = ContentDetailSerializer(read_only=True)
    
    class Meta:
        model = PRD
        fields = [
            "id",
            "content",
            "product_name",
            "version",
            "status",
            "executive_summary",
            "problem_statement",
            "goals",
            "features",
            "requirements",
            "roadmap",
            "risks",
            "success_criteria",
            "source_repository",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


class MediaSerializer(serializers.ModelSerializer):
    """Serializer for media files."""
    
    uploaded_by_username = serializers.CharField(
        source="uploaded_by.username", read_only=True
    )
    
    class Meta:
        model = Media
        fields = [
            "id",
            "title",
            "file",
            "file_type",
            "alt_text",
            "caption",
            "file_size",
            "mime_type",
            "width",
            "height",
            "uploaded_by",
            "uploaded_by_username",
            "created_at",
        ]
        read_only_fields = ["file_size", "mime_type", "width", "height", "created_at"]


class SiteSettingsSerializer(serializers.ModelSerializer):
    """Serializer for site settings."""
    
    class Meta:
        model = SiteSettings
        fields = [
            "site_name",
            "site_tagline",
            "site_description",
            "site_url",
            "logo",
            "favicon",
            "github_url",
            "twitter_url",
            "linkedin_url",
            "default_meta_title",
            "default_meta_description",
            "analytics_enabled",
            "comments_enabled",
            "ai_features_enabled",
            "theme",
            "dark_mode_default",
            "updated_at",
        ]
        read_only_fields = ["updated_at"]
