"""
GitHub API views.
"""
import hashlib
import hmac
import logging

from django.conf import settings
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from zer0_pages.github.client import GitHubClient
from zer0_pages.github.models import Issue, Repository, WebhookEvent
from zer0_pages.github.serializers import (
    CreateIssueRequestSerializer,
    IssueSerializer,
    RepositorySerializer,
    ScanRepositoryRequestSerializer,
    WebhookEventSerializer,
)

logger = logging.getLogger(__name__)


class RepositoryViewSet(viewsets.ModelViewSet):
    """ViewSet for repositories."""
    
    queryset = Repository.objects.filter(is_active=True)
    serializer_class = RepositorySerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=["post"])
    def scan(self, request, pk=None):
        """Scan repository for issues."""
        repository = self.get_object()
        serializer = ScanRepositoryRequestSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        client = GitHubClient()
        
        try:
            if data["scan_type"] == "todo_scan":
                results = client.scan_for_todos(repository.full_name)
                
                if data.get("create_issues") and results:
                    for todo in results[:10]:  # Limit to 10 issues
                        issue = client.create_issue(
                            repository.full_name,
                            title=f"[{todo['marker']}] {todo['file']}:{todo['line']}",
                            body=f"Found in `{todo['file']}` at line {todo['line']}:\n\n```\n{todo['content']}\n```",
                            labels=["tech-debt", "enhancement"],
                        )
                        
                        Issue.objects.create(
                            repository=repository,
                            github_id=issue.id,
                            number=issue.number,
                            title=issue.title,
                            body=issue.body,
                            html_url=issue.html_url,
                            chore_type="todo_scan",
                            labels=[l.name for l in issue.labels],
                        )
                
                return Response({
                    "scan_type": "todo_scan",
                    "results": results,
                    "count": len(results),
                }, status=status.HTTP_200_OK)
            
            return Response({
                "error": f"Scan type '{data['scan_type']}' not yet implemented"
            }, status=status.HTTP_501_NOT_IMPLEMENTED)
            
        except Exception as e:
            logger.error(f"Repository scan error: {e}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    
    @action(detail=True, methods=["get"])
    def prd(self, request, pk=None):
        """Get PRD from repository."""
        repository = self.get_object()
        client = GitHubClient()
        
        try:
            prd_content = client.get_prd_from_repo(repository.full_name)
            
            if prd_content:
                return Response({
                    "repository": repository.full_name,
                    "prd": prd_content,
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "error": "PRD not found in repository"
                }, status=status.HTTP_404_NOT_FOUND)
                
        except Exception as e:
            logger.error(f"PRD retrieval error: {e}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class IssueViewSet(viewsets.ModelViewSet):
    """ViewSet for issues."""
    
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        repository = self.request.query_params.get("repository")
        if repository:
            queryset = queryset.filter(repository__full_name=repository)
        
        state = self.request.query_params.get("state")
        if state:
            queryset = queryset.filter(state=state)
        
        chore_type = self.request.query_params.get("chore_type")
        if chore_type:
            queryset = queryset.filter(chore_type=chore_type)
        
        return queryset


class CreateIssueView(APIView):
    """Create a GitHub issue."""
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Create issue in GitHub."""
        serializer = CreateIssueRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        client = GitHubClient()
        
        try:
            issue = client.create_issue(
                data["repository"],
                title=data["title"],
                body=data.get("body", ""),
                labels=data.get("labels", []),
                assignees=data.get("assignees", []),
            )
            
            # Try to find the repository in our database
            try:
                repository = Repository.objects.get(full_name=data["repository"])
                
                Issue.objects.create(
                    repository=repository,
                    github_id=issue.id,
                    number=issue.number,
                    title=issue.title,
                    body=issue.body or "",
                    html_url=issue.html_url,
                    chore_type="manual",
                    labels=[l.name for l in issue.labels],
                    assignees=[a.login for a in issue.assignees],
                )
            except Repository.DoesNotExist:
                pass
            
            return Response({
                "id": issue.id,
                "number": issue.number,
                "title": issue.title,
                "html_url": issue.html_url,
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"Issue creation error: {e}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class WebhookView(APIView):
    """Handle GitHub webhooks."""
    
    permission_classes = [AllowAny]
    
    def _verify_signature(self, request):
        """Verify GitHub webhook signature."""
        signature = request.headers.get("X-Hub-Signature-256", "")
        if not signature:
            return False
        
        secret = settings.GITHUB_WEBHOOK_SECRET
        if not secret:
            return True  # Skip verification if no secret configured
        
        expected = "sha256=" + hmac.new(
            secret.encode(),
            request.body,
            hashlib.sha256,
        ).hexdigest()
        
        return hmac.compare_digest(signature, expected)
    
    def post(self, request):
        """Process GitHub webhook."""
        if not self._verify_signature(request):
            return Response(
                {"error": "Invalid signature"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        
        event_type = request.headers.get("X-GitHub-Event", "other")
        payload = request.data
        
        # Get repository if it exists
        repository = None
        repo_data = payload.get("repository", {})
        if repo_data:
            full_name = repo_data.get("full_name")
            try:
                repository = Repository.objects.get(full_name=full_name)
            except Repository.DoesNotExist:
                pass
        
        # Log the event
        event = WebhookEvent.objects.create(
            repository=repository,
            event_type=event_type,
            action=payload.get("action", ""),
            payload=payload,
        )
        
        # Process specific events
        try:
            if event_type == "issues":
                self._process_issue_event(event, payload)
            elif event_type == "push":
                self._process_push_event(event, payload)
            
            event.processed = True
            event.processed_at = timezone.now()
            event.save()
            
        except Exception as e:
            event.error_message = str(e)
            event.save()
            logger.error(f"Webhook processing error: {e}")
        
        return Response({"status": "ok"}, status=status.HTTP_200_OK)
    
    def _process_issue_event(self, event: WebhookEvent, payload: dict):
        """Process issue events."""
        action = payload.get("action")
        issue_data = payload.get("issue", {})
        
        if not event.repository:
            return
        
        issue, created = Issue.objects.update_or_create(
            repository=event.repository,
            number=issue_data.get("number"),
            defaults={
                "github_id": issue_data.get("id"),
                "title": issue_data.get("title", ""),
                "body": issue_data.get("body", "") or "",
                "state": issue_data.get("state", "open"),
                "html_url": issue_data.get("html_url", ""),
                "labels": [l.get("name") for l in issue_data.get("labels", [])],
                "assignees": [a.get("login") for a in issue_data.get("assignees", [])],
            },
        )
    
    def _process_push_event(self, event: WebhookEvent, payload: dict):
        """Process push events."""
        # Could trigger content sync, Jekyll rebuild, etc.
        pass


class WebhookEventViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for webhook events (read-only)."""
    
    queryset = WebhookEvent.objects.all()
    serializer_class = WebhookEventSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        repository = self.request.query_params.get("repository")
        if repository:
            queryset = queryset.filter(repository__full_name=repository)
        
        event_type = self.request.query_params.get("event_type")
        if event_type:
            queryset = queryset.filter(event_type=event_type)
        
        return queryset
