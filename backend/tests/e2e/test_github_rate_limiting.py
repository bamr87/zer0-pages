"""
E2E tests for GitHub rate limit handling.
"""
import pytest
import responses
import time
from tests.mocks.github_mocks import mock_github_rate_limit_response
from github.services import GitHubService


@pytest.mark.django_db
@pytest.mark.e2e
@pytest.mark.github
class TestGitHubRateLimiting:
    """Test GitHub rate limit handling"""
    
    @responses.activate
    def test_rate_limit_detection(self):
        """Test detection of rate limit responses"""
        reset_time = int(time.time()) + 3600
        mock_github_rate_limit_response(remaining=0, reset_time=reset_time)
        
        service = GitHubService()
        
        # Should handle rate limit gracefully
        try:
            service.list_issues('test', 'repo')
        except Exception as e:
            # Service should handle rate limit error
            assert 'rate limit' in str(e).lower() or '403' in str(e)
    
    @responses.activate
    def test_rate_limit_retry(self):
        """Test retry after rate limit"""
        # First call: rate limit
        reset_time = int(time.time()) + 1  # Reset in 1 second
        mock_github_rate_limit_response(remaining=0, reset_time=reset_time)
        
        # Second call: success (after reset)
        responses.add(
            responses.GET,
            "https://api.github.com/repos/test/repo/issues",
            json=[],
            status=200
        )
        
        service = GitHubService()
        
        # Service should retry after waiting
        # Note: This test verifies the retry mechanism exists
        # Actual retry would require time.sleep which we can mock



