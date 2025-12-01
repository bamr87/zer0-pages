"""
AI serializers.
"""
from rest_framework import serializers

from zer0_pages.ai.models import AIModel, AIProvider, AIResponse, PromptTemplate


class AIProviderSerializer(serializers.ModelSerializer):
    """Serializer for AI providers."""
    
    class Meta:
        model = AIProvider
        fields = [
            "id",
            "name",
            "api_key_configured",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


class AIModelSerializer(serializers.ModelSerializer):
    """Serializer for AI models."""
    
    provider_name = serializers.CharField(source="provider.name", read_only=True)
    
    class Meta:
        model = AIModel
        fields = [
            "id",
            "provider",
            "provider_name",
            "name",
            "display_name",
            "is_default",
            "is_active",
            "cost_per_1k_input_tokens",
            "cost_per_1k_output_tokens",
            "max_tokens",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


class PromptTemplateSerializer(serializers.ModelSerializer):
    """Serializer for prompt templates."""
    
    created_by_username = serializers.CharField(
        source="created_by.username", read_only=True
    )
    
    class Meta:
        model = PromptTemplate
        fields = [
            "id",
            "name",
            "slug",
            "template_type",
            "system_prompt",
            "user_prompt_template",
            "description",
            "variables",
            "is_active",
            "created_by",
            "created_by_username",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at", "created_by"]


class AIGenerateRequestSerializer(serializers.Serializer):
    """Serializer for AI content generation requests."""
    
    prompt = serializers.CharField(required=True)
    template = serializers.SlugField(required=False)
    provider = serializers.ChoiceField(
        choices=["openai", "anthropic", "xai"],
        required=False,
    )
    model = serializers.CharField(required=False)
    variables = serializers.DictField(required=False, default=dict)
    max_tokens = serializers.IntegerField(required=False, default=4096)


class AIEnhanceRequestSerializer(serializers.Serializer):
    """Serializer for content enhancement requests."""
    
    content = serializers.CharField(required=True)
    enhancement_type = serializers.ChoiceField(
        choices=["clarity", "completeness", "readability", "seo", "grammar"],
        default="clarity",
    )
    provider = serializers.ChoiceField(
        choices=["openai", "anthropic", "xai"],
        required=False,
    )


class AIAnalyzeRequestSerializer(serializers.Serializer):
    """Serializer for repository/document analysis requests."""
    
    target = serializers.CharField(required=True, help_text="Repository URL or document content")
    analysis_type = serializers.ChoiceField(
        choices=["todo_scan", "code_quality", "documentation", "security", "prd"],
        default="code_quality",
    )
    provider = serializers.ChoiceField(
        choices=["openai", "anthropic", "xai"],
        required=False,
    )


class AIChatRequestSerializer(serializers.Serializer):
    """Serializer for interactive AI chat requests."""
    
    message = serializers.CharField(required=True)
    context = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        default=list,
    )
    provider = serializers.ChoiceField(
        choices=["openai", "anthropic", "xai"],
        required=False,
    )


class AIResponseSerializer(serializers.ModelSerializer):
    """Serializer for AI responses."""
    
    model_name = serializers.CharField(source="model.name", read_only=True)
    
    class Meta:
        model = AIResponse
        fields = [
            "id",
            "model",
            "model_name",
            "prompt",
            "response",
            "input_tokens",
            "output_tokens",
            "cost",
            "latency_ms",
            "created_at",
        ]
        read_only_fields = ["__all__"]
