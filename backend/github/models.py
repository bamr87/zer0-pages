from django.db import models
from django.conf import settings

class Repository(models.Model):
    name = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)
    url = models.URLField()
    default_branch = models.CharField(max_length=100, default='main')
    is_active = models.BooleanField(default=True)
    last_scanned_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['owner', 'name']

    def __str__(self):
        return f"{self.owner}/{self.name}"

class Issue(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE, related_name='issues')
    number = models.IntegerField()
    title = models.CharField(max_length=500)
    body = models.TextField(blank=True)
    state = models.CharField(max_length=20)  # open, closed
    html_url = models.URLField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    
    # Metadata for sync
    synced_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['repository', 'number']

    def __str__(self):
        return f"#{self.number} {self.title}"

class Webhook(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE, related_name='webhooks')
    event_type = models.CharField(max_length=100)
    payload = models.JSONField()
    processed = models.BooleanField(default=False)
    received_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.event_type} for {self.repository}"
