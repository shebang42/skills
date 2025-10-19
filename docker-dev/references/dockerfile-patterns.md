# Dockerfile Patterns

## Multi-Stage Build

Minimize final image size by separating build and runtime:

```dockerfile
# Build stage
FROM python:3.13-slim as builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Production stage
FROM python:3.13-slim
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY src/ /app/src/
ENV PATH="/app/.venv/bin:$PATH"
CMD ["python", "-m", "package_name"]
```

## Non-Root User

Always run as non-root for security:

```dockerfile
FROM python:3.13-slim

# Create user
RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app
COPY --chown=appuser:appuser src/ /app/src/

# Switch to non-root
USER appuser

CMD ["python", "-m", "package_name"]
```

## Development vs Production

```dockerfile
# Base stage
FROM python:3.13-slim as base
WORKDIR /app

# Development stage
FROM base as development
RUN apt-get update && apt-get install -y git
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
RUN uv sync --dev

# Production stage
FROM base as production
COPY --from=development /app/.venv /app/.venv
COPY src/ /app/src/
RUN useradd appuser && chown -R appuser:appuser /app
USER appuser
```

## Layer Optimization

Combine commands to reduce layers:

```dockerfile
# Bad - Multiple layers
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get clean

# Good - Single layer
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

## Cache Optimization

Copy dependency files first for better caching:

```dockerfile
# Copy dependency files first
COPY pyproject.toml uv.lock ./

# Install dependencies (cached if unchanged)
RUN uv sync

# Copy source code (changes frequently)
COPY src/ /app/src/
```
