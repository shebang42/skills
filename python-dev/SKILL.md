---
name: python-dev
description: Python development with maintainable code practices. Use when creating or modifying Python projects, implementing features with TDD, or working with Python codebases. Enforces OOP, SOLID principles, type hints, pytest testing (80+ percent coverage), uv package management, ruff formatting, mypy type checking, gitflow workflow, Docker deployment, and Pydantic validation. Creates structured projects with proper documentation.
---

# Python Development

Comprehensive Python development skill for creating maintainable, well-tested Python applications following best practices and SOLID principles.

## Core Principles

Follow these principles for all Python development:

1. **Test-Driven Development (TDD)** - Write tests first, then implementation
2. **Object-Oriented Programming** - Use OOP over procedural unless specified
3. **SOLID Principles** - Design for maintainability and extensibility
4. **Type Safety** - Use type hints throughout codebase
5. **Immutability** - Prefer immutable data structures
6. **High Test Coverage** - Maintain >80% code coverage
7. **Code Quality** - Use ruff for linting/formatting, mypy for type checking

## Project Setup

### Configure Gitea Credentials (First Time Only)

Before using automatic repository creation, set up your Gitea credentials:

```bash
# Copy template to config directory
mkdir -p ~/.config/python-dev
cp assets/config.template ~/.config/python-dev/config

# Edit with your credentials
nano ~/.config/python-dev/config

# Secure the file
chmod 600 ~/.config/python-dev/config
```

See [references/configuration.md](references/configuration.md) for detailed setup instructions.

### Initialize New Project

Use the bundled initialization script for new projects:

```bash
python scripts/init_project.py project-name --path /path/to/parent
```

This creates a complete project structure with:
- Standard directory layout (src/, tests/, docs/)
- Configured pyproject.toml with all tools
- Git repository with gitflow branches
- Gitea remote repository setup
- Initial commit on develop branch
- Example test file and main entry point

### Manual Project Structure

If not using the init script, create this structure:

```
project-name/
├── src/package_name/           # Source code
│   ├── models/                 # Domain models (Pydantic)
│   ├── services/               # Business logic
│   ├── repositories/           # Data access
│   ├── api/                    # API routes
│   └── utils/                  # Utilities
├── tests/                      # Test files
│   ├── test_models/
│   ├── test_services/
│   └── integration/
├── pyproject.toml              # Project config
├── README.md
├── ARCHITECTURE.md
├── API.md                      # For APIs/web services
├── PLANNING.md                 # Task breakdown
├── Dockerfile
└── docker-compose.yml
```

See [references/project-structure.md](references/project-structure.md) for detailed structure guidance and templates.

## Development Workflow

### 1. Planning and Task Breakdown

Before coding, create or update `PLANNING.md` with task breakdown:

```markdown
## Task Breakdown

### Feature: User Authentication
- [ ] Create User model with validation
- [ ] Implement UserRepository for data access
- [ ] Create UserService with business logic
- [ ] Add authentication API endpoints
- [ ] Write unit tests for all components
- [ ] Write integration tests for API
- [ ] Update documentation
```

### 2. Test-Driven Development

**Strict TDD cycle for every feature:**

1. **Write failing test** - Define expected behavior
2. **Run test** - Verify it fails (red phase)
3. **Write minimal code** - Make test pass
4. **Run test** - Verify it passes (green phase)
5. **Refactor** - Improve code quality
6. **Mark task complete** - Update PLANNING.md

**Only move to next task after all tests pass.**

See [references/testing.md](references/testing.md) for comprehensive testing patterns.

### 3. Code Implementation

Follow these patterns:

#### Models Layer (Pydantic)

```python
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

#### Services Layer (Business Logic)

```python
from typing import Protocol

class UserRepository(Protocol):
    """Repository interface for dependency injection."""
    def create(self, user: User) -> User: ...

class UserService:
    """User business logic following SOLID principles."""
    
    def __init__(self, repository: UserRepository) -> None:
        """Inject repository dependency."""
        self._repository = repository
    
    def register_user(self, name: str, email: str) -> User:
        """Register new user with validation."""
        user = User(id=0, name=name, email=email)
        return self._repository.create(user)
```

#### Repositories Layer (Data Access)

```python
class UserRepository:
    """User data access implementation."""
    
    def create(self, user: User) -> User:
        """Persist user to database."""
        # Implementation
        pass
```

### 4. Code Quality Checks

Run after each implementation:

```bash
# Format code
uv run ruff format .

# Lint code
uv run ruff check .

# Type check
uv run mypy src/

# Run tests with coverage
uv run pytest

# Run all checks
uv run ruff format . && uv run ruff check . && uv run mypy src/ && uv run pytest
```

### 5. Git Workflow

Follow gitflow workflow with Gitea:

```bash
# Start feature from develop
git checkout develop
git pull origin develop
git checkout -b feature/feature-name

# Commit with conventional format
git commit -m "feat(module): add feature description"

# Push and create PR
git push -u origin feature/feature-name
```

See [references/git-workflow.md](references/git-workflow.md) for complete gitflow process.

## Tool Configuration

### Python Version

Use Python 3.13 for all projects.

### Package Management (uv)

```bash
# Install dependencies
uv sync

# Install with dev dependencies
uv sync --dev

# Add new dependency
uv add package-name

# Add dev dependency
uv add --dev package-name

# Update dependencies
uv sync --upgrade
```

### Testing (pytest + coverage.py)

```bash
# Run all tests
uv run pytest

# Run with coverage report
uv run pytest --cov=src --cov-report=html --cov-report=term

# Run specific test file
uv run pytest tests/test_module.py

# Run with verbose output
uv run pytest -v
```

**Coverage requirement: >80%**

### Linting and Formatting (ruff)

```bash
# Format code (auto-fix)
uv run ruff format .

# Check linting issues
uv run ruff check .

# Fix linting issues automatically
uv run ruff check --fix .
```

### Type Checking (mypy)

```bash
# Type check source code
uv run mypy src/

# Type check with verbose output
uv run mypy src/ --show-error-codes
```

## Testing Patterns

### Unit Test Structure

```python
class TestUserService:
    """Test suite for UserService."""
    
    def test_register_user_valid_data_returns_user(self) -> None:
        """Test user registration with valid data."""
        # Arrange
        mock_repo = Mock(spec=UserRepository)
        service = UserService(mock_repo)
        
        # Act
        result = service.register_user("John Doe", "john@example.com")
        
        # Assert
        assert result.name == "John Doe"
        mock_repo.create.assert_called_once()
```

### Parametrized Tests

```python
@pytest.mark.parametrize("email,expected", [
    ("valid@example.com", True),
    ("invalid", False),
    ("", False),
])
def test_email_validation(email: str, expected: bool) -> None:
    """Test email validation with multiple inputs."""
    result = is_valid_email(email)
    assert result == expected
```

For more patterns, see [references/testing.md](references/testing.md).

## Deployment

### Docker Setup

Use provided templates in `assets/` directory:

```bash
# Copy templates
cp assets/Dockerfile.template Dockerfile
cp assets/docker-compose.yml.template docker-compose.yml
cp assets/env.example.template .env.example

# Customize for your project
# Edit package_name and project-specific settings
```

### Docker Commands

```bash
# Build and start services
docker compose up -d

# View logs
docker compose logs -f app

# Run tests in container
docker compose exec app uv run pytest

# Stop services
docker compose down
```

See [references/deployment.md](references/deployment.md) for complete deployment guide.

## Documentation Requirements

Every project must include:

1. **README.md** - Project overview, installation, usage
2. **ARCHITECTURE.md** - System design, patterns, data flow
3. **API.md** - API endpoints (for web services)
4. **PLANNING.md** - Task breakdown with checkboxes

Templates available in [references/project-structure.md](references/project-structure.md).

## Security Best Practices

1. **Never commit secrets** - Use .env files, add to .gitignore
2. **Validate all inputs** - Use Pydantic models
3. **Use type hints** - Catch errors early with mypy
4. **Principle of least privilege** - Run containers as non-root
5. **Keep dependencies updated** - Regular security updates

## Bundled Resources

### Scripts

- **init_project.py** - Initialize new Python project with complete structure and configuration. Reads Gitea credentials from config file or environment variables (never hardcoded).

### References

- **testing.md** - Comprehensive testing guide with pytest, coverage, TDD workflow
- **git-workflow.md** - Gitflow workflow, Gitea setup, commit conventions
- **project-structure.md** - Standard project layout, templates for README/ARCHITECTURE/API docs
- **deployment.md** - Docker containerization, docker compose, environment configuration
- **configuration.md** - Security-focused guide for setting up Gitea credentials

### Assets

- **Dockerfile.template** - Multi-stage Docker build template
- **docker-compose.yml.template** - Complete docker compose configuration with PostgreSQL
- **env.example.template** - Environment variables template
- **config.template** - Gitea credentials template (never includes actual secrets)

## Quick Reference

### Start New Project

```bash
# Initialize project (recommended)
python scripts/init_project.py my-project

# Or manually create structure
mkdir -p my-project/src/my_package my-project/tests
cd my-project
uv init
uv sync --dev
```

### TDD Cycle

1. Write test → 2. Run (fail) → 3. Write code → 4. Run (pass) → 5. Refactor

### Code Quality

```bash
uv run ruff format . && uv run ruff check . && uv run mypy src/ && uv run pytest
```

### Git Flow

```bash
feature/name → develop → release/v1.0.0 → main (tagged)
```

### Deploy

```bash
docker compose up -d
```
