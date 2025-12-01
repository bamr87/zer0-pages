"""
Analytics app configuration.
"""
from django.apps import AppConfig


class AnalyticsConfig(AppConfig):
    """Configuration for the Analytics application."""
    
    default_auto_field = "django.db.models.BigAutoField"
    name = "zer0_pages.analytics"
    verbose_name = "zer0-pages Analytics"
