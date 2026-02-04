"""
E2E tests for webhook processing.
"""
import pytest
from django.utils import timezone
from github.models import Repository, Webhook
from tests.mocks.github_mocks import mock_github_webhook_payload


@pytest.mark.django_db
@pytest.mark.e2e
@pytest.mark.github
class TestWebhookProcessing:
    """Test GitHub webhook processing"""
    
    def test_webhook_creation(self, test_repository):
        """Test creating a webhook record"""
        payload = mock_github_webhook_payload('push')
        
        webhook = Webhook.objects.create(
            repository=test_repository,
            event_type='push',
            payload=payload,
            processed=False
        )
        
        assert webhook.repository == test_repository
        assert webhook.event_type == 'push'
        assert webhook.processed == False
    
    def test_webhook_processing(self, test_repository):
        """Test processing a webhook"""
        payload = mock_github_webhook_payload('issues')
        
        webhook = Webhook.objects.create(
            repository=test_repository,
            event_type='issues',
            payload=payload,
            processed=False
        )
        
        # Process webhook
        webhook.processed = True
        webhook.processed_at = timezone.now()
        webhook.save()
        
        webhook.refresh_from_db()
        assert webhook.processed == True
        assert webhook.processed_at is not None
    
    def test_push_webhook_payload(self, test_repository):
        """Test push webhook payload structure"""
        payload = mock_github_webhook_payload('push')
        
        webhook = Webhook.objects.create(
            repository=test_repository,
            event_type='push',
            payload=payload
        )
        
        assert 'ref' in webhook.payload
        assert 'commits' in webhook.payload
    
    def test_issue_webhook_payload(self, test_repository):
        """Test issue webhook payload structure"""
        payload = mock_github_webhook_payload('issues')
        
        webhook = Webhook.objects.create(
            repository=test_repository,
            event_type='issues',
            payload=payload
        )
        
        assert 'action' in webhook.payload
        assert 'issue' in webhook.payload



