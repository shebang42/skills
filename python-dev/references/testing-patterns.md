# Testing Patterns

## Test Structure (Arrange-Act-Assert)

```python
def test_user_registration_success() -> None:
    """Test successful user registration."""
    # Arrange - Set up test data and dependencies
    repository = InMemoryUserRepository()
    service = UserService(repository)
    
    # Act - Execute the behavior being tested
    user = service.register("John Doe", "john@example.com")
    
    # Assert - Verify the outcome
    assert user.name == "John Doe"
    assert user.email == "john@example.com"
```

## Fixtures

```python
import pytest


@pytest.fixture
def user_repository() -> InMemoryUserRepository:
    """Provide clean repository for each test."""
    return InMemoryUserRepository()


@pytest.fixture
def user_service(user_repository: InMemoryUserRepository) -> UserService:
    """Provide service with injected repository."""
    return UserService(user_repository)


def test_with_fixtures(user_service: UserService) -> None:
    """Test using fixtures."""
    user = user_service.register("Test", "test@example.com")
    assert user.id > 0
```

## Parametrized Tests

```python
@pytest.mark.parametrize("input_value,expected", [
    (0, 0),
    (1, 2),
    (5, 10),
    (10, 20),
])
def test_double(input_value: int, expected: int) -> None:
    """Test doubling with multiple inputs."""
    assert double(input_value) == expected


@pytest.mark.parametrize("email", [
    "invalid",
    "@example.com",
    "user@",
    "",
])
def test_invalid_emails(email: str) -> None:
    """Test that invalid emails raise errors."""
    with pytest.raises(ValueError):
        User(id=1, name="Test", email=email)
```

## Mocking

```python
from unittest.mock import Mock, patch


def test_with_mock() -> None:
    """Test using mock repository."""
    # Create mock
    mock_repo = Mock(spec=UserRepository)
    mock_repo.find_by_email.return_value = None
    
    # Use mock
    service = UserService(mock_repo)
    service.register("Test", "test@example.com")
    
    # Verify mock was called
    mock_repo.create.assert_called_once()
    mock_repo.find_by_email.assert_called_with("test@example.com")


@patch('package.module.external_api')
def test_with_patch(mock_api: Mock) -> None:
    """Test with patched external dependency."""
    mock_api.return_value = {"status": "success"}
    result = function_using_api()
    assert result == "success"
```

## Exception Testing

```python
def test_duplicate_user_raises_error() -> None:
    """Test that duplicate registration raises error."""
    repository = InMemoryUserRepository()
    service = UserService(repository)
    
    service.register("Test", "test@example.com")
    
    with pytest.raises(ValueError, match="already exists"):
        service.register("Test2", "test@example.com")
```

## Integration Tests

```python
class TestUserWorkflow:
    """Integration tests for complete user workflow."""
    
    def test_complete_user_lifecycle(self) -> None:
        """Test creating, finding, and updating user."""
        # Setup real dependencies
        repository = DatabaseUserRepository()
        service = UserService(repository)
        
        # Create user
        user = service.register("Test", "test@example.com")
        assert user.id > 0
        
        # Find user
        found = repository.find_by_id(user.id)
        assert found is not None
        assert found.email == "test@example.com"
```

## Test Naming

Use descriptive names that explain:
- What is being tested
- Under what conditions
- What the expected result is

**Pattern**: `test_<method>_<condition>_<expected_result>`

**Examples**:
- `test_register_valid_data_creates_user`
- `test_register_duplicate_email_raises_error`
- `test_calculate_total_empty_cart_returns_zero`
- `test_find_nonexistent_user_returns_none`
