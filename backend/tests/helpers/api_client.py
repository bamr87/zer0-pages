"""
Enhanced API client helper for E2E tests.
"""
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


class AuthenticatedAPIClient(APIClient):
    """API client with authentication helpers"""
    
    def authenticate_user(self, user):
        """Authenticate a user and set JWT token"""
        refresh = RefreshToken.for_user(user)
        self.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        return refresh
    
    def logout(self):
        """Remove authentication"""
        self.credentials()
    
    def get_token(self, user):
        """Get JWT token for a user"""
        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }



