# Deployment Guide

## Docker Containerization

### Dockerfile

```dockerfile
# Multi-stage build for smaller image
FROM python:3.13-slim as builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Production stage
FROM python:3.13-slim

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY src/ /app/src/

# Set ownership
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/src:$PYTHONPATH"
ENV PYTHONUNBUFFERED=1

# Expose application port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Run application
CMD ["python", "-m", "package_name.main"]
```

### .dockerignore

```dockerignore
# Git
.git
.gitignore

# Python
__pycache__
*.py[cod]
*$py.class
*.so
.Python
*.egg-info/
dist/
build/

# Virtual environments
venv/
.venv/
env/
ENV/

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/
.hypothesis/

# Type checking
.mypy_cache/
.dmypy.json
dmypy.json

# IDEs
.vscode/
.idea/
*.swp
*.swo

# Environment files
.env
.env.local
.env.*.local

# Documentation
docs/
*.md
!README.md

# CI/CD
.github/

# Docker
docker-compose.override.yml
```

## Docker Compose

### docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: project-name-app
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - SECRET_KEY=${SECRET_KEY}
      - LOG_LEVEL=${LOG_LEVEL:-INFO}
    env_file:
      - .env
    volumes:
      - ./logs:/app/logs
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "python", "-c", "import sys; sys.exit(0)"]
      interval: 30s
      timeout: 3s
      retries: 3

  db:
    image: postgres:16-alpine
    container_name: project-name-db
    environment:
      - POSTGRES_DB=${DB_NAME}
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped
    networks:
      - app-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5

networks:
  app-network:
    driver: bridge

volumes:
  postgres_data:
```

### docker-compose.override.yml (for local development)

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: builder  # Use builder stage for dev
    command: uv run python -m package_name.main
    volumes:
      - ./src:/app/src  # Mount source for live reload
      - ./tests:/app/tests
    environment:
      - DEBUG=true
      - LOG_LEVEL=DEBUG
```

## Environment Configuration

### .env.example

```bash
# Application
APP_NAME=project-name
APP_VERSION=0.1.0
DEBUG=false
LOG_LEVEL=INFO

# Database
DATABASE_URL=postgresql://user:password@db:5432/dbname
DB_NAME=projectdb
DB_USER=dbuser
DB_PASSWORD=securepassword

# Security
SECRET_KEY=change-this-to-a-secure-random-string
API_KEY=your-api-key-here

# External Services
REDIS_URL=redis://redis:6379/0
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=noreply@example.com
SMTP_PASSWORD=password

# Feature Flags
ENABLE_FEATURE_X=false
ENABLE_FEATURE_Y=true
```

### .env (DO NOT COMMIT)

```bash
# Copy from .env.example and fill in actual values
# This file should be in .gitignore
```

## Docker Commands

### Build and Run

```bash
# Build image
docker compose build

# Start services
docker compose up -d

# View logs
docker compose logs -f app

# Stop services
docker compose down

# Remove volumes
docker compose down -v
```

### Development Workflow

```bash
# Start with override for development
docker compose -f docker-compose.yml -f docker-compose.override.yml up

# Run tests in container
docker compose exec app uv run pytest

# Run linting
docker compose exec app uv run ruff check src/

# Access container shell
docker compose exec app bash

# View container stats
docker stats
```

### Production Deployment

```bash
# Build for production (without dev dependencies)
docker compose -f docker-compose.yml build

# Start in production mode
docker compose -f docker-compose.yml up -d

# Scale services (if needed)
docker compose -f docker-compose.yml up -d --scale app=3

# View resource usage
docker compose -f docker-compose.yml ps

# Backup database
docker compose exec db pg_dump -U ${DB_USER} ${DB_NAME} > backup.sql

# Restore database
docker compose exec -T db psql -U ${DB_USER} ${DB_NAME} < backup.sql
```

## Configuration Management

### Python Configuration Module

```python
# src/package_name/config.py
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )
    
    # Application
    app_name: str = "project-name"
    app_version: str = "0.1.0"
    debug: bool = False
    log_level: str = "INFO"
    
    # Database
    database_url: str
    
    # Security
    secret_key: str
    api_key: str | None = None
    
    # External services
    redis_url: str | None = None


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
```

## Security Best Practices

### 1. Never Commit Secrets

- Use `.env` files for local configuration
- Use environment variables in production
- Add `.env` to `.gitignore`
- Provide `.env.example` template
- Use secret management tools in production (e.g., Docker secrets, Kubernetes secrets)

### 2. Run as Non-Root User

```dockerfile
# Create and use non-root user
RUN useradd --create-home --shell /bin/bash appuser
USER appuser
```

### 3. Minimal Base Image

```dockerfile
# Use slim variants
FROM python:3.13-slim
```

### 4. Multi-Stage Builds

```dockerfile
# Separate build and runtime stages
FROM python:3.13-slim as builder
# ... build steps ...
FROM python:3.13-slim
# Copy only what's needed
```

### 5. Health Checks

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s \
    CMD python -c "import sys; sys.exit(0)"
```

## Monitoring and Logging

### Logging Configuration

```python
# src/package_name/logging_config.py
import logging
import sys
from pathlib import Path

from .config import get_settings


def setup_logging() -> None:
    """Configure application logging."""
    settings = get_settings()
    
    # Create logs directory
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, settings.log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_dir / "app.log"),
        ],
    )
```

### Docker Logs

```bash
# View all logs
docker compose logs

# Follow logs
docker compose logs -f app

# Tail last 100 lines
docker compose logs --tail=100 app

# Filter by time
docker compose logs --since="2024-01-01T00:00:00" app
```

## Backup and Recovery

### Database Backup Script

```bash
#!/bin/bash
# scripts/backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="./backups"
mkdir -p $BACKUP_DIR

# Backup database
docker compose exec -T db pg_dump -U ${DB_USER} ${DB_NAME} | gzip > "${BACKUP_DIR}/backup_${DATE}.sql.gz"

# Keep only last 7 backups
ls -t ${BACKUP_DIR}/backup_*.sql.gz | tail -n +8 | xargs -r rm

echo "Backup completed: backup_${DATE}.sql.gz"
```

### Database Restore

```bash
#!/bin/bash
# scripts/restore.sh

if [ -z "$1" ]; then
    echo "Usage: ./restore.sh <backup_file>"
    exit 1
fi

gunzip -c "$1" | docker compose exec -T db psql -U ${DB_USER} ${DB_NAME}
echo "Database restored from $1"
```

## Performance Optimization

### Docker Image Optimization

1. **Use specific versions** - Pin Python and dependency versions
2. **Multi-stage builds** - Reduce final image size
3. **Layer caching** - Order Dockerfile commands for optimal caching
4. **Minimal dependencies** - Only install what's needed
5. **Combine commands** - Reduce number of layers

### Container Resource Limits

```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```
