"""
E2E tests for authentication flow.
"""
import pytest
from rest_framework import status
from django.urls import reverse
from users.models import User


@pytest.mark.django_db
@pytest.mark.e2e
class TestAuthFlow:
    """Test authentication end-to-end flow"""
    
    def test_user_login_success(self, api_client, admin_user):
        """Test successful user login"""
        url = reverse('token_obtain_pair')
        data = {
            'username': 'admin',
            'password': 'password'
        }
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
    
    def test_user_login_invalid_credentials(self, api_client):
        """Test login with invalid credentials"""
        url = reverse('token_obtain_pair')
        data = {
            'username': 'invalid',
            'password': 'wrong'
        }
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_token_refresh(self, api_client, admin_user):
        """Test token refresh flow"""
        # Get initial token
        login_url = reverse('token_obtain_pair')
        login_data = {'username': 'admin', 'password': 'password'}
        login_response = api_client.post(login_url, login_data, format='json')
        refresh_token = login_response.data['refresh']
        
        # Refresh token
        refresh_url = reverse('token_refresh')
        refresh_data = {'refresh': refresh_token}
        response = api_client.post(refresh_url, refresh_data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
    
    def test_authenticated_request(self, authenticated_admin_client):
        """Test accessing protected endpoint with valid token"""
        url = '/api/content/posts/'
        response = authenticated_admin_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
    
    def test_unauthenticated_request(self, api_client):
        """Test accessing protected endpoint without token"""
        url = '/api/content/posts/'
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_token_expiration_handling(self, authenticated_admin_client):
        """Test handling of expired tokens"""
        # This would require mocking token expiration
        # For now, we test that invalid token is rejected
        authenticated_admin_client.logout()
        authenticated_admin_client.credentials(
            HTTP_AUTHORIZATION='Bearer invalid_token'
        )
        
        url = '/api/content/posts/'
        response = authenticated_admin_client.get(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

