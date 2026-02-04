from django.db import models
from django.conf import settings

class AIProvider(models.Model):
    name = models.CharField(max_length=50, unique=True)  # e.g., openai, anthropic
    is_active = models.BooleanField(default=True)
    api_base_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class AIModel(models.Model):
    provider = models.ForeignKey(AIProvider, on_delete=models.CASCADE, related_name='models')
    name = models.CharField(max_length=100)  # e.g., gpt-4o
    context_window = models.IntegerField(default=4096)
    cost_per_input_token = models.DecimalField(max_digits=10, decimal_places=8, default=0)
    cost_per_output_token = models.DecimalField(max_digits=10, decimal_places=8, default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.provider.name}/{self.name}"

class PromptTemplate(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    template = models.TextField()
    input_variables = models.JSONField(default=list)
    version = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class AIResponse(models.Model):
    """Cache for AI responses"""
    prompt_hash = models.CharField(max_length=64, db_index=True)
    provider = models.ForeignKey(AIProvider, on_delete=models.CASCADE)
    model = models.ForeignKey(AIModel, on_delete=models.CASCADE)
    prompt_text = models.TextField()
    response_text = models.TextField()
    tokens_used = models.IntegerField(default=0)
    cost = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['prompt_hash']),
        ]
