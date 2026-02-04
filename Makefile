.PHONY: help test test-backend test-frontend test-e2e test-all coverage clean

help:
	@echo "Available commands:"
	@echo "  make test-backend    - Run backend tests"
	@echo "  make test-frontend   - Run frontend Cypress tests"
	@echo "  make test-e2e        - Run full-stack Playwright tests"
	@echo "  make test-all        - Run all test suites"
	@echo "  make coverage        - Generate coverage report"
	@echo "  make clean           - Clean test artifacts"

test-backend:
	@echo "Running backend tests..."
	cd backend && pytest tests/e2e/ -m e2e -v

test-frontend:
	@echo "Running frontend tests..."
	cd frontend && npm run test:e2e

test-e2e:
	@echo "Running full-stack E2E tests..."
	cd e2e && npm run test

test-all: test-backend test-frontend test-e2e
	@echo "All tests completed!"

coverage:
	@echo "Generating coverage report..."
	cd backend && pytest --cov=. --cov-report=html --cov-report=term
	@echo "Coverage report generated in backend/htmlcov/"

clean:
	@echo "Cleaning test artifacts..."
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name "htmlcov" -exec rm -r {} +
	find . -type d -name ".coverage" -exec rm -r {} +
	find . -type d -name "test-results" -exec rm -r {} +
	find . -type d -name "playwright-report" -exec rm -r {} +
	find . -type d -name "cypress/videos" -exec rm -r {} +
	find . -type d -name "cypress/screenshots" -exec rm -r {} +
	@echo "Cleanup complete!"

test-setup:
	@echo "Setting up test environment..."
	docker-compose -f docker-compose.test.yml up -d db redis
	@echo "Waiting for services to be ready..."
	sleep 5
	cd backend && python manage.py migrate
	@echo "Test environment ready!"



