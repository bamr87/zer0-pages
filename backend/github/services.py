import requests
import time
import logging
from django.conf import settings
from .models import Repository, Issue

logger = logging.getLogger(__name__)

class GitHubService:
    BASE_URL = "https://api.github.com"

    def __init__(self, token=None):
        self.token = token or settings.GITHUB_TOKEN
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def _request(self, method, endpoint, **kwargs):
        url = f"{self.BASE_URL}/{endpoint}"
        try:
            response = requests.request(method, url, headers=self.headers, **kwargs)
            
            # Handle rate limiting
            if response.status_code == 403 and 'X-RateLimit-Remaining' in response.headers:
                remaining = int(response.headers['X-RateLimit-Remaining'])
                if remaining == 0:
                    reset_time = int(response.headers['X-RateLimit-Reset'])
                    sleep_time = reset_time - int(time.time()) + 1
                    logger.warning(f"Rate limit exceeded. Sleeping for {sleep_time} seconds.")
                    time.sleep(max(sleep_time, 0))
                    return self._request(method, endpoint, **kwargs)

            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"GitHub API request failed: {e}")
            raise

    def get_repo(self, owner, name):
        return self._request('GET', f"repos/{owner}/{name}")

    def create_issue(self, owner, name, title, body, labels=None):
        data = {
            "title": title,
            "body": body,
            "labels": labels or []
        }
        return self._request('POST', f"repos/{owner}/{name}/issues", json=data)

    def list_issues(self, owner, name, state='open'):
        return self._request('GET', f"repos/{owner}/{name}/issues", params={'state': state})

    def scan_repository_for_todos(self, owner, name):
        # Simplified scan: assumes fetching repo content recursively or searching code
        # GitHub Search API is good for finding TODOs
        query = f"TODO repo:{owner}/{name}"
        results = self._request('GET', "search/code", params={'q': query})
        
        todos = []
        for item in results.get('items', []):
            todos.append({
                'path': item['path'],
                'url': item['html_url'],
                'sha': item['sha']
            })
        return todos

    def sync_issues(self, repository_id):
        repo = Repository.objects.get(id=repository_id)
        issues_data = self.list_issues(repo.owner, repo.name)
        
        for issue_data in issues_data:
            Issue.objects.update_or_create(
                repository=repo,
                number=issue_data['number'],
                defaults={
                    'title': issue_data['title'],
                    'body': issue_data['body'] or '',
                    'state': issue_data['state'],
                    'html_url': issue_data['html_url'],
                    'created_at': issue_data['created_at'],
                    'updated_at': issue_data['updated_at']
                }
            )

