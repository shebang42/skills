---
name: python-dev
description: Python development with TDD and maintainability focus. Use for Python projects requiring test-driven development, OOP, SOLID principles, type safety, and high code quality. Includes pytest testing (80+ percent coverage), mypy type checking, ruff formatting, uv package management, and Pydantic validation. Creates well-structured Python projects with comprehensive testing.
---

# Python Development

Focused skill for Python development with test-driven development, type safety, and code quality.

## Core Principles

1. **Test-Driven Development** - Write tests first, then implementation
2. **Object-Oriented Programming** - Use OOP over procedural unless specified
3. **SOLID Principles** - Single responsibility, open/closed, Liskov substitution, interface segregation, dependency inversion
4. **Type Safety** - Complete type hints with mypy validation
5. **Immutability** - Prefer immutable data structures
6. **80+ percent Test Coverage** - Maintain high coverage with pytest and coverage.py
7. **Code Quality** - Enforce with ruff linting and formatting

## Quick Start

### New Project Structure

```
project-name/
├── src/package_name/
│   ├── __init__.py
│   ├── main.py
│   ├── models/         # Pydantic models
│   ├── services/       # Business logic
│   ├── repositories/   # Data access
│   └── utils/          # Utilities
├── tests/
│   ├── __init__.py
│   ├── test_models/
│   ├── test_services/
│   └── integration/
├── pyproject.toml
├── README.md
├── ARCHITECTURE.md
└── PLANNING.md
```

### Initialize Project

```bash
# Use bundled init script
python scripts/init_project.py my-project

# Or manually
mkdir -p my-project/src/my_package my-project/tests
cd my-project
uv init
uv sync --dev
```

## Test-Driven Development Workflow

**Strict TDD cycle for every feature:**

1. **Write test** - Define expected behavior in test
2. **Run test** - Verify it fails (red)
3. **Write code** - Minimal implementation
4. **Run test** - Verify it passes (green)
5. **Refactor** - Improve code quality
6. **Next task** - Only proceed after tests pass

### Example TDD Cycle

```python
# Step 1: Write failing test
def test_calculate_total_empty_cart_returns_zero() -> None:
    """Test that empty cart returns zero total."""
    cart = ShoppingCart()
    assert cart.calculate_total() == 0

# Step 2: Run test (fails - ShoppingCart doesn't exist)
# Step 3: Write minimal code
class ShoppingCart:
    def calculate_total(self) -> int:
        return 0

# Step 4: Run test (passes)
# Step 5: Refactor if needed
```

See [references/tdd-workflow.md](references/tdd-workflow.md) for detailed patterns.

## Code Implementation Patterns

### Models Layer (Pydantic)

```python
from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    """User domain model with validation."""
    
    id: int = Field(..., gt=0, description="User ID")
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    is_active: bool = Field(default=True)
    
    class Config:
        """Pydantic configuration."""
        frozen = True  # Immutability
```

### Services Layer (Business Logic)

```python
from typing import Protocol


class UserRepository(Protocol):
    """Repository interface for dependency injection."""
    
    def create(self, user: User) -> User: ...
    def find_by_email(self, email: str) -> User | None: ...


class UserService:
    """User business logic following SOLID principles."""
    
    def __init__(self, repository: UserRepository) -> None:
        """Initialize with injected repository dependency."""
        self._repository = repository
    
    def register_user(self, name: str, email: str) -> User:
        """Register new user with validation."""
        existing = self._repository.find_by_email(email)
        if existing:
            raise ValueError(f"User with email {email} already exists")
        
        user = User(id=0, name=name, email=email)
        return self._repository.create(user)
```

## Testing Patterns

### Unit Tests

```python
import pytest
from unittest.mock import Mock


class TestUserService:
    """Test suite for UserService."""
    
    def test_register_user_valid_data_returns_user(self) -> None:
        """Test successful user registration."""
        # Arrange
        mock_repo = Mock(spec=UserRepository)
        mock_repo.find_by_email.return_value = None
        service = UserService(mock_repo)
        
        # Act
        result = service.register_user("John Doe", "john@example.com")
        
        # Assert
        assert result.name == "John Doe"
        mock_repo.create.assert_called_once()
```

### Parametrized Tests

```python
@pytest.mark.parametrize("email,is_valid", [
    ("valid@example.com", True),
    ("invalid", False),
])
def test_email_validation(email: str, is_valid: bool) -> None:
    """Test email validation."""
    if is_valid:
        user = User(id=1, name="Test", email=email)
        assert user.email == email
    else:
        with pytest.raises(ValueError):
            User(id=1, name="Test", email=email)
```

See [references/testing-patterns.md](references/testing-patterns.md) for more examples.

## Tool Usage

### Package Management (uv)

```bash
uv sync              # Install dependencies
uv sync --dev        # Include dev dependencies
uv add pydantic      # Add dependency
uv run pytest        # Run in environment
```

### Testing (pytest)

```bash
uv run pytest                          # Run all tests
uv run pytest --cov=src                # With coverage
uv run pytest tests/test_module.py     # Specific file
```

### Code Quality

```bash
uv run ruff format .     # Format code
uv run ruff check .      # Lint code
uv run mypy src/         # Type check
```

### Complete Check

```bash
uv run ruff format . && uv run ruff check . && uv run mypy src/ && uv run pytest
```

## Configuration

See [references/pyproject-config.md](references/pyproject-config.md) for complete pyproject.toml template with:
- pytest configuration
- coverage.py settings (80 percent threshold)
- mypy strict checking
- ruff linting rules

## Documentation

Required files:
1. **README.md** - Project overview
2. **ARCHITECTURE.md** - Design decisions
3. **PLANNING.md** - Task breakdown

Templates in [references/documentation-templates.md](references/documentation-templates.md).

## Bundled Resources

### Scripts
- **init_project.py** - Initialize Python project structure

### References
- **tdd-workflow.md** - TDD patterns and workflow
- **testing-patterns.md** - pytest patterns, fixtures, mocking
- **pyproject-config.md** - Complete configuration
- **documentation-templates.md** - Doc templates

## Quick Reference

**TDD**: Test → Fail → Code → Pass → Refactor

**Quality**: `uv run ruff format . && uv run ruff check . && uv run mypy src/ && uv run pytest`

**Coverage**: 80+ percent target

**Python**: 3.13 required
