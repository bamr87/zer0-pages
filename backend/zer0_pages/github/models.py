"""
GitHub integration data models.
"""
from django.contrib.auth.models import User
from django.db import models


class Repository(models.Model):
    """GitHub repository configuration."""
    
    owner = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    default_branch = models.CharField(max_length=100, default="main")
    is_active = models.BooleanField(default=True)
    webhook_secret = models.CharField(max_length=200, blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="repositories"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["full_name"]
        verbose_name = "Repository"
        verbose_name_plural = "Repositories"
    
    def __str__(self):
        return self.full_name


class Issue(models.Model):
    """GitHub issue tracking."""
    
    STATE_CHOICES = [
        ("open", "Open"),
        ("closed", "Closed"),
    ]
    
    CHORE_TYPES = [
        ("todo_scan", "TODO Scan"),
        ("code_quality", "Code Quality"),
        ("documentation", "Documentation"),
        ("dependency_update", "Dependency Update"),
        ("security_scan", "Security Scan"),
        ("test_coverage", "Test Coverage"),
        ("manual", "Manual"),
    ]
    
    repository = models.ForeignKey(
        Repository, on_delete=models.CASCADE, related_name="issues"
    )
    github_id = models.BigIntegerField(db_index=True)
    number = models.IntegerField()
    title = models.CharField(max_length=500)
    body = models.TextField(blank=True)
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default="open")
    chore_type = models.CharField(
        max_length=50, choices=CHORE_TYPES, null=True, blank=True
    )
    labels = models.JSONField(default=list)
    assignees = models.JSONField(default=list)
    html_url = models.URLField(max_length=500)
    synced_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-created_at"]
        unique_together = ["repository", "number"]
        verbose_name = "Issue"
        verbose_name_plural = "Issues"
    
    def __str__(self):
        return f"#{self.number}: {self.title}"


class WebhookEvent(models.Model):
    """GitHub webhook event log."""
    
    EVENT_TYPES = [
        ("push", "Push"),
        ("pull_request", "Pull Request"),
        ("issues", "Issues"),
        ("issue_comment", "Issue Comment"),
        ("create", "Create"),
        ("delete", "Delete"),
        ("release", "Release"),
        ("workflow_run", "Workflow Run"),
        ("other", "Other"),
    ]
    
    repository = models.ForeignKey(
        Repository, on_delete=models.CASCADE, related_name="webhook_events", null=True
    )
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    action = models.CharField(max_length=50, blank=True)
    payload = models.JSONField(default=dict)
    processed = models.BooleanField(default=False)
    error_message = models.TextField(blank=True)
    received_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ["-received_at"]
        verbose_name = "Webhook Event"
        verbose_name_plural = "Webhook Events"
    
    def __str__(self):
        return f"{self.event_type} at {self.received_at}"
