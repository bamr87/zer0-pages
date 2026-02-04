# Testing Guide

This document describes the end-to-end testing framework for zer0-pages.

## Overview

The testing framework consists of three layers:

1. **Backend Integration Tests** (pytest) - API endpoint testing with real database
2. **Frontend E2E Tests** (Cypress) - Component interactions and user workflows
3. **Full-Stack E2E Tests** (Playwright) - Complete user journeys across backend and frontend

## Prerequisites

- Docker and Docker Compose
- Python 3.10+
- Node.js 18+
- PostgreSQL 14+ (or use Docker)

## Quick Start

### Backend Tests

```bash
# Start test database
docker-compose -f docker-compose.test.yml up -d db redis

# Run all backend tests
cd backend
pytest

# Run E2E tests only
pytest tests/e2e/ -m e2e

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/e2e/test_content_crud.py
```

### Frontend Tests (Cypress)

```bash
# Install dependencies
cd frontend
npm install

# Run tests headlessly
npm run test:e2e

# Open Cypress UI
npm run test:e2e:open

# Run in headed mode
npm run test:e2e:headed
```

### Full-Stack Tests (Playwright)

```bash
# Install dependencies
cd e2e
npm install

# Install Playwright browsers
npx playwright install

# Run all tests
npm run test

# Run in UI mode
npm run test:ui

# Run in headed mode
npm run test:headed

# Debug tests
npm run test:debug
```

## Test Structure

### Backend Tests

```
backend/tests/
├── e2e/                    # End-to-end tests
│   ├── test_auth_flow.py
│   ├── test_content_crud.py
│   ├── test_ai_integration.py
│   ├── test_github_integration.py
│   ├── test_prd_workflow.py
│   └── test_jekyll_build.py
├── mocks/                  # Service mocks
│   ├── ai_mocks.py
│   └── github_mocks.py
├── fixtures/               # Test data
│   ├── users.json
│   └── content.json
├── factories.py           # Model factories
├── helpers/                # Test utilities
│   ├── api_client.py
│   ├── db_helpers.py
│   └── jekyll_helpers.py
└── conftest.py            # Pytest configuration
```

### Frontend Tests

```
frontend/cypress/
├── e2e/                   # E2E test files
│   ├── auth.cy.js
│   ├── dashboard.cy.js
│   ├── posts.cy.js
│   ├── pages.cy.js
│   ├── prds.cy.js
│   └── settings.cy.js
├── fixtures/              # Test fixtures
├── support/              # Support files
│   ├── commands.js       # Custom commands
│   └── e2e.js            # Global setup
└── cypress.config.js     # Cypress configuration
```

### Full-Stack Tests

```
e2e/
├── tests/
│   ├── user-journeys/    # Complete user flows
│   │   ├── complete-content-flow.spec.js
│   │   ├── ai-generation-flow.spec.js
│   │   ├── github-integration-flow.spec.js
│   │   └── multi-user-workflow.spec.js
│   └── integration/      # API-Frontend integration
│       └── api-frontend-integration.spec.js
├── helpers/              # Test helpers
│   ├── auth_helpers.js
│   └── api_helpers.js
└── playwright.config.js  # Playwright configuration
```

## Running Tests

### All Tests

```bash
# Backend
cd backend && pytest

# Frontend
cd frontend && npm run test:e2e

# Full-stack
cd e2e && npm run test
```

### Specific Test Suites

```bash
# Backend - Authentication tests
pytest tests/e2e/test_auth_flow.py

# Backend - AI tests
pytest tests/e2e/ -m ai

# Backend - GitHub tests
pytest tests/e2e/ -m github

# Backend - Jekyll tests
pytest tests/e2e/ -m jekyll
```

### With Coverage

```bash
# Backend coverage
cd backend
pytest --cov=. --cov-report=html
open htmlcov/index.html
```

## Test Markers

Backend tests use pytest markers for categorization:

- `@pytest.mark.e2e` - End-to-end tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.ai` - AI service tests
- `@pytest.mark.github` - GitHub integration tests
- `@pytest.mark.jekyll` - Jekyll build tests
- `@pytest.mark.slow` - Slow running tests

## Test Data

### Factories

Use factories for creating test data:

```python
from tests.factories import PostFactory, UserFactory

# Create a post
post = PostFactory(title='Test Post', status='published')

# Create an admin user
admin = UserFactory(role='admin')
```

### Fixtures

Use fixtures for common test setup:

```python
def test_example(authenticated_editor_client, test_posts):
    # authenticated_editor_client is a pre-authenticated API client
    # test_posts contains pre-created posts
    pass
```

## Mocking External Services

### AI Services

```python
from unittest.mock import patch
from tests.mocks.ai_mocks import mock_openai_response

@patch('ai.services.OpenAIProvider.generate')
def test_ai_generation(mock_generate):
    mock_generate.return_value = "Generated content"
    # Test code
```

### GitHub API

```python
import responses
from tests.mocks.github_mocks import mock_github_repo_response

@responses.activate
def test_github_integration():
    mock_github_repo_response(owner='test', name='repo')
    # Test code
```

## Writing New Tests

### Backend E2E Test

```python
import pytest
from rest_framework import status

@pytest.mark.django_db
@pytest.mark.e2e
def test_create_post(authenticated_editor_client):
    url = '/api/content/posts/'
    data = {'title': 'Test', 'content': 'Content'}
    response = authenticated_editor_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
```

### Cypress Test

```javascript
describe('Feature', () => {
  beforeEach(() => {
    cy.login()
    cy.visit('/feature')
  })

  it('should do something', () => {
    cy.get('button').click()
    cy.contains('Success').should('be.visible')
  })
})
```

### Playwright Test

```javascript
import { test, expect } from '@playwright/test';
import { setupAuthenticatedContext } from '../../helpers/auth_helpers';

test('user journey', async ({ page, request }) => {
  await setupAuthenticatedContext(page, request)
  await page.goto('/')
  // Test steps
})
```

## Continuous Integration

Tests can be run in CI/CD pipelines:

```yaml
# Example GitHub Actions
- name: Run Backend Tests
  run: |
    cd backend
    pytest --cov=. --cov-report=xml

- name: Run Frontend Tests
  run: |
    cd frontend
    npm run test:e2e

- name: Run Full-Stack Tests
  run: |
    cd e2e
    npm run test
```

## Troubleshooting

### Database Issues

If tests fail due to database state:

```bash
# Reset test database
docker-compose -f docker-compose.test.yml down -v
docker-compose -f docker-compose.test.yml up -d db
cd backend
python manage.py migrate
```

### Port Conflicts

If ports are already in use:

```bash
# Check what's using the port
lsof -i :8000
lsof -i :3000

# Kill process or change ports in config files
```

### Cypress Issues

```bash
# Clear Cypress cache
cd frontend
rm -rf node_modules/.cache/cypress
npm run test:e2e:open
```

### Playwright Issues

```bash
# Reinstall browsers
cd e2e
npx playwright install --force
```

## Best Practices

1. **Isolation**: Each test should be independent and not rely on other tests
2. **Cleanup**: Clean up test data after tests complete
3. **Mocking**: Mock external services to avoid API costs and rate limits
4. **Assertions**: Use clear, descriptive assertions
5. **Naming**: Use descriptive test names that explain what is being tested
6. **Fixtures**: Reuse fixtures for common setup
7. **Markers**: Use markers to categorize and filter tests

## Coverage Goals

- Backend: >80% coverage for critical paths
- Frontend: All critical user flows covered
- Full-stack: All major user journeys tested

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [Cypress Documentation](https://docs.cypress.io/)
- [Playwright Documentation](https://playwright.dev/)
- [Django Testing](https://docs.djangoproject.com/en/stable/topics/testing/)



