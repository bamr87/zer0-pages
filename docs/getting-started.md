# Getting Started with zer0-pages

This guide will help you get zer0-pages up and running in under 10 minutes.

## Prerequisites

- Python 3.10 or higher
- PostgreSQL 14 or higher (or Docker)
- Redis (or Docker)
- Ruby 2.7+ and Jekyll (for static site)

## Quick Start with Docker

The fastest way to get started is using Docker:

```bash
# Clone the repository
git clone https://github.com/bamr87/zer0-pages.git
cd zer0-pages

# Start all services
docker-compose up -d

# Check status
docker-compose ps
```

Access the services:
- **Django API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/docs/
- **Jekyll Site**: http://localhost:4000

## Creating Your First Content

### 1. Create an Admin User

```bash
docker-compose exec backend python manage.py createsuperuser
```

### 2. Get an Access Token

```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your-password"}'
```

### 3. Create a Blog Post

```bash
curl -X POST http://localhost:8000/api/cms/posts/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Post",
    "body": "Hello, zer0-pages!",
    "status": "published"
  }'
```

### 4. Generate Content with AI

```bash
curl -X POST http://localhost:8000/api/ai/generate/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a blog post about getting started with AI-powered CMS"
  }'
```

## Next Steps

- [Configure AI providers](configuration.md#ai-providers)
- [Set up GitHub integration](github-integration.md)
- [Customize your Jekyll theme](jekyll-theming.md)
- [Deploy to production](deployment.md)
