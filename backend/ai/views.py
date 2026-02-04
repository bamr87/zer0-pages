from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .services import AIService

class AIGenerateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        prompt = request.data.get('prompt')
        provider = request.data.get('provider', 'openai')
        model = request.data.get('model', 'gpt-4o')
        
        if not prompt:
            return Response({'error': 'Prompt is required'}, status=status.HTTP_400_BAD_REQUEST)

        service = AIService()
        try:
            result = service.generate(prompt, provider_name=provider, model_name=model)
            return Response({'result': result})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AIEnhanceView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        content = request.data.get('content')
        instruction = request.data.get('instruction', 'Improve clarity and readability.')
        provider = request.data.get('provider', 'openai')
        model = request.data.get('model', 'gpt-4o')
        
        if not content:
            return Response({'error': 'Content is required'}, status=status.HTTP_400_BAD_REQUEST)

        prompt = f"Content:\n{content}\n\nInstruction: {instruction}\n\nEnhanced Content:"
        service = AIService()
        try:
            result = service.generate(prompt, provider_name=provider, model_name=model)
            return Response({'result': result})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AIAnalyzeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        repo_content = request.data.get('repo_content') # Expecting dict or text representation
        provider = request.data.get('provider', 'openai')
        model = request.data.get('model', 'gpt-4o')
        
        if not repo_content:
            return Response({'error': 'Repo content is required'}, status=status.HTTP_400_BAD_REQUEST)

        service = AIService()
        try:
            # Pass as simple prompt for now, real implementation would process repo structure
            prompt = f"Analyze this repository content and list top 3 issues:\n{str(repo_content)[:5000]}"
            result = service.generate(prompt, provider_name=provider, model_name=model)
            return Response({'result': result})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AIChatView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        messages = request.data.get('messages', []) # List of {role, content}
        provider = request.data.get('provider', 'openai')
        model = request.data.get('model', 'gpt-4o')
        
        if not messages:
            return Response({'error': 'Messages are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Simple concatenation for now, should use provider's chat interface
        prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
        
        service = AIService()
        try:
            result = service.generate(prompt, provider_name=provider, model_name=model)
            return Response({'result': result})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
