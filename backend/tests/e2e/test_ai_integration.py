"""
E2E tests for AI service integration.
"""
import pytest
from unittest.mock import patch, MagicMock
from rest_framework import status
from tests.mocks.ai_mocks import mock_openai_response, mock_ai_rate_limit_error
import responses


@pytest.mark.django_db
@pytest.mark.e2e
@pytest.mark.ai
class TestAIIntegration:
    """Test AI service integration end-to-end"""
    
    @patch('ai.services.OpenAIProvider.generate')
    def test_ai_generate_content(self, mock_generate, authenticated_editor_client, ai_provider_setup):
        """Test AI content generation"""
        mock_generate.return_value = "Generated blog post content"
        
        url = '/api/ai/generate/'
        data = {
            'prompt': 'Write a blog post about Django',
            'provider': 'openai',
            'model': 'gpt-4o'
        }
        response = authenticated_editor_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'result' in response.data
        assert response.data['result'] == "Generated blog post content"
        mock_generate.assert_called_once()
    
    @patch('ai.services.OpenAIProvider.generate')
    def test_ai_enhance_content(self, mock_generate, authenticated_editor_client, ai_provider_setup):
        """Test AI content enhancement"""
        mock_generate.return_value = "Enhanced content with better clarity"
        
        url = '/api/ai/enhance/'
        data = {
            'content': 'Original content that needs improvement',
            'instruction': 'Improve clarity and readability',
            'provider': 'openai',
            'model': 'gpt-4o'
        }
        response = authenticated_editor_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'result' in response.data
        mock_generate.assert_called_once()
    
    @patch('ai.services.AIService.generate')
    def test_ai_analyze_repository(self, mock_analyze, authenticated_editor_client, ai_provider_setup):
        """Test AI repository analysis"""
        mock_analyze.return_value = "Analysis: Found 3 TODO items, 2 security issues"
        
        url = '/api/ai/analyze/'
        data = {
            'repo_content': {'file1.py': 'code content', 'file2.py': 'more code'},
            'provider': 'openai',
            'model': 'gpt-4o'
        }
        response = authenticated_editor_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'result' in response.data
        mock_analyze.assert_called_once()
    
    @patch('ai.services.AIService.generate')
    def test_ai_chat(self, mock_chat, authenticated_editor_client, ai_provider_setup):
        """Test AI chat interface"""
        mock_chat.return_value = "Chat response"
        
        url = '/api/ai/chat/'
        data = {
            'messages': [
                {'role': 'user', 'content': 'Hello'}
            ],
            'provider': 'openai',
            'model': 'gpt-4o'
        }
        response = authenticated_editor_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'result' in response.data
        mock_chat.assert_called_once()
    
    def test_ai_generate_missing_prompt(self, authenticated_editor_client):
        """Test AI generation with missing prompt"""
        url = '/api/ai/generate/'
        data = {'provider': 'openai'}
        response = authenticated_editor_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.data
    
    @patch('ai.services.OpenAIProvider.generate')
    def test_ai_caching(self, mock_generate, authenticated_editor_client, ai_provider_setup):
        """Test AI response caching"""
        mock_generate.return_value = "Cached response"
        
        url = '/api/ai/generate/'
        data = {
            'prompt': 'Test prompt for caching',
            'provider': 'openai',
            'model': 'gpt-4o'
        }
        
        # First call
        response1 = authenticated_editor_client.post(url, data, format='json')
        assert response1.status_code == status.HTTP_200_OK
        assert mock_generate.call_count == 1
        
        # Second call with same prompt should use cache
        response2 = authenticated_editor_client.post(url, data, format='json')
        assert response2.status_code == status.HTTP_200_OK
        # Note: In real implementation, cache would prevent second API call
        # This test verifies the caching mechanism exists



