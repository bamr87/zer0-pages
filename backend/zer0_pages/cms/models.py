"""
CMS data models for content management.
"""
from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class Content(models.Model):
    """Base content model for posts and pages."""
    
    CONTENT_TYPES = [
        ("post", "Blog Post"),
        ("page", "Static Page"),
        ("documentation", "Documentation"),
        ("prd", "PRD"),
    ]
    
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("review", "In Review"),
        ("published", "Published"),
        ("archived", "Archived"),
    ]
    
    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=500, unique=True, blank=True)
    content_type = models.CharField(max_length=50, choices=CONTENT_TYPES, default="post")
    body = models.TextField(blank=True)
    excerpt = models.TextField(blank=True, max_length=500)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    featured_image = models.ImageField(upload_to="content/", blank=True, null=True)
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="contents"
    )
    categories = models.ManyToManyField("Category", blank=True, related_name="contents")
    tags = models.ManyToManyField("Tag", blank=True, related_name="contents")
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Content"
        verbose_name_plural = "Contents"
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class ContentVersion(models.Model):
    """Version history for content."""
    
    content = models.ForeignKey(
        Content, on_delete=models.CASCADE, related_name="versions"
    )
    version_number = models.IntegerField()
    title = models.CharField(max_length=500)
    body = models.TextField(blank=True)
    change_summary = models.TextField(blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="content_versions"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-version_number"]
        unique_together = ["content", "version_number"]
        verbose_name = "Content Version"
        verbose_name_plural = "Content Versions"
    
    def __str__(self):
        return f"{self.content.title} v{self.version_number}"


class PRD(models.Model):
    """Product Requirements Document with lifecycle management."""
    
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("review", "In Review"),
        ("approved", "Approved"),
        ("implemented", "Implemented"),
        ("archived", "Archived"),
    ]
    
    content = models.OneToOneField(
        Content, on_delete=models.CASCADE, related_name="prd"
    )
    product_name = models.CharField(max_length=200)
    version = models.CharField(max_length=50, default="1.0.0")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    executive_summary = models.TextField(blank=True)
    problem_statement = models.TextField(blank=True)
    goals = models.TextField(blank=True)
    features = models.JSONField(default=list)
    requirements = models.JSONField(default=list)
    roadmap = models.JSONField(default=list)
    risks = models.JSONField(default=list)
    success_criteria = models.JSONField(default=list)
    source_repository = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "PRD"
        verbose_name_plural = "PRDs"
    
    def __str__(self):
        return f"{self.product_name} v{self.version}"


class Category(models.Model):
    """Content category."""
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True, related_name="children"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name


class Tag(models.Model):
    """Content tag."""
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    
    class Meta:
        ordering = ["name"]
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
    
    def __str__(self):
        return self.name


class Media(models.Model):
    """Media file management."""
    
    FILE_TYPES = [
        ("image", "Image"),
        ("document", "Document"),
        ("video", "Video"),
        ("audio", "Audio"),
        ("other", "Other"),
    ]
    
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to="media/%Y/%m/")
    file_type = models.CharField(max_length=20, choices=FILE_TYPES, default="other")
    alt_text = models.CharField(max_length=200, blank=True)
    caption = models.TextField(blank=True)
    file_size = models.BigIntegerField(default=0)
    mime_type = models.CharField(max_length=100, blank=True)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    uploaded_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="media_files"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Media"
        verbose_name_plural = "Media Files"
    
    def __str__(self):
        return self.title


class SiteSettings(models.Model):
    """Global site configuration."""
    
    site_name = models.CharField(max_length=200, default="zer0-pages")
    site_tagline = models.CharField(max_length=200, blank=True)
    site_description = models.TextField(blank=True)
    site_url = models.URLField(blank=True)
    logo = models.ImageField(upload_to="site/", blank=True, null=True)
    favicon = models.ImageField(upload_to="site/", blank=True, null=True)
    
    # Social links
    github_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    
    # SEO settings
    default_meta_title = models.CharField(max_length=70, blank=True)
    default_meta_description = models.CharField(max_length=160, blank=True)
    
    # Feature flags
    analytics_enabled = models.BooleanField(default=True)
    comments_enabled = models.BooleanField(default=False)
    ai_features_enabled = models.BooleanField(default=True)
    
    # Theme settings
    theme = models.CharField(max_length=50, default="default")
    dark_mode_default = models.BooleanField(default=False)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def get_settings(cls):
        """Get or create site settings."""
        settings, _ = cls.objects.get_or_create(pk=1)
        return settings
