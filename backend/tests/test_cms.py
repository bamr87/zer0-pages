"""
Tests for CMS functionality.
"""
import pytest
from django.urls import reverse
from rest_framework import status

from zer0_pages.cms.models import Category, Content, Tag


@pytest.mark.django_db
class TestContentAPI:
    """Test content API endpoints."""
    
    def test_list_posts_unauthenticated(self, api_client):
        """Test that public can list published posts."""
        url = reverse("posts-list")
        response = api_client.get(url)
        
        # Public access should work for posts
        assert response.status_code == status.HTTP_200_OK
    
    def test_create_post_requires_authentication(self, api_client):
        """Test that creating posts requires authentication."""
        url = reverse("posts-list")
        data = {
            "title": "Test Post",
            "body": "Test content",
        }
        response = api_client.post(url, data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_create_post_authenticated(self, authenticated_client, user):
        """Test creating a post when authenticated."""
        url = reverse("posts-list")
        data = {
            "title": "Test Post",
            "body": "Test content",
        }
        response = authenticated_client.post(url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == "Test Post"
        assert response.data["content_type"] == "post"
    
    def test_content_has_author(self, authenticated_client, user):
        """Test that created content has author set."""
        url = reverse("posts-list")
        data = {
            "title": "Test Post",
            "body": "Test content",
        }
        response = authenticated_client.post(url, data)
        
        assert response.data["author"] == user.id


@pytest.mark.django_db
class TestCategoryTag:
    """Test category and tag models."""
    
    def test_create_category(self, db):
        """Test creating a category."""
        category = Category.objects.create(
            name="Technology",
            slug="technology",
        )
        
        assert str(category) == "Technology"
    
    def test_create_tag(self, db):
        """Test creating a tag."""
        tag = Tag.objects.create(
            name="Python",
            slug="python",
        )
        
        assert str(tag) == "Python"
    
    def test_content_with_categories(self, authenticated_client, user, db):
        """Test creating content with categories."""
        category = Category.objects.create(name="Tech", slug="tech")
        
        content = Content.objects.create(
            title="Test",
            body="Content",
            author=user,
        )
        content.categories.add(category)
        
        assert category in content.categories.all()


@pytest.mark.django_db
class TestContentVersioning:
    """Test content versioning."""
    
    def test_create_version(self, authenticated_client, user):
        """Test creating a content version."""
        # Create content first
        content = Content.objects.create(
            title="Test Post",
            slug="test-post",
            body="Original content",
            author=user,
        )
        
        # Create version via API
        url = reverse("content-create-version", kwargs={"slug": "test-post"})
        response = authenticated_client.post(url, {"change_summary": "Initial version"})
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["version_number"] == 1
