"""
AI app configuration.
"""
from django.apps import AppConfig


class AiConfig(AppConfig):
    """Configuration for the AI application."""
    
    default_auto_field = "django.db.models.BigAutoField"
    name = "zer0_pages.ai"
    verbose_name = "zer0-pages AI Engine"
