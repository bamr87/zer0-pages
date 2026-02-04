from django.urls import path
from .views import AIGenerateView, AIEnhanceView, AIAnalyzeView, AIChatView

urlpatterns = [
    path('generate/', AIGenerateView.as_view(), name='ai-generate'),
    path('enhance/', AIEnhanceView.as_view(), name='ai-enhance'),
    path('analyze/', AIAnalyzeView.as_view(), name='ai-analyze'),
    path('chat/', AIChatView.as_view(), name='ai-chat'),
]

