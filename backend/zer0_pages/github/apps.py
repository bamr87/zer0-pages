"""
GitHub app configuration.
"""
from django.apps import AppConfig


class GithubConfig(AppConfig):
    """Configuration for the GitHub integration application."""
    
    default_auto_field = "django.db.models.BigAutoField"
    name = "zer0_pages.github"
    verbose_name = "zer0-pages GitHub Integration"
