"""
Tests for API health check endpoints.
"""
import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestHealthCheck:
    """Test health check endpoint."""
    
    def test_health_check_returns_200(self, api_client):
        """Test that health check returns 200 OK."""
        url = reverse("health-check")
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["status"] in ["healthy", "degraded"]
        assert "timestamp" in response.data
        assert "version" in response.data
    
    def test_health_check_includes_database_status(self, api_client):
        """Test that health check includes database status."""
        url = reverse("health-check")
        response = api_client.get(url)
        
        assert "database" in response.data


@pytest.mark.django_db
class TestSystemStatus:
    """Test system status endpoint."""
    
    def test_system_status_returns_200(self, api_client):
        """Test that system status returns 200 OK."""
        url = reverse("system-status")
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["name"] == "zer0-pages"
        assert "version" in response.data
        assert "components" in response.data
    
    def test_system_status_includes_components(self, api_client):
        """Test that system status includes component information."""
        url = reverse("system-status")
        response = api_client.get(url)
        
        components = response.data["components"]
        assert "django" in components
        assert "api" in components
        assert "ai_providers" in components
