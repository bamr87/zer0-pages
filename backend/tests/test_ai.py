"""
Tests for AI engine functionality.
"""
import pytest
from unittest.mock import MagicMock, patch

from zer0_pages.ai.engine import AIEngine, OpenAIClient


class TestAIEngine:
    """Test AI engine."""
    
    def test_engine_initialization(self):
        """Test AI engine can be initialized."""
        engine = AIEngine()
        assert engine.provider_name == "openai"
    
    def test_engine_with_custom_provider(self):
        """Test AI engine with custom provider."""
        engine = AIEngine(provider="anthropic")
        assert engine.provider_name == "anthropic"
    
    def test_get_client_raises_for_unknown_provider(self):
        """Test that get_client raises for unknown provider."""
        engine = AIEngine()
        with pytest.raises(ValueError, match="Unknown AI provider"):
            engine.get_client("unknown_provider")
    
    def test_get_client_returns_correct_type(self):
        """Test that get_client returns the correct client type."""
        engine = AIEngine()
        client = engine.get_client("openai")
        assert isinstance(client, OpenAIClient)


class TestOpenAIClient:
    """Test OpenAI client."""
    
    def test_client_initialization(self):
        """Test OpenAI client can be initialized."""
        client = OpenAIClient()
        assert client.default_model == "gpt-4o"
    
    def test_generate_without_api_key_raises(self):
        """Test that generate raises without API key."""
        client = OpenAIClient()
        client.api_key = ""  # Ensure no API key
        
        with pytest.raises(ValueError, match="OpenAI API key not configured"):
            client.generate("Test prompt")


class TestPromptTemplates:
    """Test prompt template functionality."""
    
    @pytest.mark.django_db
    def test_prompt_template_creation(self, admin_user):
        """Test creating a prompt template."""
        from zer0_pages.ai.models import PromptTemplate
        
        template = PromptTemplate.objects.create(
            name="Test Template",
            slug="test-template",
            template_type="blog_post",
            system_prompt="You are a helpful assistant.",
            user_prompt_template="Write about {topic}",
            created_by=admin_user,
        )
        
        assert template.name == "Test Template"
        assert template.is_active
        assert str(template) == "Test Template"
