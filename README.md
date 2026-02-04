# zer0-pages

> **Zero friction. Infinite possibilities.**

An AI-powered content management system that combines Django's robust backend with Jekyll's lightning-fast static site generation. Automate content creation, repository management, documentation generation, and site deployment—all with zero configuration friction.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Django 4.2+](https://img.shields.io/badge/django-4.2+-green.svg)](https://www.djangoproject.com/)
[![React 18+](https://img.shields.io/badge/react-18+-61dafb.svg)](https://reactjs.org/)

## 🚀 Features

### 🤖 AI Content Engine
- **Multi-Provider Support**: OpenAI GPT-4o, Anthropic Claude, xAI Grok
- **Content Generation**: Blog posts, documentation, PRDs from prompts or outlines
- **Content Enhancement**: Improve existing content for clarity and SEO
- **Code Analysis**: Scan repositories for TODOs, anti-patterns, and documentation gaps
- **Intelligent Caching**: Reduce API costs with response caching and TTL management

### 🔗 GitHub Integration Hub
- **Auto-Issue Generation**: AI creates structured GitHub issues with proper labels
- **Code Quality Scans**: Automated scanning for technical debt and improvements
- **Webhook Processing**: React to repository events automatically
- **Rate Limit Management**: Intelligent request batching and conditional requests

### 📋 PRD Machine
- **Generate PRDs**: Create comprehensive PRDs from GitHub repository analysis
- **Download PRDs**: Extract existing PRDs from repositories
- **Enhance PRDs**: Improve completeness and quality using AI
- **Version Control**: Track PRD changes with full history and diff visualization
- **Export**: Convert PRDs to GitHub Issues, Jira tickets

### 🎨 Jekyll Site Builder
- **Zero-Config Deployment**: Works immediately on GitHub Pages
- **Bootstrap 5 Integration**: Modern responsive design with dark/light themes
- **SEO Optimized**: Meta tags, Open Graph, structured data, sitemaps
- **Docker-First**: Universal compatibility across all platforms

### 💻 React Admin Dashboard
- **Content Editor**: Rich Markdown editing with live preview
- **Media Library**: Drag-and-drop file management
- **Prompt Studio**: Visual AI prompt builder with testing sandbox
- **Analytics Dashboard**: Real-time content performance metrics
- **GitHub Hub**: Repository connections and issue management
- **PRD Workspace**: Visual PRD editor with version comparison

### 🔒 Privacy-First Analytics
- **GDPR/CCPA Compliant**: Cookie consent with granular permissions
- **Do Not Track**: Respects browser DNT settings
- **PostHog Integration**: Privacy-compliant event tracking

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [Documentation](#documentation)
- [License](#license)

## 🏃 Quick Start

### Prerequisites

- **Docker** and **Docker Compose** (recommended)
- **Git**
- **Python 3.10+** (for local development)
- **Node.js 18+** (for frontend development)

### Docker Quick Start (Recommended)

```bash
# Clone the repository
git clone https://github.com/bamr87/zer0-pages.git
cd zer0-pages

# Copy environment file
cp example.env .env

# Edit .env and add your API keys:
# - OPENAI_API_KEY (optional)
# - ANTHROPIC_API_KEY (optional)
# - XAI_API_KEY (optional)
# - GITHUB_TOKEN (optional)

# Start all services
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Access the application
# - Admin Dashboard: http://localhost:3000
# - Backend API: http://localhost:8000
# - API Docs: http://localhost:8000/swagger/
```

### Local Development Setup

```bash
# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install

# Start PostgreSQL and Redis (via Docker)
docker-compose up -d db redis

# Run backend migrations
cd ../backend
python manage.py migrate
python manage.py createsuperuser

# Start backend (terminal 1)
python manage.py runserver

# Start frontend (terminal 2)
cd ../frontend
npm run dev
```

## 🏗️ Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    zer0-pages Platform                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────────┐      ┌──────────────────────┐   │
│  │  REACT ADMIN (SPA)   │      │ BOOTSTRAP PUBLIC SITE│   │
│  │  • Content Mgmt      │      │  • Blog / Docs       │   │
│  │  • AI Studio         │      │  • Responsive        │   │
│  │  • GitHub Dashboard  │      │  • SEO Optimized     │   │
│  └──────────┬───────────┘      └──────────┬───────────┘   │
│             │ REST API                     │ Static Files  │
│             ▼                              ▼                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Django Backend                          │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐         │  │
│  │  │ REST API │  │  Jekyll  │  │ AI Layer │         │  │
│  │  │  (DRF)   │  │ Generator│  │(Multi-   │         │  │
│  │  │          │  │          │  │ Provider)│         │  │
│  │  └──────────┘  └──────────┘  └──────────┘         │  │
│  └──────────────────────────────────────────────────────┘  │
│                        │                                    │
│  ┌─────────────────────▼────────────────────────────────┐   │
│  │         Unified Content Model                       │   │
│  │  • Posts/Pages  • PRDs  • Documentation  • Issues    │   │
│  └──────┬───────────────┬───────────────┬──────────────┘   │
│         │               │               │                   │
│  ┌──────▼────┐  ┌──────▼────┐  ┌──────▼──────┐            │
│  │PostgreSQL │  │   Redis   │  │   GitHub    │            │
│  │  Database │  │   Cache   │  │    API      │            │
│  └───────────┘  └───────────┘  └─────────────┘            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Backend** | Django 4.2+ | CMS API, Business Logic |
| **Static Gen** | Jekyll 4.3+ | Fast static site generation |
| **Public Frontend** | Bootstrap 5.3 | Publication site UI |
| **Admin Frontend** | React 18+ | CMS dashboard, content editor |
| **Database** | PostgreSQL 14+ | Primary data store |
| **Cache** | Redis | API response caching, Celery broker |
| **AI** | OpenAI/Anthropic/xAI | Content generation, analysis |
| **Container** | Docker + Compose | Universal development environment |

## ⚙️ Configuration

### Environment Variables

Copy `example.env` to `.env` and configure:

```bash
# Django Settings
DEBUG=1
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
POSTGRES_DB=zer0pages
POSTGRES_USER=zer0pages
POSTGRES_PASSWORD=zer0pages
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Redis
REDIS_URL=redis://redis:6379/0

# AI Providers (at least one recommended)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
XAI_API_KEY=xai-...

# GitHub Integration
GITHUB_TOKEN=ghp_...

# Optional: Error Tracking
SENTRY_DSN=https://...
```

### Initial Setup

1. **Create Admin User**:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

2. **Configure Site Settings**:
   - Access admin dashboard at http://localhost:3000
   - Navigate to Settings
   - Configure site name, description, and GitHub repository

3. **Connect GitHub** (optional):
   - Generate a GitHub Personal Access Token with `repo` scope
   - Add token to `.env` file
   - Connect repositories in the GitHub Hub section

4. **Configure AI Providers** (optional):
   - Add API keys to `.env` file
   - Test AI generation in the Prompt Studio

## 📖 Usage

### Creating Content

1. **Blog Posts**:
   - Navigate to Content → Posts
   - Click "New Post"
   - Use AI generation (optional) or write manually
   - Preview and publish

2. **Pages**:
   - Navigate to Content → Pages
   - Create static pages (About, Contact, etc.)
   - Publish when ready

3. **PRDs**:
   - Navigate to PRDs → New
   - Generate from GitHub repository or create manually
   - Enhance with AI suggestions
   - Export to GitHub Issues or Jira

### AI Content Generation

```python
# Example: Generate blog post via API
POST /api/ai/generate/
{
  "prompt": "Write a blog post about Django best practices",
  "content_type": "blog_post",
  "provider": "openai",
  "model": "gpt-4o"
}
```

### Building Static Site

```bash
# Generate Jekyll site from published content
docker-compose exec web python manage.py build_site

# Output will be in jekyll_site/ directory
# Deploy to GitHub Pages or any static hosting
```

### GitHub Integration

1. **Auto-Issue Generation**:
   - Connect repository in GitHub Hub
   - Run code quality scan
   - Review and approve generated issues

2. **Webhook Setup**:
   - Configure webhook in repository settings
   - Point to `/api/github/webhooks/`
   - Select events: push, pull_request, issues

## 📚 API Documentation

Interactive API documentation is available at:
- **Swagger UI**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/

### Key Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/posts/` | GET, POST | Blog posts CRUD |
| `/api/pages/` | GET, POST | Static pages CRUD |
| `/api/prds/` | GET, POST | PRD management |
| `/api/ai/generate/` | POST | AI content generation |
| `/api/ai/enhance/` | POST | Content enhancement |
| `/api/github/issues/` | GET, POST | GitHub issues sync |
| `/api/analytics/` | GET | Usage statistics |
| `/api/auth/token/` | POST | JWT authentication |

### Authentication

All API endpoints require authentication via JWT tokens:

```bash
# Get access token
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'

# Use token in requests
curl -H "Authorization: Bearer <token>" \
  http://localhost:8000/api/posts/
```

## 🛠️ Development

### Project Structure

```
zer0-pages/
├── backend/                 # Django backend
│   ├── content/            # Content models and views
│   ├── ai/                 # AI provider integration
│   ├── github/             # GitHub API client
│   ├── prd/                # PRD generation logic
│   ├── analytics/          # Analytics tracking
│   ├── users/              # User management
│   └── zer0pages/          # Django project settings
├── frontend/               # React admin dashboard
│   ├── src/
│   │   ├── components/     # Reusable components
│   │   ├── pages/          # Page components
│   │   └── services/       # API client
│   └── dist/               # Build output
├── docs/                   # Documentation
├── docker-compose.yml      # Production Docker setup
└── docker-compose.dev.yml  # Development Docker setup
```

### Running Tests

```bash
# Backend tests
cd backend
pytest

# With coverage
pytest --cov=. --cov-report=html

# Frontend tests (when implemented)
cd frontend
npm test
```

### Code Style

- **Python**: Follow PEP 8, use Black for formatting
- **JavaScript**: ESLint with React plugin
- **Pre-commit**: Run linters before committing

## 🧪 Testing

### Backend Testing

```bash
# Run all tests
docker-compose exec web pytest

# Run specific test file
docker-compose exec web pytest tests/test_content.py

# Run with coverage
docker-compose exec web pytest --cov=. --cov-report=term-missing
```

### Frontend Testing

```bash
cd frontend
npm run lint          # ESLint
npm run test          # Unit tests (when implemented)
npm run test:e2e      # E2E tests with Cypress
```

## 🚢 Deployment

### GitHub Pages Deployment

1. **Build Static Site**:
   ```bash
   docker-compose exec web python manage.py build_site
   ```

2. **Deploy to GitHub Pages**:
   - Push `jekyll_site/` to `gh-pages` branch
   - Or configure GitHub Actions for automatic deployment

### Production Deployment

1. **Update Environment**:
   ```bash
   DEBUG=0
   SECRET_KEY=<strong-secret-key>
   ALLOWED_HOSTS=yourdomain.com
   ```

2. **Build and Deploy**:
   ```bash
   docker-compose -f docker-compose.yml build
   docker-compose -f docker-compose.yml up -d
   ```

3. **Run Migrations**:
   ```bash
   docker-compose exec web python manage.py migrate
   ```

4. **Collect Static Files**:
   ```bash
   docker-compose exec web python manage.py collectstatic --noinput
   ```

### Health Checks

Monitor application health:
```bash
curl http://localhost:8000/admin/
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Reporting Issues

Please use the [GitHub issue tracker](https://github.com/bamr87/zer0-pages/issues) to report bugs or suggest features.

## 📚 Documentation

- [Architecture](docs/ARCHITECTURE.md) - System architecture overview
- [Docker Guide](docs/DOCKER.md) - Docker setup and configuration
- [Frontend Testing](docs/FRONTEND_TESTING.md) - Frontend testing guide
- [Contributing](docs/CONTRIBUTING.md) - Contribution guidelines
- [User Manual](docs/README.md) - User-facing documentation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Django and Django REST Framework
- React and the React ecosystem
- Jekyll and GitHub Pages
- OpenAI, Anthropic, and xAI for AI capabilities
- All contributors and users

## 📞 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/bamr87/zer0-pages/issues)
- **Discussions**: [GitHub Discussions](https://github.com/bamr87/zer0-pages/discussions)

---

**Made with ❤️ by the zer0-pages team**

*Zero friction. Infinite possibilities.*



