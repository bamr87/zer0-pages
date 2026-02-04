"""
Mock implementations for AI providers for testing.
"""
from unittest.mock import Mock, MagicMock
import responses


class MockOpenAIProvider:
    """Mock OpenAI provider"""
    
    def __init__(self):
        self.client = Mock()
        self.generate_calls = []
    
    def generate(self, model, prompt, **kwargs):
        """Mock generate method"""
        self.generate_calls.append({
            'model': model,
            'prompt': prompt,
            'kwargs': kwargs
        })
        return f"Mock OpenAI response for: {prompt[:50]}..."


class MockAnthropicProvider:
    """Mock Anthropic provider"""
    
    def __init__(self):
        self.client = Mock()
        self.generate_calls = []
    
    def generate(self, model, prompt, **kwargs):
        """Mock generate method"""
        self.generate_calls.append({
            'model': model,
            'prompt': prompt,
            'kwargs': kwargs
        })
        return f"Mock Anthropic response for: {prompt[:50]}..."


class MockXAIProvider:
    """Mock xAI provider"""
    
    def __init__(self):
        self.api_key = "mock-xai-key"
        self.generate_calls = []
    
    def generate(self, model, prompt, **kwargs):
        """Mock generate method"""
        self.generate_calls.append({
            'model': model,
            'prompt': prompt,
            'kwargs': kwargs
        })
        return f"Mock xAI response for: {prompt[:50]}..."


def mock_openai_response(response_text="Generated content", status=200):
    """Mock OpenAI API response"""
    responses.add(
        responses.POST,
        "https://api.openai.com/v1/chat/completions",
        json={
            "choices": [{
                "message": {
                    "content": response_text
                }
            }]
        },
        status=status
    )


def mock_anthropic_response(response_text="Generated content", status=200):
    """Mock Anthropic API response"""
    responses.add(
        responses.POST,
        "https://api.anthropic.com/v1/messages",
        json={
            "content": [{
                "text": response_text
            }]
        },
        status=status
    )


def mock_ai_rate_limit_error():
    """Mock AI API rate limit error"""
    responses.add(
        responses.POST,
        "https://api.openai.com/v1/chat/completions",
        json={"error": {"message": "Rate limit exceeded"}},
        status=429
    )


def mock_ai_api_error():
    """Mock AI API error"""
    responses.add(
        responses.POST,
        "https://api.openai.com/v1/chat/completions",
        json={"error": {"message": "API error"}},
        status=500
    )



