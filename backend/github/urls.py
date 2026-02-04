from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RepositoryViewSet, IssueViewSet, WebhookView

router = DefaultRouter()
router.register(r'repos', RepositoryViewSet)
router.register(r'issues', IssueViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('webhooks/', WebhookView.as_view(), name='github-webhook'),
]

