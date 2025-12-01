"""
Privacy-first analytics data models.
"""
from django.contrib.auth.models import User
from django.db import models


class ConsentRecord(models.Model):
    """User consent tracking for GDPR/CCPA compliance."""
    
    CONSENT_TYPES = [
        ("essential", "Essential Cookies"),
        ("analytics", "Analytics"),
        ("marketing", "Marketing"),
        ("personalization", "Personalization"),
    ]
    
    session_id = models.CharField(max_length=64, db_index=True)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="consent_records"
    )
    consent_type = models.CharField(max_length=50, choices=CONSENT_TYPES)
    granted = models.BooleanField(default=False)
    ip_hash = models.CharField(max_length=64, blank=True)  # Hashed for privacy
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_at"]
        unique_together = ["session_id", "consent_type"]
        verbose_name = "Consent Record"
        verbose_name_plural = "Consent Records"
    
    def __str__(self):
        status = "granted" if self.granted else "denied"
        return f"{self.consent_type}: {status}"


class AnalyticsEvent(models.Model):
    """Privacy-compliant analytics event."""
    
    EVENT_TYPES = [
        ("page_view", "Page View"),
        ("content_view", "Content View"),
        ("download", "Download"),
        ("external_link", "External Link"),
        ("scroll_depth", "Scroll Depth"),
        ("search", "Search"),
        ("form_submit", "Form Submit"),
        ("error", "Error"),
        ("custom", "Custom"),
    ]
    
    session_id = models.CharField(max_length=64, db_index=True)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="analytics_events"
    )
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    event_name = models.CharField(max_length=100)
    page_path = models.CharField(max_length=500)
    referrer = models.URLField(blank=True)
    properties = models.JSONField(default=dict)
    
    # Anonymized tracking
    country_code = models.CharField(max_length=2, blank=True)  # No more specific than country
    device_type = models.CharField(max_length=20, blank=True)  # mobile, tablet, desktop
    browser = models.CharField(max_length=50, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["event_type", "created_at"]),
            models.Index(fields=["page_path", "created_at"]),
        ]
        verbose_name = "Analytics Event"
        verbose_name_plural = "Analytics Events"
    
    def __str__(self):
        return f"{self.event_type}: {self.event_name}"


class DailyStats(models.Model):
    """Aggregated daily statistics."""
    
    date = models.DateField(unique=True, db_index=True)
    page_views = models.IntegerField(default=0)
    unique_visitors = models.IntegerField(default=0)
    total_events = models.IntegerField(default=0)
    avg_session_duration = models.FloatField(default=0)
    bounce_rate = models.FloatField(default=0)
    top_pages = models.JSONField(default=list)
    top_referrers = models.JSONField(default=list)
    device_breakdown = models.JSONField(default=dict)
    country_breakdown = models.JSONField(default=dict)
    
    class Meta:
        ordering = ["-date"]
        verbose_name = "Daily Stats"
        verbose_name_plural = "Daily Stats"
    
    def __str__(self):
        return f"Stats for {self.date}"


class ContentStats(models.Model):
    """Content-specific statistics."""
    
    content_slug = models.CharField(max_length=500, db_index=True)
    content_type = models.CharField(max_length=50)
    total_views = models.IntegerField(default=0)
    unique_views = models.IntegerField(default=0)
    avg_time_on_page = models.FloatField(default=0)
    bounce_rate = models.FloatField(default=0)
    scroll_depth_avg = models.FloatField(default=0)
    last_viewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-total_views"]
        unique_together = ["content_slug", "content_type"]
        verbose_name = "Content Stats"
        verbose_name_plural = "Content Stats"
    
    def __str__(self):
        return f"Stats for {self.content_slug}"
