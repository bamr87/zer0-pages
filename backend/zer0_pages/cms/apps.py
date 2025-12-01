"""
CMS app configuration.
"""
from django.apps import AppConfig


class CmsConfig(AppConfig):
    """Configuration for the CMS application."""
    
    default_auto_field = "django.db.models.BigAutoField"
    name = "zer0_pages.cms"
    verbose_name = "zer0-pages CMS"
