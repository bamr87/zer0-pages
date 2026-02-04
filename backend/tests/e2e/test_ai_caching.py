"""
E2E tests for AI caching behavior.
"""
import pytest
from unittest.mock import patch
from rest_framework import status
from ai.models import AIResponse, AIProvider, AIModel


@pytest.mark.django_db
@pytest.mark.e2e
@pytest.mark.ai
class TestAICaching:
    """Test AI response caching"""
    
    @patch('ai.services.OpenAIProvider.generate')
    def test_cache_hit(self, mock_generate, authenticated_editor_client, ai_provider_setup):
        """Test that cached responses are returned"""
        prompt = "Test prompt for caching"
        cached_response = "This is a cached response"
        
        # Create cached response
        provider = AIProvider.objects.get(name='openai')
        model = AIModel.objects.get(provider=provider, name='gpt-4o')
        AIResponse.objects.create(
            prompt_hash='test_hash_123',
            provider=provider,
            model=model,
            prompt_text=prompt,
            response_text=cached_response,
            tokens_used=100
        )
        
        # Mock the hash generation to return our test hash
        with patch('ai.services.AIService._get_cache_key', return_value='test_hash_123'):
            url = '/api/ai/generate/'
            data = {
                'prompt': prompt,
                'provider': 'openai',
                'model': 'gpt-4o'
            }
            response = authenticated_editor_client.post(url, data, format='json')
            
            # Should return cached response without calling API
            assert response.status_code == status.HTTP_200_OK
            assert response.data['result'] == cached_response
            # API should not be called
            mock_generate.assert_not_called()
    
    @patch('ai.services.OpenAIProvider.generate')
    def test_cache_miss(self, mock_generate, authenticated_editor_client, ai_provider_setup):
        """Test that cache miss triggers API call"""
        mock_generate.return_value = "New API response"
        
        url = '/api/ai/generate/'
        data = {
            'prompt': 'New unique prompt',
            'provider': 'openai',
            'model': 'gpt-4o'
        }
        response = authenticated_editor_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['result'] == "New API response"
        mock_generate.assert_called_once()
        
        # Verify response was cached
        assert AIResponse.objects.filter(prompt_text='New unique prompt').exists()



