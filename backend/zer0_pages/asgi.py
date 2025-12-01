"""
ASGI config for zer0_pages project.
"""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zer0_pages.settings")

application = get_asgi_application()
