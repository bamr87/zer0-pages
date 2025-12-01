"""
GitHub URL configuration.
"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from zer0_pages.github.views import (
    CreateIssueView,
    IssueViewSet,
    RepositoryViewSet,
    WebhookEventViewSet,
    WebhookView,
)

router = DefaultRouter()
router.register(r"repositories", RepositoryViewSet)
router.register(r"issues", IssueViewSet)
router.register(r"webhooks/events", WebhookEventViewSet)

urlpatterns = [
    # Custom endpoints
    path("issues/create/", CreateIssueView.as_view(), name="create-issue"),
    path("webhooks/receive/", WebhookView.as_view(), name="webhook-receive"),
    
    # ViewSets
    path("", include(router.urls)),
]
