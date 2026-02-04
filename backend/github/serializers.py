from rest_framework import serializers
from .models import Repository, Issue, Webhook

class RepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Repository
        fields = '__all__'
        read_only_fields = ('created_at', 'last_scanned_at')

class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'synced_at', 'html_url')

class WebhookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Webhook
        fields = '__all__'

