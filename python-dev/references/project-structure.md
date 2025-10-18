# Project Structure Guide

## Standard Python Project Layout

```
project-name/
├── .git/
├── .github/                    # Optional: GitHub workflows (if using GitHub)
├── .gitignore
├── .env.example                # Template for environment variables
├── .dockerignore
├── pyproject.toml              # Project metadata and dependencies
├── uv.lock                     # Locked dependencies (auto-generated)
├── README.md
├── ARCHITECTURE.md
├── API.md                      # For web services/APIs
├── PLANNING.md                 # Task breakdown and progress tracking
├── Dockerfile
├── docker-compose.yml
├── src/
│   └── package_name/
│       ├── __init__.py
│       ├── main.py
│       ├── models/
│       │   ├── __init__.py
│       │   └── user.py
│       ├── services/
│       │   ├── __init__.py
│       │   └── user_service.py
│       ├── repositories/
│       │   ├── __init__.py
│       │   └── user_repository.py
│       ├── api/
│       │   ├── __init__.py
│       │   └── routes.py
│       └── utils/
│           ├── __init__.py
│           └── validators.py
├── tests/
│   ├── __init__.py
│   ├── test_models/
│   │   ├── __init__.py
│   │   └── test_user.py
│   ├── test_services/
│   │   ├── __init__.py
│   │   └── test_user_service.py
│   └── integration/
│       ├── __init__.py
│       └── test_api.py
├── scripts/
│   └── setup.sh
└── docs/
    └── api/
        └── openapi.yaml
```

## pyproject.toml Configuration

```toml
[project]
name = "project-name"
version = "0.1.0"
description = "Project description"
readme = "README.md"
requires-python = ">=3.13"
authors = [
    { name = "Your Name", email = "your.email@example.com" }
]
dependencies = [
    "pydantic>=2.9.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.3.0",
    "pytest-cov>=5.0.0",
    "mypy>=1.11.0",
    "ruff>=0.6.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--strict-markers",
    "--strict-config",
    "--cov=src",
    "--cov-report=html",
    "--cov-report=term-missing",
]

[tool.coverage.run]
source = ["src"]
omit = ["*/tests/*", "*/test_*.py"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if TYPE_CHECKING:",
    "if __name__ == .__main__.:",
]
fail_under = 80

[tool.mypy]
python_version = "3.13"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_any_generics = true
check_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
follow_imports = "normal"
ignore_missing_imports = false

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false

[tool.ruff]
target-version = "py313"
line-length = 100

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # pyflakes
    "I",    # isort
    "B",    # flake8-bugbear
    "C4",   # flake8-comprehensions
    "UP",   # pyupgrade
    "ARG",  # flake8-unused-arguments
    "SIM",  # flake8-simplify
]
ignore = [
    "E501",  # line too long (handled by formatter)
    "B008",  # do not perform function calls in argument defaults
]

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401"]  # Allow unused imports in __init__.py
"tests/**/*" = ["ARG"]     # Allow unused arguments in tests

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

## README.md Template

```markdown
# Project Name

Brief description of the project.

## Features

- Feature 1
- Feature 2
- Feature 3

## Requirements

- Python 3.13+
- Docker (for containerized deployment)

## Installation

### Using uv (recommended)

\`\`\`bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone repository
git clone https://git.home:3443/paul/project-name.git
cd project-name

# Create virtual environment and install dependencies
uv sync

# Copy environment template
cp .env.example .env
# Edit .env with your configuration
\`\`\`

### Using Docker

\`\`\`bash
# Build and run with docker compose
docker compose up -d
\`\`\`

## Development

### Setup Development Environment

\`\`\`bash
# Install with development dependencies
uv sync --dev

# Activate virtual environment
source .venv/bin/activate
\`\`\`

### Running Tests

\`\`\`bash
# Run all tests with coverage
uv run pytest

# Run specific test file
uv run pytest tests/test_module.py

# Run with verbose output
uv run pytest -v
\`\`\`

### Code Quality

\`\`\`bash
# Format code
uv run ruff format .

# Lint code
uv run ruff check .

# Type checking
uv run mypy src/

# Run all checks
uv run ruff format . && uv run ruff check . && uv run mypy src/ && uv run pytest
\`\`\`

## Project Structure

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architecture documentation.

## API Documentation

See [API.md](API.md) for API endpoint documentation.

## Contributing

1. Create a feature branch from `develop`
2. Make your changes
3. Ensure all tests pass
4. Submit a pull request

## License

[License type]
```

## ARCHITECTURE.md Template

