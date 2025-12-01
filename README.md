# zer0-pages

> Zero friction. Infinite possibilities.

AI-Powered Content Management System that combines Django's robust backend with Jekyll's lightning-fast static site generation.

## Features

- **AI-First Architecture**: Every feature enhanced by OpenAI, Anthropic, and xAI integration
- **Django + Jekyll Hybrid**: Dynamic CMS backend with static site performance
- **Dual Frontend Strategy**: React admin dashboard + Bootstrap public sites
- **GitHub-Native Workflows**: Automated issue management, PRD tracking, and documentation
- **Zero-Configuration Deployment**: Works immediately on GitHub Pages, Azure, or any hosting platform
- **Privacy-First Analytics**: GDPR/CCPA compliant with granular user consent
- **Docker-First Development**: Universal compatibility across all platforms

## Quick Start

### Docker (Recommended)

```bash
git clone https://github.com/bamr87/zer0-pages.git
cd zer0-pages
docker-compose up -d
```

Access the application:
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs/
- **Jekyll Site**: http://localhost:4000

### Manual Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/bamr87/zer0-pages.git
   cd zer0-pages
   ```

2. **Set up the backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

3. **Set up Jekyll site**
   ```bash
   cd frontend/public
   bundle install
   bundle exec jekyll serve
   ```

## Configuration

Create a `.env` file in the backend directory:

```env
# Django
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=zer0_pages
DB_USER=zer0_pages
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# AI Providers
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
XAI_API_KEY=your-xai-key

# GitHub
GITHUB_TOKEN=your-github-token
GITHUB_WEBHOOK_SECRET=your-webhook-secret

# Redis
REDIS_URL=redis://localhost:6379/1
CELERY_BROKER_URL=redis://localhost:6379/0
```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/api/health/` | Health check |
| `/api/status/` | System status |
| `/api/auth/token/` | JWT authentication |
| `/api/ai/generate/` | AI content generation |
| `/api/ai/enhance/` | Content enhancement |
| `/api/ai/analyze/` | Repository analysis |
| `/api/cms/posts/` | Blog posts CRUD |
| `/api/cms/pages/` | Static pages CRUD |
| `/api/cms/prds/` | PRD management |
| `/api/github/repositories/` | Repository management |
| `/api/github/issues/` | Issue tracking |
| `/api/analytics/track/` | Event tracking |
| `/api/analytics/dashboard/` | Analytics dashboard |

## Project Structure

```
zer0-pages/
├── backend/               # Django backend
│   ├── zer0_pages/
│   │   ├── api/          # Core API (health, auth)
│   │   ├── ai/           # AI content engine
│   │   ├── cms/          # Content management
│   │   ├── github/       # GitHub integration
│   │   └── analytics/    # Privacy-first analytics
│   ├── tests/
│   ├── manage.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── admin/            # React admin dashboard (planned)
│   └── public/           # Jekyll static site
│       ├── _layouts/
│       ├── _includes/
│       ├── _posts/
│       ├── assets/
│       └── _config.yml
├── docs/                  # Documentation
├── scripts/               # Utility scripts
├── docker-compose.yml
├── PRD.md
└── README.md
```

## Testing

```bash
cd backend
pytest
```

## Development

### Running with Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Running Tests

```bash
# Backend tests
cd backend
pytest -v

# With coverage
pytest --cov=zer0_pages
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Links

- [Documentation](https://zer0-pages.dev/docs)
- [GitHub Repository](https://github.com/bamr87/zer0-pages)
- [Issue Tracker](https://github.com/bamr87/zer0-pages/issues)
