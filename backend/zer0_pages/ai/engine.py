"""
AI Content Engine - Multi-provider AI client.
"""
import hashlib
import logging
import time
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Any

from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)


class AIClientBase(ABC):
    """Base class for AI providers."""
    
    @abstractmethod
    def generate(self, prompt: str, system_prompt: str = None, **kwargs) -> dict:
        """Generate content from prompt."""
        pass
    
    @abstractmethod
    def chat(self, messages: list, **kwargs) -> dict:
        """Interactive chat completion."""
        pass


class OpenAIClient(AIClientBase):
    """OpenAI API client."""
    
    def __init__(self):
        self.api_key = settings.AI_PROVIDERS.get("openai", {}).get("api_key", "")
        self.default_model = settings.AI_PROVIDERS.get("openai", {}).get(
            "default_model", "gpt-4o"
        )
        self._client = None
    
    @property
    def client(self):
        """Lazy initialization of OpenAI client."""
        if self._client is None and self.api_key:
            import openai
            self._client = openai.OpenAI(api_key=self.api_key)
        return self._client
    
    def generate(
        self,
        prompt: str,
        system_prompt: str = None,
        model: str = None,
        max_tokens: int = 4096,
        **kwargs
    ) -> dict:
        """Generate content using OpenAI."""
        if not self.client:
            raise ValueError("OpenAI API key not configured")
        
        model = model or self.default_model
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        start_time = time.time()
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
            )
            
            latency_ms = int((time.time() - start_time) * 1000)
            
            return {
                "content": response.choices[0].message.content,
                "model": model,
                "provider": "openai",
                "input_tokens": response.usage.prompt_tokens,
                "output_tokens": response.usage.completion_tokens,
                "latency_ms": latency_ms,
                "finish_reason": response.choices[0].finish_reason,
            }
        except Exception as e:
            logger.error(f"OpenAI generation error: {e}")
            raise
    
    def chat(self, messages: list, model: str = None, **kwargs) -> dict:
        """Interactive chat completion."""
        if not self.client:
            raise ValueError("OpenAI API key not configured")
        
        model = model or self.default_model
        start_time = time.time()
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
            )
            
            latency_ms = int((time.time() - start_time) * 1000)
            
            return {
                "content": response.choices[0].message.content,
                "model": model,
                "provider": "openai",
                "input_tokens": response.usage.prompt_tokens,
                "output_tokens": response.usage.completion_tokens,
                "latency_ms": latency_ms,
            }
        except Exception as e:
            logger.error(f"OpenAI chat error: {e}")
            raise


class AnthropicClient(AIClientBase):
    """Anthropic API client."""
    
    def __init__(self):
        self.api_key = settings.AI_PROVIDERS.get("anthropic", {}).get("api_key", "")
        self.default_model = settings.AI_PROVIDERS.get("anthropic", {}).get(
            "default_model", "claude-3-sonnet"
        )
        self._client = None
    
    @property
    def client(self):
        """Lazy initialization of Anthropic client."""
        if self._client is None and self.api_key:
            import anthropic
            self._client = anthropic.Anthropic(api_key=self.api_key)
        return self._client
    
    def generate(
        self,
        prompt: str,
        system_prompt: str = None,
        model: str = None,
        max_tokens: int = 4096,
        **kwargs
    ) -> dict:
        """Generate content using Anthropic."""
        if not self.client:
            raise ValueError("Anthropic API key not configured")
        
        model = model or self.default_model
        start_time = time.time()
        
        try:
            response = self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                system=system_prompt or "You are a helpful assistant.",
                messages=[{"role": "user", "content": prompt}],
            )
            
            latency_ms = int((time.time() - start_time) * 1000)
            
            return {
                "content": response.content[0].text,
                "model": model,
                "provider": "anthropic",
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
                "latency_ms": latency_ms,
                "stop_reason": response.stop_reason,
            }
        except Exception as e:
            logger.error(f"Anthropic generation error: {e}")
            raise
    
    def chat(self, messages: list, model: str = None, **kwargs) -> dict:
        """Interactive chat completion."""
        if not self.client:
            raise ValueError("Anthropic API key not configured")
        
        model = model or self.default_model
        start_time = time.time()
        
        # Convert messages format for Anthropic
        anthropic_messages = []
        system = None
        for msg in messages:
            if msg["role"] == "system":
                system = msg["content"]
            else:
                anthropic_messages.append(msg)
        
        try:
            response = self.client.messages.create(
                model=model,
                max_tokens=4096,
                system=system or "You are a helpful assistant.",
                messages=anthropic_messages,
            )
            
            latency_ms = int((time.time() - start_time) * 1000)
            
            return {
                "content": response.content[0].text,
                "model": model,
                "provider": "anthropic",
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
                "latency_ms": latency_ms,
            }
        except Exception as e:
            logger.error(f"Anthropic chat error: {e}")
            raise


