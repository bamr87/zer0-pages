"""
Analytics URL configuration.
"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from zer0_pages.analytics.views import (
    AnalyticsDashboardView,
    ConsentView,
    ContentStatsViewSet,
    DailyStatsViewSet,
    TrackEventView,
)

router = DefaultRouter()
router.register(r"daily", DailyStatsViewSet, basename="daily-stats")
router.register(r"content", ContentStatsViewSet, basename="content-stats")

urlpatterns = [
    # Public endpoints
    path("consent/", ConsentView.as_view(), name="consent"),
    path("track/", TrackEventView.as_view(), name="track-event"),
    
    # Dashboard (authenticated)
    path("dashboard/", AnalyticsDashboardView.as_view(), name="analytics-dashboard"),
    
    # ViewSets
    path("", include(router.urls)),
]
