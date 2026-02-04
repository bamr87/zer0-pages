# Architecture Overview

## Backend (Django)
- **Apps**:
  - `content`: Manages Posts, Pages.
  - `ai`: Handles AI provider integration (OpenAI, Anthropic).
  - `github`: GitHub API client and webhooks.
  - `prd`: PRD generation logic.
  - `analytics`: Privacy-first analytics.
  - `users`: Custom user model and auth.

- **API**: RESTful API using Django REST Framework (DRF).

## Frontend (React)
- **Stack**: Vite, React, Tailwind CSS, Zustand, React Query.
- **Components**: Admin dashboard for managing content and settings.

## Static Site Generator (Jekyll)
- **Bridge**: Django management command `build_site` exports content to Jekyll source structure.
- **Deployment**: CI/CD pipeline builds Jekyll site and deploys to GitHub Pages.

## Infrastructure
- **Docker**: All services containerized.
- **Database**: PostgreSQL.
- **Cache/Queue**: Redis + Celery.

