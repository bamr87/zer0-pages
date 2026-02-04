# Docker Setup Guide

## Quick Start

1. **Copy environment file**:
   ```bash
   cp example.env .env
   ```

2. **Build and start containers**:
   ```bash
   docker-compose up -d --build
   ```

3. **Run migrations**:
   ```bash
   docker-compose run --rm web python manage.py migrate
   ```

4. **Create superuser** (optional):
   ```bash
   docker-compose run --rm web python manage.py createsuperuser
   ```

5. **Access the application**:
   - Backend API: http://localhost:8000
   - Admin Panel: http://localhost:8000/admin/
   - API Docs: http://localhost:8000/swagger/

## Services

- **web**: Django backend server (port 8000)
- **db**: PostgreSQL database (port 5432)
- **redis**: Redis cache/queue (port 6379)
- **celery**: Celery worker for background tasks

## Development

For development with hot-reload:
```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

## Troubleshooting

### View logs:
```bash
docker-compose logs -f web
```

### Rebuild containers:
```bash
docker-compose build --no-cache
docker-compose up -d
```

### Reset database:
```bash
docker-compose down -v
docker-compose up -d
docker-compose run --rm web python manage.py migrate
```

### Access database shell:
```bash
docker-compose exec db psql -U zer0pages -d zer0pages
```

