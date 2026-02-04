"""
Database helper utilities for tests.
"""
from django.core.management import call_command


def reset_database():
    """Reset test database by flushing and loading fixtures"""
    call_command('flush', verbosity=0, interactive=False)


def create_test_data():
    """Create standard test data for E2E tests"""
    from tests.factories import (
        UserFactory, SiteSettingsFactory, PostFactory, 
        PageFactory, RepositoryFactory
    )
    
    # Create site settings
    SiteSettingsFactory()
    
    # Create users
    admin = UserFactory(username='admin', role='admin')
    editor = UserFactory(username='editor', role='editor')
    viewer = UserFactory(username='viewer', role='viewer')
    
    # Create some content
    PostFactory.create_batch(5, author=editor, status='published')
    PostFactory.create_batch(3, author=editor, status='draft')
    PageFactory.create_batch(2, author=editor, status='published')
    
    return {
        'admin': admin,
        'editor': editor,
        'viewer': viewer
    }

