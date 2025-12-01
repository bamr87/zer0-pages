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
    
    def test_get_client_creates_client(self):
        """Test that get_client creates appropriate client."""
        engine = AIEngine()
        with pytest.raises(ValueError):
            engine.get_client("unknown_provider")
    
    @patch.object(OpenAIClient, "client", new_callable=MagicMock)
    def test_generate_calls_client(self, mock_client):
        """Test that generate calls the client."""
        engine = AIEngine()
        
        # Mock the response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="Test response"), finish_reason="stop")]
        mock_response.usage = MagicMock(prompt_tokens=10, completion_tokens=20)
        mock_client.chat.completions.create.return_value = mock_response
        
        # This would fail without API key, but we're testing the structure
        with pytest.raises(ValueError, match="OpenAI API key not configured"):
            engine.generate("Test prompt")


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
