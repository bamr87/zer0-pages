# zer0-pages User Manual

## Installation

### Prerequisites
- Docker and Docker Compose
- Git

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/zer0-pages.git
   cd zer0-pages
   ```

2. Configure environment:
   Copy `example.env` to `.env` and fill in the values:
   ```bash
   cp example.env .env
   ```

3. Start the application:
   ```bash
   docker-compose up -d
   ```

4. Access the application:
   - Admin Dashboard: http://localhost:3000
   - Backend API: http://localhost:8000

## Features

### AI Content Generation
- Generate blog posts and pages using OpenAI, Anthropic, or xAI.
- Use the "Generate" button in the editor.

### PRD Machine
- Link a GitHub repository in Settings.
- Go to PRDs -> New -> Generate from Repo.

### Jekyll Site Builder
- Publish content to "Published" status.
- Run the build command (automated via CI/CD or manual):
  ```bash
  docker-compose run web python manage.py build_site
  ```
- Output is generated in `jekyll_site/`.

## API Documentation
See http://localhost:8000/swagger/ for interactive API docs.

