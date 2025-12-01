"""
AI API views.
"""
import logging

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from zer0_pages.ai.engine import AIEngine
from zer0_pages.ai.models import AIModel, AIProvider, PromptTemplate
from zer0_pages.ai.serializers import (
    AIAnalyzeRequestSerializer,
    AIChatRequestSerializer,
    AIEnhanceRequestSerializer,
    AIGenerateRequestSerializer,
    AIModelSerializer,
    AIProviderSerializer,
    PromptTemplateSerializer,
)

logger = logging.getLogger(__name__)


class AIGenerateView(APIView):
    """Generate content using AI."""
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Generate content from prompt."""
        serializer = AIGenerateRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        engine = AIEngine()
        
        try:
            # Get template if specified
            system_prompt = None
            prompt = data["prompt"]
            
            if data.get("template"):
                try:
                    template = PromptTemplate.objects.get(
                        slug=data["template"], is_active=True
                    )
                    system_prompt = template.system_prompt
                    # Render user prompt with variables
                    prompt = template.user_prompt_template.format(
                        **data.get("variables", {}), user_input=data["prompt"]
                    )
                except PromptTemplate.DoesNotExist:
                    pass
            
            result = engine.generate(
                prompt=prompt,
                system_prompt=system_prompt,
                provider=data.get("provider"),
                model=data.get("model"),
                max_tokens=data.get("max_tokens", 4096),
            )
            
            return Response(result, status=status.HTTP_200_OK)
            
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"AI generation error: {e}")
            return Response(
                {"error": "AI generation failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class AIEnhanceView(APIView):
    """Enhance existing content using AI."""
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Enhance content."""
        serializer = AIEnhanceRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        engine = AIEngine()
        
        try:
            result = engine.enhance(
                content=data["content"],
                enhancement_type=data.get("enhancement_type", "clarity"),
                provider=data.get("provider"),
            )
            
            return Response(result, status=status.HTTP_200_OK)
            
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"AI enhancement error: {e}")
            return Response(
                {"error": "AI enhancement failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class AIAnalyzeView(APIView):
    """Analyze repository or document using AI."""
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Analyze target."""
        serializer = AIAnalyzeRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        engine = AIEngine()
        
        try:
            result = engine.analyze(
                target=data["target"],
                analysis_type=data.get("analysis_type", "code_quality"),
                provider=data.get("provider"),
            )
            
            return Response(result, status=status.HTTP_200_OK)
            
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"AI analysis error: {e}")
            return Response(
                {"error": "AI analysis failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class AIChatView(APIView):
    """Interactive AI chat."""
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Chat with AI."""
        serializer = AIChatRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        engine = AIEngine()
        
        try:
            result = engine.chat(
                message=data["message"],
                context=data.get("context", []),
                provider=data.get("provider"),
            )
            
            return Response(result, status=status.HTTP_200_OK)
            
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"AI chat error: {e}")
            return Response(
                {"error": "AI chat failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class AIProviderViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for AI providers."""
    
    queryset = AIProvider.objects.filter(is_active=True)
    serializer_class = AIProviderSerializer
    permission_classes = [IsAuthenticated]


class AIModelViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for AI models."""
    
    queryset = AIModel.objects.filter(is_active=True)
    serializer_class = AIModelSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        provider = self.request.query_params.get("provider")
        if provider:
            queryset = queryset.filter(provider__name=provider)
        return queryset


class PromptTemplateViewSet(viewsets.ModelViewSet):
    """ViewSet for prompt templates."""
    
    queryset = PromptTemplate.objects.filter(is_active=True)
    serializer_class = PromptTemplateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
