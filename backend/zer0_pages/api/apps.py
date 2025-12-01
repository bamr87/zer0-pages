"""
API app configuration.
"""
from django.apps import AppConfig


class ApiConfig(AppConfig):
    """Configuration for the API application."""
    
    default_auto_field = "django.db.models.BigAutoField"
    name = "zer0_pages.api"
    verbose_name = "zer0-pages API"
