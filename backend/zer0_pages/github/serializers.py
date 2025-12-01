"""
GitHub serializers.
"""
from rest_framework import serializers

from zer0_pages.github.models import Issue, Repository, WebhookEvent


class RepositorySerializer(serializers.ModelSerializer):
    """Serializer for repositories."""
    
    class Meta:
        model = Repository
        fields = [
            "id",
            "owner",
            "name",
            "full_name",
            "description",
            "default_branch",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


class IssueSerializer(serializers.ModelSerializer):
    """Serializer for issues."""
    
    repository_name = serializers.CharField(source="repository.full_name", read_only=True)
    
    class Meta:
        model = Issue
        fields = [
            "id",
            "repository",
            "repository_name",
            "github_id",
            "number",
            "title",
            "body",
            "state",
            "chore_type",
            "labels",
            "assignees",
            "html_url",
            "synced_at",
            "created_at",
        ]
        read_only_fields = ["synced_at", "created_at"]


class WebhookEventSerializer(serializers.ModelSerializer):
    """Serializer for webhook events."""
    
    class Meta:
        model = WebhookEvent
        fields = [
            "id",
            "repository",
            "event_type",
            "action",
            "payload",
            "processed",
            "error_message",
            "received_at",
            "processed_at",
        ]
        read_only_fields = ["received_at", "processed_at"]


class CreateIssueRequestSerializer(serializers.Serializer):
    """Serializer for creating GitHub issues."""
    
    repository = serializers.CharField(help_text="Full repository name (owner/repo)")
    title = serializers.CharField(max_length=500)
    body = serializers.CharField(required=False, default="")
    labels = serializers.ListField(
        child=serializers.CharField(), required=False, default=list
    )
    assignees = serializers.ListField(
        child=serializers.CharField(), required=False, default=list
    )


class ScanRepositoryRequestSerializer(serializers.Serializer):
    """Serializer for repository scan requests."""
    
    repository = serializers.CharField(help_text="Full repository name (owner/repo)")
    scan_type = serializers.ChoiceField(
        choices=["todo_scan", "code_quality", "documentation", "security_scan"],
        default="todo_scan",
    )
    create_issues = serializers.BooleanField(default=False)
