from .models import PRD
from github.models import Repository
from ai.services import AIService
from github.services import GitHubService

class PRDService:
    def generate_from_repo(self, repository_id, user):
        repo = Repository.objects.get(id=repository_id)
        
        # 1. Fetch repo structure/content
        gh_service = GitHubService()
        # Simplified: just getting repo info, real implementation would crawl
        repo_info = gh_service.get_repo(repo.owner, repo.name)
        
        # 2. Use AI to generate PRD
        ai_service = AIService()
        prompt = f"Generate a Product Requirements Document (PRD) for a GitHub repository with the following details:\n{repo_info}\n\nInclude sections: Executive Summary, Goals, User Stories, Technical Architecture."
        content = ai_service.generate(prompt, model_name="gpt-4o")
        
        # 3. Create PRD
        prd = PRD.objects.create(
            title=f"PRD for {repo.name}",
            version="0.1.0",
            content=content,
            author=user,
            repository=repo,
            status='draft'
        )
        return prd

    def enhance_prd(self, prd_id, instruction):
        prd = PRD.objects.get(id=prd_id)
        ai_service = AIService()
        
        prompt = f"Enhance this PRD based on the following instruction: {instruction}\n\nCurrent PRD:\n{prd.content}"
        enhanced_content = ai_service.generate(prompt, model_name="gpt-4o")
        
        # Create new version? Or update? 
        # For now, update content and bump version (simplified)
        # Parse version string and increment logic omitted
        prd.content = enhanced_content
        prd.save()
        return prd

    def export_to_issue(self, prd_id):
        prd = PRD.objects.get(id=prd_id)
        if not prd.repository:
            raise ValueError("PRD is not linked to a repository")
        
        gh_service = GitHubService()
        issue = gh_service.create_issue(
            prd.repository.owner,
            prd.repository.name,
            title=f"PRD: {prd.title} v{prd.version}",
            body=prd.content,
            labels=['documentation', 'prd']
        )
        return issue

