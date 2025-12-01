# API Reference

zer0-pages provides a comprehensive REST API built with Django REST Framework.

## Authentication

The API uses JWT (JSON Web Token) authentication.

### Get Token

```http
POST /api/auth/token/
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

Response:
```json
{
  "access": "eyJ...",
  "refresh": "eyJ..."
}
```

### Use Token

Include the access token in the Authorization header:

```http
Authorization: Bearer eyJ...
```

### Refresh Token

```http
POST /api/auth/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ..."
}
```

## Core Endpoints

### Health Check

```http
GET /api/health/
```

Returns system health status (no authentication required).

### System Status

```http
GET /api/status/
```

Returns detailed system information.

## AI Endpoints

### Generate Content

```http
POST /api/ai/generate/
Authorization: Bearer {token}
Content-Type: application/json

{
  "prompt": "Write about Django REST Framework",
  "provider": "openai",
  "model": "gpt-4o",
  "max_tokens": 2000
}
```

### Enhance Content

```http
POST /api/ai/enhance/
Authorization: Bearer {token}
Content-Type: application/json

{
  "content": "Your content to enhance",
  "enhancement_type": "clarity"
}
```

Enhancement types: `clarity`, `completeness`, `readability`, `seo`, `grammar`

### Analyze Repository

```http
POST /api/ai/analyze/
Authorization: Bearer {token}
Content-Type: application/json

{
  "target": "https://github.com/owner/repo",
  "analysis_type": "code_quality"
}
```

Analysis types: `todo_scan`, `code_quality`, `documentation`, `security`, `prd`

## CMS Endpoints

### Posts

```http
# List posts
GET /api/cms/posts/

# Create post
POST /api/cms/posts/
{
  "title": "Post Title",
  "body": "Post content...",
  "status": "draft"
}

# Get post
GET /api/cms/posts/{slug}/

# Update post
PUT /api/cms/posts/{slug}/

# Delete post
DELETE /api/cms/posts/{slug}/

# Publish post
POST /api/cms/posts/{slug}/publish/
```

### Pages

```http
GET /api/cms/pages/
POST /api/cms/pages/
GET /api/cms/pages/{slug}/
PUT /api/cms/pages/{slug}/
DELETE /api/cms/pages/{slug}/
```

### PRDs

```http
GET /api/cms/prds/
POST /api/cms/prds/
GET /api/cms/prds/{id}/
PUT /api/cms/prds/{id}/
DELETE /api/cms/prds/{id}/
POST /api/cms/prds/{id}/enhance/
GET /api/cms/prds/{id}/export/?format=markdown
```

## GitHub Endpoints

### Repositories

```http
GET /api/github/repositories/
POST /api/github/repositories/
GET /api/github/repositories/{id}/
POST /api/github/repositories/{id}/scan/
GET /api/github/repositories/{id}/prd/
```

### Issues

```http
GET /api/github/issues/
POST /api/github/issues/create/
```

### Webhooks

```http
POST /api/github/webhooks/receive/
GET /api/github/webhooks/events/
```

## Analytics Endpoints

### Consent

```http
# Get consent status
GET /api/analytics/consent/?session_id={session_id}

# Update consent
POST /api/analytics/consent/
{
  "session_id": "session_id",
  "consents": {
    "essential": true,
    "analytics": true,
    "marketing": false
  }
}
```

### Track Event

```http
POST /api/analytics/track/
{
  "session_id": "session_id",
  "event_type": "page_view",
  "event_name": "Homepage View",
  "page_path": "/",
  "properties": {}
}
```

### Dashboard (Authenticated)

```http
GET /api/analytics/dashboard/?days=30
Authorization: Bearer {token}
```

## Error Responses

The API returns standard HTTP status codes:

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 500 | Internal Server Error |

Error response format:
```json
{
  "error": "Error message",
  "detail": "Additional details"
}
```

## Pagination

List endpoints support cursor-based pagination:

```http
GET /api/cms/posts/?cursor=cD0yMDIz...
```

Response includes pagination info:
```json
{
  "next": "http://localhost:8000/api/cms/posts/?cursor=...",
  "previous": null,
  "results": [...]
}
```

## Rate Limiting

The API implements rate limiting:
- Anonymous users: 100 requests/hour
- Authenticated users: 1000 requests/hour

Rate limit headers are included in responses:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1609459200
```
