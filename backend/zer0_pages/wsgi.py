"""
WSGI config for zer0_pages project.
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zer0_pages.settings")

application = get_wsgi_application()
