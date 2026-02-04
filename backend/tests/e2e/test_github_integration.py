"""
E2E tests for GitHub integration.
"""
import pytest
from unittest.mock import patch
from rest_framework import status
import responses
from tests.mocks.github_mocks import (
    mock_github_repo_response,
    mock_github_issues_response,
    mock_github_create_issue_response,
    mock_github_search_code_response
)
from github.models import Repository, Issue


@pytest.mark.django_db
@pytest.mark.e2e
@pytest.mark.github
class TestGitHubIntegration:
    """Test GitHub integration end-to-end"""
    
    @responses.activate
    def test_connect_repository(self, authenticated_admin_client):
        """Test connecting a GitHub repository"""
        mock_github_repo_response(owner='test', name='test-repo')
        
        url = '/api/github/repos/'
        data = {
            'name': 'test-repo',
            'owner': 'test',
            'url': 'https://github.com/test/test-repo',
            'default_branch': 'main'
        }
        response = authenticated_admin_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert Repository.objects.filter(owner='test', name='test-repo').exists()
    
    @responses.activate
    def test_sync_issues(self, authenticated_admin_client, test_repository):
        """Test syncing GitHub issues"""
        mock_github_issues_response(
            owner=test_repository.owner,
            name=test_repository.name,
            issues=[
                {
                    'number': 1,
                    'title': 'Test Issue',
                    'body': 'Issue body',
                    'state': 'open',
                    'html_url': f'https://github.com/{test_repository.owner}/{test_repository.name}/issues/1',
                    'created_at': '2024-01-01T00:00:00Z',
                    'updated_at': '2024-01-01T00:00:00Z'
                }
            ]
        )
        
        # Sync issues via service
        from github.services import GitHubService
        service = GitHubService()
        service.sync_issues(test_repository.id)
        
        # Verify issue was created
        assert Issue.objects.filter(repository=test_repository, number=1).exists()
    
    @responses.activate
    def test_create_issue(self, authenticated_admin_client, test_repository):
        """Test creating a GitHub issue"""
        mock_github_create_issue_response(
            owner=test_repository.owner,
            name=test_repository.name,
            issue_number=1
        )
        
        url = '/api/github/issues/'
        data = {
            'repository': test_repository.id,
            'title': 'New Issue',
            'body': 'Issue description',
            'labels': ['bug']
        }
        response = authenticated_admin_client.post(url, data, format='json')
        
        # Should create issue (if endpoint exists) or return success
        assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_200_OK]
    
    @responses.activate
    def test_scan_repository_for_todos(self, authenticated_admin_client, test_repository):
        """Test scanning repository for TODO comments"""
        mock_github_search_code_response(
            query=f"TODO repo:{test_repository.owner}/{test_repository.name}",
            items=[
                {
                    'path': 'src/main.py',
                    'html_url': f'https://github.com/{test_repository.owner}/{test_repository.name}/blob/main/src/main.py',
                    'sha': 'abc123'
                }
            ]
        )
        
        # Test TODO scanning via service
        from github.services import GitHubService
        service = GitHubService()
        todos = service.scan_repository_for_todos(test_repository.owner, test_repository.name)
        
        assert len(todos) > 0
        assert todos[0]['path'] == 'src/main.py'



