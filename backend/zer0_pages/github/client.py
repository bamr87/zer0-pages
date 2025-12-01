"""
GitHub client for API operations.
"""
import logging
import time
from typing import Any

from django.conf import settings

logger = logging.getLogger(__name__)


class GitHubClient:
    """GitHub API client with rate limiting support."""
    
    def __init__(self, token: str = None):
        self.token = token or settings.GITHUB_TOKEN
        self._client = None
    
    @property
    def client(self):
        """Lazy initialization of PyGithub client."""
        if self._client is None and self.token:
            from github import Github
            self._client = Github(self.token)
        return self._client
    
    def _handle_rate_limit(self):
        """Handle GitHub API rate limiting."""
        if not self.client:
            return
        
        rate_limit = self.client.get_rate_limit()
        core_limit = rate_limit.core
        
        if core_limit.remaining < 10:
            reset_time = core_limit.reset.timestamp()
            sleep_time = max(0, reset_time - time.time() + 1)
            logger.warning(f"GitHub rate limit low. Sleeping for {sleep_time}s")
            time.sleep(sleep_time)
    
    def get_repository(self, full_name: str):
        """Get repository by full name (owner/repo)."""
        if not self.client:
            raise ValueError("GitHub token not configured")
        
        self._handle_rate_limit()
        return self.client.get_repo(full_name)
    
    def list_repositories(self, user: str = None, org: str = None):
        """List repositories for user or organization."""
        if not self.client:
            raise ValueError("GitHub token not configured")
        
        self._handle_rate_limit()
        
        if org:
            return list(self.client.get_organization(org).get_repos())
        elif user:
            return list(self.client.get_user(user).get_repos())
        else:
            return list(self.client.get_user().get_repos())
    
    def get_file_content(self, repo_full_name: str, path: str, ref: str = None) -> str:
        """Get file content from repository."""
        if not self.client:
            raise ValueError("GitHub token not configured")
        
        self._handle_rate_limit()
        repo = self.client.get_repo(repo_full_name)
        
        try:
            content = repo.get_contents(path, ref=ref)
            return content.decoded_content.decode("utf-8")
        except Exception as e:
            logger.error(f"Failed to get file content: {e}")
            raise
    
    def create_issue(
        self,
        repo_full_name: str,
        title: str,
        body: str = "",
        labels: list = None,
        assignees: list = None,
    ):
        """Create a new issue in repository."""
        if not self.client:
            raise ValueError("GitHub token not configured")
        
        self._handle_rate_limit()
        repo = self.client.get_repo(repo_full_name)
        
        return repo.create_issue(
            title=title,
            body=body,
            labels=labels or [],
            assignees=assignees or [],
        )
    
    def list_issues(self, repo_full_name: str, state: str = "open", labels: list = None):
        """List issues in repository."""
        if not self.client:
            raise ValueError("GitHub token not configured")
        
        self._handle_rate_limit()
        repo = self.client.get_repo(repo_full_name)
        
        return list(repo.get_issues(state=state, labels=labels or []))
    
    def scan_for_todos(self, repo_full_name: str, path: str = "") -> list:
        """Scan repository for TODO comments."""
        if not self.client:
            raise ValueError("GitHub token not configured")
        
        self._handle_rate_limit()
        repo = self.client.get_repo(repo_full_name)
        
        todos = []
        
        try:
            contents = repo.get_contents(path)
            
            while contents:
                file_content = contents.pop(0)
                
                if file_content.type == "dir":
                    contents.extend(repo.get_contents(file_content.path))
                elif file_content.type == "file":
                    # Only scan code files
                    if any(
                        file_content.name.endswith(ext)
                        for ext in [".py", ".js", ".ts", ".jsx", ".tsx", ".rb", ".go", ".java"]
                    ):
                        try:
                            content = file_content.decoded_content.decode("utf-8")
                            lines = content.split("\n")
                            
                            for i, line in enumerate(lines):
                                for marker in ["TODO", "FIXME", "HACK", "XXX"]:
                                    if marker in line:
                                        todos.append({
                                            "file": file_content.path,
                                            "line": i + 1,
                                            "marker": marker,
                                            "content": line.strip(),
                                        })
                        except Exception:
                            continue
        except Exception as e:
            logger.error(f"Failed to scan for TODOs: {e}")
        
        return todos
    
    def get_prd_from_repo(self, repo_full_name: str) -> str:
        """Download PRD from repository if it exists."""
        prd_paths = ["PRD.md", "prd.md", "docs/PRD.md", "docs/prd.md"]
        
        for path in prd_paths:
            try:
                return self.get_file_content(repo_full_name, path)
            except Exception:
                continue
        
        return None
