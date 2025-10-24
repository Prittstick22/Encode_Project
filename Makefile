.PHONY: help up down restart logs build test clean status

help: ## Show this help message
	@echo "Portfolio Management Application - Make Commands"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

up: ## Start all services
	@echo "Starting services..."
	docker-compose up -d
	@echo "Waiting for services to be ready..."
	@sleep 10
	@make status

down: ## Stop all services
	@echo "Stopping services..."
	docker-compose down

restart: ## Restart all services
	@echo "Restarting services..."
	docker-compose restart

logs: ## View logs from all services
	docker-compose logs -f

logs-backend: ## View backend logs only
	docker-compose logs -f backend

logs-postgres: ## View PostgreSQL logs only
	docker-compose logs -f postgres

logs-grafana: ## View Grafana logs only
	docker-compose logs -f grafana

build: ## Build all services
	@echo "Building services..."
	docker-compose build

rebuild: ## Rebuild all services from scratch
	@echo "Rebuilding services..."
	docker-compose build --no-cache

test: ## Run backend tests
	@echo "Running tests..."
	docker-compose exec backend python -m pytest -v

test-coverage: ## Run tests with coverage report
	@echo "Running tests with coverage..."
	docker-compose exec backend python -m pytest --cov=. --cov-report=html --cov-report=term

clean: ## Remove all containers, volumes, and images
	@echo "Cleaning up..."
	docker-compose down -v --rmi all

clean-data: ## Remove only data volumes (keeps images)
	@echo "Removing data volumes..."
	docker-compose down -v

status: ## Show status of all services
	@echo "Service Status:"
	@docker-compose ps

shell-backend: ## Open shell in backend container
	docker-compose exec backend /bin/bash

shell-postgres: ## Open PostgreSQL shell
	docker-compose exec postgres psql -U portfolio_user -d portfolio_db

health: ## Check health of all services
	@echo "Checking service health..."
	@curl -s http://localhost:5000/health | jq || echo "Backend not responding"
	@curl -s http://localhost:3000/api/health | jq || echo "Grafana not responding"
	@curl -s http://localhost:9090/-/healthy && echo "Prometheus healthy" || echo "Prometheus not responding"

sample-data: ## Load sample portfolio data
	@echo "Loading sample data..."
	./load_sample_data.sh

setup: ## Initial setup (create .env, start services, load data)
	@echo "Running initial setup..."
	@if [ ! -f .env ]; then cp .env.example .env; echo "Created .env file"; fi
	@make up
	@echo "Waiting for services to fully start..."
	@sleep 15
	@make sample-data
	@echo ""
	@echo "Setup complete! Access the application at:"
	@echo "  Backend API: http://localhost:5000"
	@echo "  Grafana: http://localhost:3000 (admin/admin)"
	@echo "  Prometheus: http://localhost:9090"

backup-db: ## Backup PostgreSQL database
	@echo "Backing up database..."
	@mkdir -p backups
	docker-compose exec -T postgres pg_dump -U portfolio_user portfolio_db > backups/backup_$$(date +%Y%m%d_%H%M%S).sql
	@echo "Backup completed: backups/backup_$$(date +%Y%m%d_%H%M%S).sql"

restore-db: ## Restore PostgreSQL database (usage: make restore-db FILE=backups/backup_file.sql)
	@if [ -z "$(FILE)" ]; then echo "Error: Please specify FILE=path/to/backup.sql"; exit 1; fi
	@echo "Restoring database from $(FILE)..."
	docker-compose exec -T postgres psql -U portfolio_user portfolio_db < $(FILE)
	@echo "Restore completed"

lint: ## Lint Python code
	@echo "Linting Python code..."
	docker-compose exec backend python -m flake8 . || true

format: ## Format Python code with black
	@echo "Formatting Python code..."
	docker-compose exec backend python -m black . || echo "Install black: pip install black"

update: ## Update all Docker images
	@echo "Updating Docker images..."
	docker-compose pull

prune: ## Remove unused Docker resources
	@echo "Pruning Docker resources..."
	docker system prune -f

dev: ## Start services in development mode with live reload
	docker-compose up

prod: ## Start services in production mode
	docker-compose -f docker-compose.yml up -d

.DEFAULT_GOAL := help
