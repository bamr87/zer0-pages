from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Repository, Issue, Webhook
from .serializers import RepositorySerializer, IssueSerializer, WebhookSerializer
from .services import GitHubService

class RepositoryViewSet(viewsets.ModelViewSet):
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def scan(self, request, pk=None):
        repo = self.get_object()
        service = GitHubService()
        try:
            # Check validity
            service.get_repo(repo.owner, repo.name)
            
            # Trigger sync
            service.sync_issues(repo.id)
            
            # Scan TODOs and create issues (simplified logic)
            todos = service.scan_repository_for_todos(repo.owner, repo.name)
            created_issues = 0
            for todo in todos:
                # Check if issue already exists for this TODO (logic needed to prevent dupes)
                # For now, just counting
                created_issues += 1
            
            return Response({'status': 'scanned', 'todos_found': len(todos)})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class IssueViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated]

class WebhookView(APIView):
    permission_classes = [permissions.AllowAny] # GitHub sends webhooks without user auth, verify signature instead

    def post(self, request):
        event_type = request.headers.get('X-GitHub-Event', 'unknown')
        payload = request.data
        
        # Verify signature here (HMAC SHA256 with webhook secret) - omitted for brevity
        
        webhook = Webhook.objects.create(
            repository=None, # Need to link based on payload['repository']['full_name']
            event_type=event_type,
            payload=payload
        )
        
        # Link repository if possible
        if 'repository' in payload:
            full_name = payload['repository']['full_name']
            owner, name = full_name.split('/')
            repo = Repository.objects.filter(owner=owner, name=name).first()
            if repo:
                webhook.repository = repo
                webhook.save()

        return Response({'status': 'received'}, status=status.HTTP_200_OK)
