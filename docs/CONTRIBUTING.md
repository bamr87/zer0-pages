# Contributing to zer0-pages

## Development Setup

1. Start development services:
   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
   ```

2. Run tests:
   ```bash
   docker-compose run web pytest
   ```

3. Frontend development:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## Code Style
- Backend: Follow PEP 8.
- Frontend: Follow standard React/ESLint rules.

## Pull Requests
- Create a branch for your feature.
- Ensure tests pass.
- Submit PR with description of changes.

