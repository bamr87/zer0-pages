"""
Test settings for zer0-pages.
Uses SQLite for fast testing without external dependencies.
"""
from zer0_pages.settings import *  # noqa: F401, F403

# Use SQLite for testing
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Disable caching for tests
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

# Disable analytics in tests
PRIVACY_ANALYTICS_ENABLED = False

# Speed up password hashing for tests
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Disable debug mode
DEBUG = False

# Suppress Django's debug toolbar and other debug-only middleware
MIDDLEWARE = [m for m in MIDDLEWARE if "debug" not in m.lower()]  # noqa: F405
