from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PRDViewSet

router = DefaultRouter()
router.register(r'prds', PRDViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

