"""
E2E tests for PRD workflow.
"""
import pytest
from rest_framework import status
from prd.models import PRD
from tests.factories import PRDFactory


@pytest.mark.django_db
@pytest.mark.e2e
class TestPRDWorkflow:
    """Test PRD generation and workflow end-to-end"""
    
    def test_create_prd(self, authenticated_editor_client, test_repository):
        """Test creating a PRD"""
        url = '/api/prd/prds/'
        data = {
            'title': 'Test PRD',
            'version': '1.0.0',
            'content': 'PRD content here',
            'status': 'draft',
            'repository': test_repository.id
        }
        response = authenticated_editor_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert PRD.objects.filter(title='Test PRD').exists()
    
    def test_list_prds(self, authenticated_editor_client, test_prd):
        """Test listing PRDs"""
        url = '/api/prd/prds/'
        response = authenticated_editor_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) > 0
    
    def test_get_prd_detail(self, authenticated_editor_client, test_prd):
        """Test retrieving a specific PRD"""
        url = f'/api/prd/prds/{test_prd.id}/'
        response = authenticated_editor_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == test_prd.id
    
    def test_update_prd_status(self, authenticated_editor_client, test_prd):
        """Test updating PRD status"""
        url = f'/api/prd/prds/{test_prd.id}/'
        data = {'status': 'review'}
        response = authenticated_editor_client.patch(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'review'
        test_prd.refresh_from_db()
        assert test_prd.status == 'review'
    
    def test_prd_versioning(self, authenticated_editor_client, test_prd):
        """Test PRD version management"""
        # Create new version
        url = '/api/prd/prds/'
        data = {
            'title': test_prd.title,
            'version': '2.0.0',
            'content': 'Updated PRD content',
            'status': 'draft',
            'repository': test_prd.repository.id if test_prd.repository else None
        }
        response = authenticated_editor_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert PRD.objects.filter(title=test_prd.title, version='2.0.0').exists()
    
    @pytest.mark.skip(reason="PRD generation from repo requires AI service")
    def test_generate_prd_from_repo(self, authenticated_editor_client, test_repository):
        """Test generating PRD from repository analysis"""
        # This would require AI service integration
        # Placeholder for future implementation
        pass
    
    def test_prd_workflow_states(self, authenticated_editor_client, test_prd):
        """Test PRD workflow state transitions"""
        # Draft -> Review
        url = f'/api/prd/prds/{test_prd.id}/'
        data = {'status': 'review'}
        response = authenticated_editor_client.patch(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        
        # Review -> Approved
        data = {'status': 'approved'}
        response = authenticated_editor_client.patch(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        
        # Approved -> Implemented
        data = {'status': 'implemented'}
        response = authenticated_editor_client.patch(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK



