"""
pytest configuration for zer0-pages tests.
"""
import os

import django
import pytest

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zer0_pages.settings")


def pytest_configure():
    """Configure Django for tests."""
    from django.conf import settings
    
    # Use SQLite for testing
    settings.DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
    
    # Disable caching for tests
    settings.CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        }
    }
    
    # Disable analytics in tests
    settings.PRIVACY_ANALYTICS_ENABLED = False
    
    django.setup()


@pytest.fixture(scope="session")
def django_db_setup():
    """Set up the test database."""
    pass


@pytest.fixture
def api_client():
    """Create an API client for testing."""
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def user(db):
    """Create a test user."""
    from django.contrib.auth.models import User
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpass123",
    )


@pytest.fixture
def admin_user(db):
    """Create a test admin user."""
    from django.contrib.auth.models import User
    return User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="adminpass123",
    )


@pytest.fixture
def authenticated_client(api_client, user):
    """Create an authenticated API client."""
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def admin_client(api_client, admin_user):
    """Create an admin authenticated API client."""
    api_client.force_authenticate(user=admin_user)
    return api_client
