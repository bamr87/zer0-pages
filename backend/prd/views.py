from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import PRD
from .serializers import PRDSerializer
from users.permissions import IsEditor, IsViewer
from .services import PRDService

class PRDViewSet(viewsets.ModelViewSet):
    queryset = PRD.objects.all().order_by('-updated_at')
    serializer_class = PRDSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'author', 'repository']
    search_fields = ['title', 'content']
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'generate', 'enhance', 'export']:
            permission_classes = [IsEditor]
        else:
            permission_classes = [IsViewer]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['post'])
    def generate(self, request):
        repo_id = request.data.get('repository_id')
        if not repo_id:
            return Response({'error': 'repository_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        service = PRDService()
        try:
            prd = service.generate_from_repo(repo_id, request.user)
            serializer = self.get_serializer(prd)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def enhance(self, request, pk=None):
        instruction = request.data.get('instruction')
        if not instruction:
            return Response({'error': 'instruction is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        service = PRDService()
        try:
            prd = service.enhance_prd(pk, instruction)
            serializer = self.get_serializer(prd)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def export(self, request, pk=None):
        service = PRDService()
        try:
            issue = service.export_to_issue(pk)
            return Response({'status': 'exported', 'issue_url': issue.get('html_url')})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
