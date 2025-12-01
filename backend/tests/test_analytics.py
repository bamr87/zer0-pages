"""
Tests for analytics functionality.
"""
import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestConsentAPI:
    """Test consent management API."""
    
    def test_get_consent_requires_session_id(self, api_client):
        """Test that getting consent requires session_id."""
        url = reverse("consent")
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_get_consent_with_session_id(self, api_client):
        """Test getting consent with session_id."""
        url = reverse("consent")
        response = api_client.get(url, {"session_id": "test-session"})
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["session_id"] == "test-session"
    
    def test_update_consent(self, api_client):
        """Test updating consent preferences."""
        url = reverse("consent")
        data = {
            "session_id": "test-session",
            "consents": {
                "essential": True,
                "analytics": True,
                "marketing": False,
            },
        }
        response = api_client.post(url, data, format="json")
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["consents"]["analytics"] is True
        assert response.data["consents"]["marketing"] is False


@pytest.mark.django_db
class TestTrackEventAPI:
    """Test event tracking API."""
    
    def test_track_event_without_consent(self, api_client):
        """Test that tracking without consent returns consent_required."""
        url = reverse("track-event")
        data = {
            "session_id": "test-session",
            "event_type": "page_view",
            "event_name": "Page View",
            "page_path": "/test/",
        }
        response = api_client.post(url, data, format="json")
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["status"] == "consent_required"
    
    def test_track_event_with_consent(self, api_client):
        """Test tracking event with consent."""
        # First, grant consent
        consent_url = reverse("consent")
        api_client.post(consent_url, {
            "session_id": "test-session",
            "consents": {"analytics": True},
        }, format="json")
        
        # Now track event
        url = reverse("track-event")
        data = {
            "session_id": "test-session",
            "event_type": "page_view",
            "event_name": "Page View",
            "page_path": "/test/",
        }
        response = api_client.post(url, data, format="json")
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["status"] == "tracked"


@pytest.mark.django_db
class TestAnalyticsDashboard:
    """Test analytics dashboard API."""
    
    def test_dashboard_requires_authentication(self, api_client):
        """Test that dashboard requires authentication."""
        url = reverse("analytics-dashboard")
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_dashboard_authenticated(self, authenticated_client):
        """Test dashboard with authentication."""
        url = reverse("analytics-dashboard")
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert "period" in response.data
        assert "totals" in response.data
