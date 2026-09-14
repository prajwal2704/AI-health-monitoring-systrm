"""
LLM Provider Abstraction Layer
Supports multiple LLM providers with easy switching
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import config

class LLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    @abstractmethod
    def generate_response(self, prompt: str, system_prompt: str = None, **kwargs) -> str:
        """Generate a response from the LLM"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the provider is available and configured"""
        pass


class OpenAIProvider(LLMProvider):
    """OpenAI GPT Provider with REST and LangChain support"""
    
    def __init__(self):
        self.api_key = config.Config.OPENAI_API_KEY
        self.model = config.Config.OPENAI_MODEL or "gpt-4o-mini"
    
    def is_available(self) -> bool:
        return bool(self.api_key and "your_" not in self.api_key and len(self.api_key) > 10)
    
    def generate_response(self, prompt: str, system_prompt: str = None, **kwargs) -> str:
        if not self.is_available():
            raise ValueError("OpenAI provider is not configured with a valid API key.")
        
        import requests
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7
        }
        res = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=35)
        if res.status_code == 200:
            return res.json()["choices"][0]["message"]["content"]
        raise Exception(f"OpenAI API Error ({res.status_code}): {res.text}")


class GeminiProvider(LLMProvider):
    """Google Gemini Provider with direct REST API support"""
    
    def __init__(self):
        self.api_key = config.Config.GEMINI_API_KEY
        raw_model = config.Config.GEMINI_MODEL or "gemini-1.5-flash"
        # Auto-upgrade deprecated gemini-pro to modern fast model
        if "gemini-pro" in raw_model:
            self.model = "gemini-1.5-flash"
        else:
            self.model = raw_model
    
    def is_available(self) -> bool:
        return bool(self.api_key and "your_" not in self.api_key and len(self.api_key) > 10)
    
    def generate_response(self, prompt: str, system_prompt: str = None, **kwargs) -> str:
        if not self.is_available():
            raise ValueError("Gemini provider is not configured with a valid API key.")
        
        import requests
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        
        full_text = f"SYSTEM DIRECTIVE:\n{system_prompt}\n\nUSER QUERY:\n{prompt}" if system_prompt else prompt
        payload = {
            "contents": [{"parts": [{"text": full_text}]}],
            "generationConfig": {"temperature": 0.7}
        }
        res = requests.post(url, json=payload, timeout=35)
        if res.status_code == 200:
            data = res.json()
            candidates = data.get("candidates", [])
            if candidates and "content" in candidates[0]:
                return candidates[0]["content"]["parts"][0]["text"]
            raise Exception("No response candidate returned by Gemini.")
        raise Exception(f"Gemini API Error ({res.status_code}): {res.text}")


class AnthropicProvider(LLMProvider):
    """Anthropic Claude Provider"""
    def __init__(self):
        self.api_key = config.Config.ANTHROPIC_API_KEY
        self.model = config.Config.ANTHROPIC_MODEL or "claude-3-haiku-20240307"

    def is_available(self) -> bool:
        return bool(self.api_key and "your_" not in self.api_key and len(self.api_key) > 10)

    def generate_response(self, prompt: str, system_prompt: str = None, **kwargs) -> str:
        if not self.is_available():
            raise ValueError("Anthropic provider is not configured with a valid API key.")
        import requests
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        payload = {
            "model": self.model,
            "max_tokens": 1024,
            "system": system_prompt or "",
            "messages": [{"role": "user", "content": prompt}]
        }
        res = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=payload, timeout=35)
        if res.status_code == 200:
            return res.json()["content"][0]["text"]
        raise Exception(f"Anthropic API Error ({res.status_code}): {res.text}")


class LLMProviderFactory:
    """Factory class to create and manage LLM providers"""
    
    _providers = {
        'openai': OpenAIProvider,
        'gemini': GeminiProvider,
        'anthropic': AnthropicProvider
    }
    
    _instance = None
    
    @classmethod
    def get_provider(cls, provider_name: str = None) -> Optional[LLMProvider]:
        """Get an LLM provider instance, or None if unconfigured"""
        if cls._instance is None:
            provider_name = provider_name or config.Config.LLM_PROVIDER
            
            if provider_name not in cls._providers:
                return None
            
            provider_class = cls._providers[provider_name]
            instance = provider_class()
            
            if instance.is_available():
                cls._instance = instance
            else:
                return None
        
        return cls._instance
    
    @classmethod
    def switch_provider(cls, provider_name: str) -> Optional[LLMProvider]:
        """Switch to a different provider"""
        cls._instance = None
        return cls.get_provider(provider_name)
    
    @classmethod
    def list_available_providers(cls) -> List[str]:
        """List all available and configured providers"""
        available = []
        for name, provider_class in cls._providers.items():
            try:
                provider = provider_class()
                if provider.is_available():
                    available.append(name)
            except Exception:
                pass
        return available

