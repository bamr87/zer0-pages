"""
AI URL configuration.
"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from zer0_pages.ai.views import (
    AIAnalyzeView,
    AIChatView,
    AIEnhanceView,
    AIGenerateView,
    AIModelViewSet,
    AIProviderViewSet,
    PromptTemplateViewSet,
)

router = DefaultRouter()
router.register(r"providers", AIProviderViewSet)
router.register(r"models", AIModelViewSet)
router.register(r"templates", PromptTemplateViewSet)

urlpatterns = [
    # AI operations
    path("generate/", AIGenerateView.as_view(), name="ai-generate"),
    path("enhance/", AIEnhanceView.as_view(), name="ai-enhance"),
    path("analyze/", AIAnalyzeView.as_view(), name="ai-analyze"),
    path("chat/", AIChatView.as_view(), name="ai-chat"),
    
    # ViewSets
    path("", include(router.urls)),
]