class AIEngine:
    """
    AI Content Engine with multi-provider support.
    Handles content generation, enhancement, and analysis.
    """
    
    PROVIDERS = {
        "openai": OpenAIClient,
        "anthropic": AnthropicClient,
    }
    
    def __init__(self, provider: str = None):
        self.provider_name = provider or settings.DEFAULT_AI_PROVIDER
        self._clients = {}
    
    def get_client(self, provider: str = None) -> AIClientBase:
        """Get or create AI client for provider."""
        provider = provider or self.provider_name
        
        if provider not in self._clients:
            if provider not in self.PROVIDERS:
                raise ValueError(f"Unknown AI provider: {provider}")
            self._clients[provider] = self.PROVIDERS[provider]()
        
        return self._clients[provider]
    
    def _get_prompt_hash(self, prompt: str, model: str) -> str:
        """Generate hash for prompt caching."""
        content = f"{prompt}:{model}"
        return hashlib.sha256(content.encode()).hexdigest()
    
    def generate(
        self,
        prompt: str,
        system_prompt: str = None,
        provider: str = None,
        model: str = None,
        **kwargs
    ) -> dict:
        """
        Generate content from prompt.
        
        Args:
            prompt: User prompt for generation
            system_prompt: Optional system prompt
            provider: AI provider to use
            model: Specific model to use
            **kwargs: Additional generation parameters
        
        Returns:
            dict with generated content and metadata
        """
        client = self.get_client(provider)
        return client.generate(prompt, system_prompt, model=model, **kwargs)
    
    def enhance(
        self,
        content: str,
        enhancement_type: str = "clarity",
        provider: str = None,
        **kwargs
    ) -> dict:
        """
        Enhance existing content.
        
        Args:
            content: Content to enhance
            enhancement_type: Type of enhancement (clarity, completeness, readability, seo, grammar)
            provider: AI provider to use
        
        Returns:
            dict with enhanced content and metadata
        """
        enhancement_prompts = {
            "clarity": "Improve the clarity of the following content while preserving its meaning:",
            "completeness": "Expand and complete the following content, adding missing details and context:",
            "readability": "Improve the readability of the following content for a general audience:",
            "seo": "Optimize the following content for SEO while maintaining natural readability:",
            "grammar": "Fix grammar, spelling, and punctuation in the following content:",
        }
        
        system_prompt = "You are an expert content editor. Provide the improved version directly without explanations."
        prompt = f"{enhancement_prompts.get(enhancement_type, enhancement_prompts['clarity'])}\n\n{content}"
        
        return self.generate(prompt, system_prompt, provider=provider, **kwargs)
    
    def analyze(
        self,
        target: str,
        analysis_type: str = "code_quality",
        provider: str = None,
        **kwargs
    ) -> dict:
        """
        Analyze repository or document.
        
        Args:
            target: Repository URL or document content
            analysis_type: Type of analysis
            provider: AI provider to use
        
        Returns:
            dict with analysis results and metadata
        """
        analysis_prompts = {
            "todo_scan": "Scan the following code/content and list all TODO, FIXME, and HACK comments with their context:",
            "code_quality": "Analyze the following code for anti-patterns, potential improvements, and best practices violations:",
            "documentation": "Analyze the following code/content and identify missing or incomplete documentation:",
            "security": "Perform a security analysis of the following code, identifying potential vulnerabilities:",
            "prd": "Generate a comprehensive Product Requirements Document (PRD) based on the following repository/content analysis:",
        }
        
        system_prompt = "You are an expert code analyst. Provide structured, actionable analysis."
        prompt = f"{analysis_prompts.get(analysis_type, analysis_prompts['code_quality'])}\n\n{target}"
        
        return self.generate(prompt, system_prompt, provider=provider, **kwargs)
    
    def chat(
        self,
        message: str,
        context: list = None,
        provider: str = None,
        **kwargs
    ) -> dict:
        """
        Interactive chat completion.
        
        Args:
            message: User message
            context: Previous conversation context
            provider: AI provider to use
        
        Returns:
            dict with response and metadata
        """
        messages = []
        
        if context:
            messages.extend(context)
        
        messages.append({"role": "user", "content": message})
        
        client = self.get_client(provider)
        return client.chat(messages, **kwargs)
