import abc
import hashlib
import json
import logging
import time
from typing import Dict, Any, Optional, List
from django.conf import settings
from .models import AIProvider, AIModel, AIResponse
from tenacity import retry, stop_after_attempt, wait_exponential
import openai
import anthropic

logger = logging.getLogger(__name__)

class AIProviderInterface(abc.ABC):
    @abc.abstractmethod
    def generate(self, model: str, prompt: str, **kwargs) -> str:
        pass

class OpenAIProvider(AIProviderInterface):
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

    def generate(self, model: str, prompt: str, **kwargs) -> str:
        response = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        return response.choices[0].message.content

class AnthropicProvider(AIProviderInterface):
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    def generate(self, model: str, prompt: str, **kwargs) -> str:
        response = self.client.messages.create(
            model=model,
            max_tokens=kwargs.get('max_tokens', 4096),
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

class XAIProvider(AIProviderInterface):
    def __init__(self):
        # Assuming OpenAI compatible API or similar SDK structure
        # Placeholder implementation
        self.api_key = settings.XAI_API_KEY
    
    def generate(self, model: str, prompt: str, **kwargs) -> str:
        # Placeholder
        return "xAI generation not implemented yet"

class AIService:
    PROVIDERS = {
        'openai': OpenAIProvider,
        'anthropic': AnthropicProvider,
        'xai': XAIProvider,
    }

    def __init__(self):
        self.providers = {}

    def get_provider(self, name: str) -> AIProviderInterface:
        if name not in self.providers:
            if name in self.PROVIDERS:
                self.providers[name] = self.PROVIDERS[name]()
            else:
                raise ValueError(f"Unknown provider: {name}")
        return self.providers[name]

    def _get_cache_key(self, provider_name: str, model_name: str, prompt: str) -> str:
        data = f"{provider_name}:{model_name}:{prompt}"
        return hashlib.sha256(data.encode()).hexdigest()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def generate(self, prompt: str, provider_name: str = 'openai', model_name: str = 'gpt-4o', use_cache: bool = True, **kwargs) -> str:
        cache_key = self._get_cache_key(provider_name, model_name, prompt)
        
        if use_cache:
            cached = AIResponse.objects.filter(prompt_hash=cache_key).first()
            if cached:
                return cached.response_text

        try:
            provider_instance = self.get_provider(provider_name)
            response_text = provider_instance.generate(model_name, prompt, **kwargs)
            
            # Cache result
            # Need to fetch or create provider/model DB objects
            db_provider, _ = AIProvider.objects.get_or_create(name=provider_name)
            db_model, _ = AIModel.objects.get_or_create(provider=db_provider, name=model_name)
            
            AIResponse.objects.create(
                prompt_hash=cache_key,
                provider=db_provider,
                model=db_model,
                prompt_text=prompt,
                response_text=response_text,
                # tokens_used calculation omitted for brevity
            )
            
            return response_text
        except Exception as e:
            logger.error(f"AI generation failed: {e}")
            raise

    def analyze_repo(self, repo_content: Dict[str, str]) -> str:
        # Logic to analyze repo content
        prompt = f"Analyze this repository content: {json.dumps(repo_content)[:10000]}..." # Truncate for example
        return self.generate(prompt)

