from django.db import models

class AnalyticsEvent(models.Model):
    event_name = models.CharField(max_length=100)
    path = models.CharField(max_length=500)
    referrer = models.CharField(max_length=500, blank=True, null=True)
    user_agent = models.CharField(max_length=500, blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)  # Hashed or anonymized in practice
    session_id = models.CharField(max_length=100, blank=True, null=True)
    properties = models.JSONField(default=dict)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['event_name', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.event_name} at {self.timestamp}"
