"""
Analytics serializers.
"""
from rest_framework import serializers

from zer0_pages.analytics.models import (
    AnalyticsEvent,
    ConsentRecord,
    ContentStats,
    DailyStats,
)


class ConsentRecordSerializer(serializers.ModelSerializer):
    """Serializer for consent records."""
    
    class Meta:
        model = ConsentRecord
        fields = [
            "id",
            "session_id",
            "consent_type",
            "granted",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


class ConsentUpdateSerializer(serializers.Serializer):
    """Serializer for updating consent preferences."""
    
    session_id = serializers.CharField(max_length=64)
    consents = serializers.DictField(
        child=serializers.BooleanField(),
        help_text="Dictionary of consent_type: granted pairs",
    )


class AnalyticsEventSerializer(serializers.ModelSerializer):
    """Serializer for analytics events."""
    
    class Meta:
        model = AnalyticsEvent
        fields = [
            "id",
            "session_id",
            "event_type",
            "event_name",
            "page_path",
            "referrer",
            "properties",
            "country_code",
            "device_type",
            "browser",
            "created_at",
        ]
        read_only_fields = ["created_at"]


class TrackEventSerializer(serializers.Serializer):
    """Serializer for tracking events."""
    
    session_id = serializers.CharField(max_length=64)
    event_type = serializers.ChoiceField(
        choices=[
            "page_view",
            "content_view",
            "download",
            "external_link",
            "scroll_depth",
            "search",
            "form_submit",
            "error",
            "custom",
        ]
    )
    event_name = serializers.CharField(max_length=100)
    page_path = serializers.CharField(max_length=500)
    referrer = serializers.URLField(required=False, allow_blank=True)
    properties = serializers.DictField(required=False, default=dict)


class DailyStatsSerializer(serializers.ModelSerializer):
    """Serializer for daily stats."""
    
    class Meta:
        model = DailyStats
        fields = [
            "id",
            "date",
            "page_views",
            "unique_visitors",
            "total_events",
            "avg_session_duration",
            "bounce_rate",
            "top_pages",
            "top_referrers",
            "device_breakdown",
            "country_breakdown",
        ]


class ContentStatsSerializer(serializers.ModelSerializer):
    """Serializer for content stats."""
    
    class Meta:
        model = ContentStats
        fields = [
            "id",
            "content_slug",
            "content_type",
            "total_views",
            "unique_views",
            "avg_time_on_page",
            "bounce_rate",
            "scroll_depth_avg",
            "last_viewed_at",
            "created_at",
            "updated_at",
        ]


class AnalyticsSummarySerializer(serializers.Serializer):
    """Serializer for analytics summary."""
    
    period_start = serializers.DateField()
    period_end = serializers.DateField()
    total_page_views = serializers.IntegerField()
    total_unique_visitors = serializers.IntegerField()
    avg_session_duration = serializers.FloatField()
    bounce_rate = serializers.FloatField()
    top_content = serializers.ListField(child=serializers.DictField())
    traffic_trend = serializers.ListField(child=serializers.DictField())
