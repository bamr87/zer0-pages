import pytest
import os
import shutil
from rest_framework.test import APIClient
from django.core.management import call_command
from users.models import User
from tests.factories import (
    UserFactory, PostFactory, PageFactory, RepositoryFactory,
    IssueFactory, PRDFactory, AIProviderFactory, AIModelFactory
)
from tests.helpers.api_client import AuthenticatedAPIClient


@pytest.fixture
def api_client():
    """Standard API client"""
    return APIClient()


@pytest.fixture
def authenticated_client():
    """Authenticated API client"""
    return AuthenticatedAPIClient()


@pytest.fixture
def admin_user():
    """Admin user fixture"""
    return UserFactory(username='admin', role='admin')


@pytest.fixture
def editor_user():
    """Editor user fixture"""
    return UserFactory(username='editor', role='editor')


@pytest.fixture
def viewer_user():
    """Viewer user fixture"""
    return UserFactory(username='viewer', role='viewer')


@pytest.fixture
def authenticated_admin_client(admin_user):
    """Authenticated API client with admin user"""
    client = AuthenticatedAPIClient()
    client.authenticate_user(admin_user)
    return client


@pytest.fixture
def authenticated_editor_client(editor_user):
    """Authenticated API client with editor user"""
    client = AuthenticatedAPIClient()
    client.authenticate_user(editor_user)
    return client


@pytest.fixture
def test_posts(editor_user):
    """Create test posts"""
    return PostFactory.create_batch(5, author=editor_user)


@pytest.fixture
def test_pages(editor_user):
    """Create test pages"""
    return PageFactory.create_batch(3, author=editor_user)


@pytest.fixture
def test_repository():
    """Create test repository"""
    return RepositoryFactory(owner='test', name='test-repo')


@pytest.fixture
def test_issues(test_repository):
    """Create test issues"""
    return IssueFactory.create_batch(3, repository=test_repository)


@pytest.fixture
def test_prd(editor_user, test_repository):
    """Create test PRD"""
    return PRDFactory(author=editor_user, repository=test_repository)


@pytest.fixture
def ai_provider_setup():
    """Set up AI providers and models"""
    openai_provider = AIProviderFactory(name='openai')
    anthropic_provider = AIProviderFactory(name='anthropic')
    
    AIModelFactory(provider=openai_provider, name='gpt-4o')
    AIModelFactory(provider=openai_provider, name='gpt-4-turbo')
    AIModelFactory(provider=anthropic_provider, name='claude-3-opus')
    
    return {
        'openai': openai_provider,
        'anthropic': anthropic_provider
    }


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """Enable database access for all tests"""
    pass


@pytest.fixture
def jekyll_output_dir(tmp_path):
    """Temporary directory for Jekyll output"""
    output_dir = tmp_path / "jekyll_site"
    output_dir.mkdir()
    yield str(output_dir)
    # Cleanup
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    """Set up test database with migrations"""
    with django_db_blocker.unblock():
        call_command('migrate', verbosity=0)

