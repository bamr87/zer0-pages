"""
CMS URL configuration.
"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from zer0_pages.cms.views import (
    CategoryViewSet,
    ContentViewSet,
    MediaViewSet,
    PageViewSet,
    PostViewSet,
    PRDViewSet,
    SiteSettingsViewSet,
    TagViewSet,
)

router = DefaultRouter()
router.register(r"content", ContentViewSet, basename="content")
router.register(r"posts", PostViewSet, basename="posts")
router.register(r"pages", PageViewSet, basename="pages")
router.register(r"prds", PRDViewSet, basename="prds")
router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"tags", TagViewSet, basename="tags")
router.register(r"media", MediaViewSet, basename="media")
router.register(r"settings", SiteSettingsViewSet, basename="settings")

urlpatterns = [
    path("", include(router.urls)),
]
