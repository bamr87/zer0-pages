"""
Factory classes for creating test data using factory_boy.
"""
import factory
from django.utils import timezone
from faker import Faker
from users.models import User
from content.models import Post, Page, SiteSettings
from prd.models import PRD
from github.models import Repository, Issue, Webhook
from ai.models import AIProvider, AIModel, PromptTemplate, AIResponse

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    """Factory for User model"""
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    password = factory.PostGenerationMethodCall('set_password', 'password')
    role = 'viewer'

    @factory.trait
    def admin(self):
        self.role = 'admin'

    @factory.trait
    def editor(self):
        self.role = 'editor'

    @factory.trait
    def viewer(self):
        self.role = 'viewer'


class SiteSettingsFactory(factory.django.DjangoModelFactory):
    """Factory for SiteSettings model"""
    class Meta:
        model = SiteSettings
        django_get_or_create = ('site_name',)

    site_name = factory.LazyFunction(lambda: fake.company())
    site_description = factory.LazyFunction(lambda: fake.text(max_nb_chars=200))
    github_repo = factory.LazyFunction(lambda: f"{fake.user_name()}/{fake.word()}")
    analytics_enabled = True
    ai_enabled = True


class PostFactory(factory.django.DjangoModelFactory):
    """Factory for Post model"""
    class Meta:
        model = Post

    title = factory.LazyFunction(lambda: fake.sentence(nb_words=6))
    slug = factory.LazyAttribute(lambda obj: fake.slug())
    content = factory.LazyFunction(lambda: fake.text(max_nb_chars=1000))
    summary = factory.LazyFunction(lambda: fake.text(max_nb_chars=200))
    status = 'draft'
    author = factory.SubFactory(UserFactory)
    published_at = None

    @factory.trait
    def published(self):
        self.status = 'published'
        self.published_at = factory.LazyFunction(timezone.now)

    @factory.trait
    def archived(self):
        self.status = 'archived'


class PageFactory(factory.django.DjangoModelFactory):
    """Factory for Page model"""
    class Meta:
        model = Page

    title = factory.LazyFunction(lambda: fake.sentence(nb_words=4))
    slug = factory.LazyAttribute(lambda obj: fake.slug())
    content = factory.LazyFunction(lambda: fake.text(max_nb_chars=500))
    status = 'draft'
    author = factory.SubFactory(UserFactory)

    @factory.trait
    def published(self):
        self.status = 'published'


class AIProviderFactory(factory.django.DjangoModelFactory):
    """Factory for AIProvider model"""
    class Meta:
        model = AIProvider
        django_get_or_create = ('name',)

    name = factory.Iterator(['openai', 'anthropic', 'xai'])
    is_active = True


class AIModelFactory(factory.django.DjangoModelFactory):
    """Factory for AIModel model"""
    class Meta:
        model = AIModel

    provider = factory.SubFactory(AIProviderFactory)
    name = factory.Iterator(['gpt-4o', 'gpt-4-turbo', 'claude-3-opus', 'claude-3-sonnet', 'grok-2'])
    context_window = 4096
    cost_per_input_token = 0.00001
    cost_per_output_token = 0.00003
    is_active = True


class PromptTemplateFactory(factory.django.DjangoModelFactory):
    """Factory for PromptTemplate model"""
    class Meta:
        model = PromptTemplate

    name = factory.LazyFunction(lambda: fake.word())
    description = factory.LazyFunction(lambda: fake.text(max_nb_chars=200))
    template = factory.LazyFunction(lambda: fake.text(max_nb_chars=500))
    input_variables = factory.LazyFunction(lambda: ['prompt', 'context'])
    version = 1
    is_active = True
    created_by = factory.SubFactory(UserFactory)


class AIResponseFactory(factory.django.DjangoModelFactory):
    """Factory for AIResponse model"""
    class Meta:
        model = AIResponse

    prompt_hash = factory.LazyFunction(lambda: fake.sha256())
    provider = factory.SubFactory(AIProviderFactory)
    model = factory.SubFactory(AIModelFactory)
    prompt_text = factory.LazyFunction(lambda: fake.text(max_nb_chars=500))
    response_text = factory.LazyFunction(lambda: fake.text(max_nb_chars=1000))
    tokens_used = factory.LazyFunction(lambda: fake.random_int(min=100, max=5000))
    cost = factory.LazyFunction(lambda: fake.pyfloat(left_digits=0, right_digits=6, positive=True))


class RepositoryFactory(factory.django.DjangoModelFactory):
    """Factory for Repository model"""
    class Meta:
        model = Repository
        django_get_or_create = ('owner', 'name')

    name = factory.LazyFunction(lambda: fake.word())
    owner = factory.LazyFunction(lambda: fake.user_name())
    url = factory.LazyAttribute(lambda obj: f"https://github.com/{obj.owner}/{obj.name}")
    default_branch = 'main'
    is_active = True


class IssueFactory(factory.django.DjangoModelFactory):
    """Factory for Issue model"""
    class Meta:
        model = Issue
        django_get_or_create = ('repository', 'number')

    repository = factory.SubFactory(RepositoryFactory)
    number = factory.Sequence(lambda n: n)
    title = factory.LazyFunction(lambda: fake.sentence(nb_words=6))
    body = factory.LazyFunction(lambda: fake.text(max_nb_chars=500))
    state = 'open'
    html_url = factory.LazyAttribute(lambda obj: f"{obj.repository.url}/issues/{obj.number}")
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)


class WebhookFactory(factory.django.DjangoModelFactory):
    """Factory for Webhook model"""
    class Meta:
        model = Webhook

    repository = factory.SubFactory(RepositoryFactory)
    event_type = factory.Iterator(['push', 'pull_request', 'issues', 'issue_comment'])
    payload = factory.LazyFunction(lambda: {'action': 'opened', 'issue': {'number': 1}})
    processed = False


class PRDFactory(factory.django.DjangoModelFactory):
    """Factory for PRD model"""
    class Meta:
        model = PRD

    title = factory.LazyFunction(lambda: fake.sentence(nb_words=5))
    version = '1.0.0'
    content = factory.LazyFunction(lambda: fake.text(max_nb_chars=2000))
    status = 'draft'
    author = factory.SubFactory(UserFactory)
    repository = factory.SubFactory(RepositoryFactory)

    @factory.trait
    def approved(self):
        self.status = 'approved'

    @factory.trait
    def review(self):
        self.status = 'review'