```markdown
# Architecture

## Overview

High-level description of the system architecture and design decisions.

## Directory Structure

\`\`\`
src/package_name/
├── models/         # Domain models and data structures
├── services/       # Business logic layer
├── repositories/   # Data access layer
├── api/            # API routes and controllers
└── utils/          # Utility functions and helpers
\`\`\`

## Design Patterns

### Dependency Injection

[Explain how DI is implemented]

### Repository Pattern

[Explain repository pattern usage]

### Service Layer

[Explain service layer design]

## Data Flow

\`\`\`
Client Request
    ↓
API Routes
    ↓
Services (Business Logic)
    ↓
Repositories (Data Access)
    ↓
Database/External Services
\`\`\`

## Key Components

### Models

Domain entities with validation using Pydantic.

### Services

Business logic implementation following SOLID principles.

### Repositories

Abstract data access to allow for testing and flexibility.

## Testing Strategy

- Unit tests for models and services
- Integration tests for repositories and API
- 80%+ code coverage requirement

## Security Considerations

- Input validation with Pydantic
- Environment-based configuration
- No secrets in code

## Performance Considerations

[Document any performance-related decisions]

## Future Improvements

- [ ] Item 1
- [ ] Item 2
```

## API.md Template (for web services)

```markdown
# API Documentation

## Base URL

\`\`\`
http://localhost:8000
\`\`\`

## Authentication

[Describe authentication mechanism]

## Endpoints

### GET /api/users

Retrieve list of users.

**Query Parameters:**
- `limit` (integer, optional): Maximum number of results (default: 10)
- `offset` (integer, optional): Number of results to skip (default: 0)

**Response:**
\`\`\`json
{
  "users": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com"
    }
  ],
  "total": 100
}
\`\`\`

### POST /api/users

Create a new user.

**Request Body:**
\`\`\`json
{
  "name": "Jane Doe",
  "email": "jane@example.com"
}
\`\`\`

**Response:**
\`\`\`json
{
  "id": 2,
  "name": "Jane Doe",
  "email": "jane@example.com"
}
\`\`\`

**Status Codes:**
- `201`: User created successfully
- `400`: Invalid request data
- `409`: User already exists

## Error Responses

All errors follow this format:

\`\`\`json
{
  "error": "Error message",
  "details": "Additional error details"
}
\`\`\`
```

## PLANNING.md Template

```markdown
# Project Planning

## Task Breakdown

### Phase 1: Setup
- [x] Initialize project structure
- [x] Configure dependencies
- [ ] Set up Docker environment
- [ ] Create initial documentation

### Phase 2: Core Features
- [ ] Implement user model
- [ ] Create user service
- [ ] Add user repository
- [ ] Implement user API endpoints

### Phase 3: Testing
- [ ] Unit tests for models
- [ ] Unit tests for services
- [ ] Integration tests for API
- [ ] Achieve 80%+ coverage

### Phase 4: Deployment
- [ ] Create Dockerfile
- [ ] Configure docker compose
- [ ] Set up CI/CD
- [ ] Deploy to production

## Current Status

Working on: [Current task]
Blocked by: [Any blockers]
Next up: [Next task]
```

## Package Organization

### Models Layer (`models/`)

Domain entities with Pydantic validation:

```python
# src/package_name/models/user.py
from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    """User domain model."""
    
    id: int = Field(..., gt=0)
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    
    class Config:
        """Pydantic configuration."""
        frozen = True  # Immutability
```

### Services Layer (`services/`)

Business logic with SOLID principles:

```python
# src/package_name/services/user_service.py
from typing import Protocol

from ..models.user import User


class UserRepository(Protocol):
    """User repository interface."""
    
    def create(self, user: User) -> User: ...
    def get_by_id(self, user_id: int) -> User | None: ...


class UserService:
    """User business logic."""
    
    def __init__(self, repository: UserRepository) -> None:
        """Initialize service with repository dependency."""
        self._repository = repository
    
    def register_user(self, name: str, email: str) -> User:
        """Register a new user."""
        user = User(id=0, name=name, email=email)
        return self._repository.create(user)
```

### Repositories Layer (`repositories/`)

Data access abstraction:

```python
# src/package_name/repositories/user_repository.py
from ..models.user import User


class UserRepository:
    """User data access."""
    
    def create(self, user: User) -> User:
        """Create user in database."""
        # Implementation
        pass
    
    def get_by_id(self, user_id: int) -> User | None:
        """Retrieve user by ID."""
        # Implementation
        pass
```
