---
name: docker-dev
description: Docker containerization for development and deployment. Use when creating Dockerfiles, docker compose configurations, or deploying applications with containers. Provides multi-stage builds, security best practices, docker compose orchestration, environment configuration, and deployment patterns. Emphasizes security (non-root users, minimal images) and portability.
---

# Docker Development

Docker containerization skill for building and deploying applications with security and best practices.

## Core Principles

1. **Multi-stage Builds** - Minimize final image size
2. **Security First** - Non-root users, minimal base images
3. **Environment Configuration** - .env files, never commit secrets
4. **Portability** - Works across environments
5. **Development vs Production** - Different configurations for each

## Quick Start

### Create Dockerfile

Use bundled template:

```bash
cp assets/Dockerfile.template Dockerfile
# Edit package_name and customize
```

### Create docker-compose.yml

```bash
cp assets/docker-compose.yml.template docker-compose.yml
cp assets/env.example.template .env.example
cp .env.example .env
# Edit configuration
```

### Build and Run

```bash
# Build image
docker compose build

# Start services
docker compose up -d

# View logs
docker compose logs -f

# Stop services
docker compose down
```

## Dockerfile Best Practices

### Multi-stage Build

```dockerfile
# Build stage
FROM python:3.13-slim as builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Production stage
FROM python:3.13-slim

RUN useradd --create-home appuser
WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY src/ /app/src/

RUN chown -R appuser:appuser /app
USER appuser

ENV PATH="/app/.venv/bin:$PATH"
CMD ["python", "-m", "package_name"]
```

### Security Practices

1. **Use slim base images** - `python:3.13-slim` not `python:3.13`
2. **Run as non-root** - Create and use dedicated user
3. **Multi-stage builds** - Separate build and runtime
4. **Minimal layers** - Combine RUN commands
5. **Specific versions** - Pin Python and dependency versions

See [references/dockerfile-patterns.md](references/dockerfile-patterns.md) for more examples.

## Docker Compose

### Basic Service

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
    env_file:
      - .env
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
```

### With Database

```yaml
services:
  app:
    build: .
    depends_on:
      db:
        condition: service_healthy
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/dbname
  
  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_DB=dbname
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "user"]
      interval: 10s

volumes:
  postgres_data:
```

See [references/compose-patterns.md](references/compose-patterns.md) for complete examples.

## Environment Configuration

### .env File

```bash
# Application
APP_NAME=my-app
DEBUG=false

# Database
DATABASE_URL=postgresql://user:pass@db:5432/dbname

# Secrets (NEVER commit)
SECRET_KEY=change-this-secret
API_KEY=your-api-key
```

### .env.example Template

```bash
# Application
APP_NAME=my-app
DEBUG=false

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname

# Secrets (fill in your values)
SECRET_KEY=
API_KEY=
```

**Always:**
- Include .env.example in repository
- Add .env to .gitignore
- Never commit secrets to Git

## Development vs Production

### Development Configuration

```yaml
# docker-compose.override.yml
services:
  app:
    build:
      target: builder
    command: uv run python -m package_name
    volumes:
      - ./src:/app/src  # Live reload
    environment:
      - DEBUG=true
```

### Production Configuration

```yaml
# docker-compose.yml (production)
services:
  app:
    build:
      context: .
    restart: always
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
```

## Docker Commands

### Build and Run

```bash
# Build image
docker compose build

# Build without cache
docker compose build --no-cache

# Start services
docker compose up -d

# Start specific service
docker compose up -d app

# View logs
docker compose logs -f app

# Follow logs for all services
docker compose logs -f
```

### Management

```bash
# List running containers
docker compose ps

# Stop services
docker compose down

# Stop and remove volumes
docker compose down -v

# Execute command in container
docker compose exec app bash

# Run one-off command
docker compose run app pytest
```

### Cleanup

```bash
# Remove stopped containers
docker compose rm

# Remove unused images
docker image prune

# Remove all unused resources
docker system prune -a
```

## .dockerignore

```dockerignore
# Git
.git
.gitignore

# Python
__pycache__
*.pyc
.venv/
*.egg-info/

# Testing
.pytest_cache/
.coverage
htmlcov/

# Development
.vscode/
.idea/

# Environment
.env
.env.local

# Documentation
docs/
*.md
!README.md
```

## Health Checks

### Application Health Check

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"
```

### Docker Compose Health Check

```yaml
services:
  app:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 3s
      retries: 3
      start_period: 10s
```

## Logging

### Configure Logging

```yaml
services:
  app:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### View Logs

```bash
# All logs
docker compose logs

# Specific service
docker compose logs app

# Follow logs
docker compose logs -f app

# Last 100 lines
docker compose logs --tail=100 app

# Since timestamp
docker compose logs --since="2024-01-01T00:00:00"
```

## Bundled Resources

### Assets
- **Dockerfile.template** - Multi-stage build template
- **docker-compose.yml.template** - Complete orchestration template
- **env.example.template** - Environment variables template
- **.dockerignore.template** - Standard ignore patterns

### References
- **dockerfile-patterns.md** - Common Dockerfile patterns
- **compose-patterns.md** - docker compose examples
- **security-practices.md** - Security guidelines

## Quick Reference

**Build**: `docker compose build`

**Start**: `docker compose up -d`

**Logs**: `docker compose logs -f app`

**Stop**: `docker compose down`

**Exec**: `docker compose exec app bash`

**Environment**: Use .env files, never commit secrets
