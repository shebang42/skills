# Docker Security Practices

## 1. Use Minimal Base Images

```dockerfile
# Good - slim variant
FROM python:3.13-slim

# Avoid - full image (larger attack surface)
FROM python:3.13
```

## 2. Run as Non-Root User

```dockerfile
# Create and use non-root user
RUN useradd --create-home --shell /bin/bash appuser
USER appuser
```

## 3. Multi-Stage Builds

Separate build dependencies from runtime:

```dockerfile
FROM python:3.13-slim as builder
# Build dependencies here

FROM python:3.13-slim
# Copy only what's needed
COPY --from=builder /app/.venv /app/.venv
```

## 4. Pin Versions

```dockerfile
# Pin base image version
FROM python:3.13.1-slim

# Pin dependency versions in requirements
# pydantic==2.9.1 (not pydantic>=2.9.0)
```

## 5. Scan for Vulnerabilities

```bash
# Scan image
docker scan my-image:latest

# Use trivy
trivy image my-image:latest
```

## 6. Environment Variables

```yaml
# Use env_file for secrets
services:
  app:
    env_file:
      - .env  # Never commit this file
```

```bash
# .env file
SECRET_KEY=your-secret-here
API_KEY=your-api-key
```

## 7. Network Isolation

```yaml
services:
  app:
    networks:
      - frontend
      - backend
  
  db:
    networks:
      - backend  # Not exposed to frontend
```

## 8. Read-Only Filesystem

```yaml
services:
  app:
    read_only: true
    tmpfs:
      - /tmp
```

## 9. Drop Capabilities

```yaml
services:
  app:
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE  # Only if needed
```

## 10. Resource Limits

```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
```

## Checklist

- [ ] Use slim base images
- [ ] Run as non-root user
- [ ] Multi-stage builds
- [ ] Pin all versions
- [ ] Scan for vulnerabilities
- [ ] Use .env for secrets (never commit)
- [ ] Network isolation
- [ ] Health checks
- [ ] Resource limits
- [ ] Minimal attack surface
