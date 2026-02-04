"""
E2E tests for content CRUD operations.
"""
import pytest
from rest_framework import status
from content.models import Post, Page


@pytest.mark.django_db
@pytest.mark.e2e
class TestPostCRUD:
    """Test Post CRUD operations end-to-end"""
    
    def test_create_post(self, authenticated_editor_client):
        """Test creating a new post"""
        url = '/api/content/posts/'
        data = {
            'title': 'Test Post',
            'content': 'This is test content',
            'summary': 'Test summary',
            'status': 'draft'
        }
        response = authenticated_editor_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'Test Post'
        assert Post.objects.filter(title='Test Post').exists()
    
    def test_list_posts(self, authenticated_editor_client, test_posts):
        """Test listing posts"""
        url = '/api/content/posts/'
        response = authenticated_editor_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) > 0
    
    def test_get_post_detail(self, authenticated_editor_client, test_posts):
        """Test retrieving a specific post"""
        post = test_posts[0]
        url = f'/api/content/posts/{post.id}/'
        response = authenticated_editor_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == post.id
        assert response.data['title'] == post.title
    
    def test_update_post(self, authenticated_editor_client, test_posts):
        """Test updating a post"""
        post = test_posts[0]
        url = f'/api/content/posts/{post.id}/'
        data = {
            'title': 'Updated Title',
            'content': post.content,
            'status': post.status
        }
        response = authenticated_editor_client.patch(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated Title'
        post.refresh_from_db()
        assert post.title == 'Updated Title'
    
    def test_publish_post(self, authenticated_editor_client, test_posts):
        """Test publishing a draft post"""
        post = test_posts[0]
        post.status = 'draft'
        post.save()
        
        url = f'/api/content/posts/{post.id}/'
        data = {
            'status': 'published'
        }
        response = authenticated_editor_client.patch(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'published'
        post.refresh_from_db()
        assert post.status == 'published'
    
    def test_delete_post(self, authenticated_editor_client, test_posts):
        """Test deleting a post"""
        post = test_posts[0]
        post_id = post.id
        url = f'/api/content/posts/{post_id}/'
        response = authenticated_editor_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Post.objects.filter(id=post_id).exists()
    
    def test_filter_posts_by_status(self, authenticated_editor_client, test_posts):
        """Test filtering posts by status"""
        url = '/api/content/posts/?status=published'
        response = authenticated_editor_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        for post in response.data['results']:
            assert post['status'] == 'published'
    
    def test_search_posts(self, authenticated_editor_client, test_posts):
        """Test searching posts"""
        url = '/api/content/posts/?search=test'
        response = authenticated_editor_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
    
    def test_viewer_cannot_create_post(self, authenticated_admin_client, viewer_user):
        """Test that viewer role cannot create posts"""
        # Create viewer client
        from tests.helpers.api_client import AuthenticatedAPIClient
        viewer_client = AuthenticatedAPIClient()
        viewer_client.authenticate_user(viewer_user)
        
        url = '/api/content/posts/'
        data = {'title': 'Test', 'content': 'Test'}
        response = viewer_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
@pytest.mark.e2e
class TestPageCRUD:
    """Test Page CRUD operations end-to-end"""
    
    def test_create_page(self, authenticated_editor_client):
        """Test creating a new page"""
        url = '/api/content/pages/'
        data = {
            'title': 'Test Page',
            'content': 'This is test page content',
            'status': 'draft'
        }
        response = authenticated_editor_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'Test Page'
        assert Page.objects.filter(title='Test Page').exists()
    
    def test_list_pages(self, authenticated_editor_client, test_pages):
        """Test listing pages"""
        url = '/api/content/pages/'
        response = authenticated_editor_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) > 0
    
    def test_update_page(self, authenticated_editor_client, test_pages):
        """Test updating a page"""
        page = test_pages[0]
        url = f'/api/content/pages/{page.id}/'
        data = {'title': 'Updated Page Title'}
        response = authenticated_editor_client.patch(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated Page Title'



