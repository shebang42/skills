# Documentation Templates

## README.md

```markdown
# Project Name

Brief description of what this project does.

## Features

- Feature 1
- Feature 2
- Feature 3

## Requirements

- Python 3.13+

## Installation

```bash
# Clone repository
git clone <repository-url>
cd project-name

# Install dependencies with uv
uv sync

# Copy environment template
cp .env.example .env
```

## Usage

```bash
# Run application
uv run python -m package_name

# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov=src
```

## Development

```bash
# Install development dependencies
uv sync --dev

# Format code
uv run ruff format .

# Lint code
uv run ruff check .

# Type check
uv run mypy src/

# Run all checks
uv run ruff format . && uv run ruff check . && uv run mypy src/ && uv run pytest
```

## Project Structure

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed documentation.

## License

[Your license]
```

## ARCHITECTURE.md

```markdown
# Architecture

## Overview

High-level description of the system architecture and design decisions.

## Directory Structure

```
src/package_name/
├── models/         # Domain models (Pydantic)
├── services/       # Business logic
├── repositories/   # Data access
└── utils/          # Utilities
```

## Design Patterns

### Dependency Injection

Services receive dependencies through constructor injection, enabling testability and flexibility.

### Repository Pattern

Data access is abstracted behind repository interfaces, allowing different implementations (in-memory, database, etc.).

### Service Layer

Business logic is isolated in service classes following SOLID principles.

## Data Flow

```
Input → Service Layer → Repository Layer → Data Store
```

## Key Components

### Models (src/package_name/models/)

Domain entities with Pydantic validation.

### Services (src/package_name/services/)

Business logic implementation.

### Repositories (src/package_name/repositories/)

Data access abstraction.

## Testing Strategy

- Unit tests for services and models
- Integration tests for complete workflows
- 80+ percent code coverage requirement

## Future Improvements

- [ ] Improvement 1
- [ ] Improvement 2
```

## PLANNING.md

```markdown
# Project Planning

## Current Sprint

### In Progress
- [ ] Feature X implementation
- [ ] Unit tests for feature X

### Blocked
- [ ] Feature Y (waiting on external dependency)

## Task Breakdown

### Phase 1: Core Features
- [x] Project setup
- [x] Basic models
- [ ] User authentication
  - [ ] Create User model
  - [ ] Write User model tests
  - [ ] Implement UserService
  - [ ] Write UserService tests
  - [ ] Create UserRepository
  - [ ] Write integration tests

### Phase 2: API Layer
- [ ] REST API endpoints
- [ ] API documentation
- [ ] Authentication middleware

### Phase 3: Testing
- [ ] Achieve 80+ percent coverage
- [ ] Integration tests
- [ ] Performance tests

## Next Steps

1. Complete user authentication
2. Begin API layer
3. Write documentation
```
