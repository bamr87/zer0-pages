"""
AI data models for providers, prompts, and responses.
"""
from django.contrib.auth.models import User
from django.db import models


class AIProvider(models.Model):
    """AI provider configuration."""
    
    PROVIDER_CHOICES = [
        ("openai", "OpenAI"),
        ("anthropic", "Anthropic"),
        ("xai", "xAI"),
    ]
    
    name = models.CharField(max_length=50, choices=PROVIDER_CHOICES, unique=True)
    api_key_configured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["name"]
        verbose_name = "AI Provider"
        verbose_name_plural = "AI Providers"
    
    def __str__(self):
        return self.get_name_display()


class AIModel(models.Model):
    """AI model configuration."""
    
    provider = models.ForeignKey(
        AIProvider, on_delete=models.CASCADE, related_name="models"
    )
    name = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    cost_per_1k_input_tokens = models.DecimalField(
        max_digits=10, decimal_places=6, default=0
    )
    cost_per_1k_output_tokens = models.DecimalField(
        max_digits=10, decimal_places=6, default=0
    )
    max_tokens = models.IntegerField(default=4096)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["provider", "name"]
        unique_together = ["provider", "name"]
        verbose_name = "AI Model"
        verbose_name_plural = "AI Models"
    
    def __str__(self):
        return f"{self.provider.name}/{self.name}"


class PromptTemplate(models.Model):
    """Prompt template for AI generation."""
    
    TEMPLATE_TYPES = [
        ("blog_post", "Blog Post"),
        ("documentation", "Documentation"),
        ("prd", "PRD"),
        ("code_analysis", "Code Analysis"),
        ("enhancement", "Content Enhancement"),
        ("translation", "Translation"),
        ("custom", "Custom"),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    template_type = models.CharField(max_length=50, choices=TEMPLATE_TYPES)
    system_prompt = models.TextField()
    user_prompt_template = models.TextField()
    description = models.TextField(blank=True)
    variables = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="prompt_templates"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["template_type", "name"]
        verbose_name = "Prompt Template"
        verbose_name_plural = "Prompt Templates"
    
    def __str__(self):
        return self.name


class AIResponse(models.Model):
    """Cached AI response."""
    
    prompt_hash = models.CharField(max_length=64, db_index=True)
    model = models.ForeignKey(
        AIModel, on_delete=models.CASCADE, related_name="responses"
    )
    prompt = models.TextField()
    response = models.TextField()
    input_tokens = models.IntegerField(default=0)
    output_tokens = models.IntegerField(default=0)
    cost = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    latency_ms = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["prompt_hash", "model"]),
        ]
        verbose_name = "AI Response"
        verbose_name_plural = "AI Responses"
    
    def __str__(self):
        return f"Response from {self.model} at {self.created_at}"
