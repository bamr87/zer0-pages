"""
Mock implementations for GitHub API for testing.
"""
import responses
from datetime import datetime, timezone


def mock_github_repo_response(owner="test", name="repo"):
    """Mock GitHub repository API response"""
    responses.add(
        responses.GET,
        f"https://api.github.com/repos/{owner}/{name}",
        json={
            "id": 123456,
            "name": name,
            "full_name": f"{owner}/{name}",
            "owner": {"login": owner},
            "html_url": f"https://github.com/{owner}/{name}",
            "default_branch": "main",
            "created_at": "2020-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z"
        },
        status=200
    )


def mock_github_issues_response(owner="test", name="repo", issues=None):
    """Mock GitHub issues API response"""
    if issues is None:
        issues = [
            {
                "number": 1,
                "title": "Test Issue 1",
                "body": "Issue body",
                "state": "open",
                "html_url": f"https://github.com/{owner}/{name}/issues/1",
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
        ]
    
    responses.add(
        responses.GET,
        f"https://api.github.com/repos/{owner}/{name}/issues",
        json=issues,
        status=200
    )


def mock_github_create_issue_response(owner="test", name="repo", issue_number=1):
    """Mock GitHub create issue API response"""
    responses.add(
        responses.POST,
        f"https://api.github.com/repos/{owner}/{name}/issues",
        json={
            "number": issue_number,
            "title": "New Issue",
            "body": "Issue body",
            "state": "open",
            "html_url": f"https://github.com/{owner}/{name}/issues/{issue_number}",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        },
        status=201
    )


def mock_github_search_code_response(query="TODO", items=None):
    """Mock GitHub search code API response"""
    if items is None:
        items = [
            {
                "path": "src/main.py",
                "html_url": "https://github.com/test/repo/blob/main/src/main.py",
                "sha": "abc123"
            }
        ]
    
    responses.add(
        responses.GET,
        "https://api.github.com/search/code",
        json={"items": items},
        status=200,
        match=[responses.matchers.query_param_matcher({"q": query})]
    )


def mock_github_rate_limit_response(remaining=0, reset_time=None):
    """Mock GitHub rate limit response"""
    if reset_time is None:
        reset_time = int(datetime.now(timezone.utc).timestamp()) + 3600
    
    responses.add(
        responses.GET,
        "https://api.github.com/repos/test/repo/issues",
        json={"message": "API rate limit exceeded"},
        status=403,
        headers={
            "X-RateLimit-Remaining": str(remaining),
            "X-RateLimit-Reset": str(reset_time)
        }
    )


def mock_github_webhook_payload(event_type="push"):
    """Generate mock GitHub webhook payload"""
    payloads = {
        "push": {
            "ref": "refs/heads/main",
            "commits": [{
                "id": "abc123",
                "message": "Test commit",
                "author": {"name": "Test User"}
            }]
        },
        "issues": {
            "action": "opened",
            "issue": {
                "number": 1,
                "title": "Test Issue",
                "body": "Issue body"
            }
        },
        "pull_request": {
            "action": "opened",
            "pull_request": {
                "number": 1,
                "title": "Test PR",
                "body": "PR body"
            }
        }
    }
    return payloads.get(event_type, {})



