import pytest
from content.models import Post

@pytest.mark.django_db
def test_create_post(api_client, editor_user):
    api_client.force_authenticate(user=editor_user)
    data = {'title': 'Test Post', 'content': 'Content'}
    response = api_client.post('/api/content/posts/', data)
    assert response.status_code == 201
    assert Post.objects.count() == 1
    assert Post.objects.first().title == 'Test Post'

@pytest.mark.django_db
def test_list_posts_public(api_client):
    # Assuming viewers can list published posts? 
    # Viewset permission is Viewer for list
    response = api_client.get('/api/content/posts/')
    assert response.status_code == 401 # Because IsViewer requires auth

@pytest.mark.django_db
def test_list_posts_auth(api_client, editor_user):
    api_client.force_authenticate(user=editor_user)
    response = api_client.get('/api/content/posts/')
    assert response.status_code == 200

