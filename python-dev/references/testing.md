# Testing Guide

## Test-Driven Development (TDD) Workflow

Follow this strict TDD cycle for all features:

1. **Write the test first** - Create a failing test that defines the desired behavior
2. **Run the test** - Verify it fails (red phase)
3. **Write minimal code** - Implement just enough to make the test pass
4. **Run the test again** - Verify it passes (green phase)
5. **Refactor** - Improve code quality while keeping tests green
6. **Move to next step** - Only proceed after all tests pass

## Test Structure with pytest

### Basic Test Organization

```python
# tests/test_module_name.py
import pytest
from src.module_name import ClassName


class TestClassName:
    """Test suite for ClassName."""
    
    def test_method_behavior_expected_result(self) -> None:
        """Test that method produces expected result given specific input."""
        # Arrange
        instance = ClassName(param="value")
        
        # Act
        result = instance.method()
        
        # Assert
        assert result == expected_value
```

### Parametrized Tests

```python
@pytest.mark.parametrize("input_val,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_multiply_by_two(input_val: int, expected: int) -> None:
    """Test multiplication with multiple inputs."""
    assert multiply_by_two(input_val) == expected
```

### Fixtures

```python
@pytest.fixture
def sample_data() -> dict[str, Any]:
    """Provide sample data for tests."""
    return {"key": "value", "count": 42}


def test_with_fixture(sample_data: dict[str, Any]) -> None:
    """Test using fixture data."""
    assert sample_data["count"] == 42
```

### Exception Testing

```python
def test_raises_value_error() -> None:
    """Test that function raises ValueError for invalid input."""
    with pytest.raises(ValueError, match="Invalid input"):
        function_that_raises("invalid")
```

## Test Coverage with coverage.py

### Running Tests with Coverage

```bash
# Run tests with coverage
uv run pytest --cov=src --cov-report=html --cov-report=term

# View coverage report
open htmlcov/index.html
```

### Coverage Requirements

- **Minimum threshold**: 80% coverage
- **Focus areas**: Business logic, data validation, error handling
- **Acceptable gaps**: Simple getters/setters, __repr__ methods

### Configuration in pyproject.toml

```toml
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
```

## Test Organization Patterns

### Directory Structure

```
project/
├── src/
│   └── package/
│       ├── __init__.py
│       ├── module.py
│       └── subpackage/
│           ├── __init__.py
│           └── another_module.py
└── tests/
    ├── __init__.py
    ├── test_module.py
    └── subpackage/
        ├── __init__.py
        └── test_another_module.py
```

### Test Naming Conventions

- Test files: `test_<module_name>.py`
- Test classes: `Test<ClassName>`
- Test methods: `test_<method>_<condition>_<expected_result>`

Examples:
- `test_validate_email_invalid_format_raises_error`
- `test_calculate_total_empty_cart_returns_zero`
- `test_process_data_valid_input_returns_dict`

## Integration Testing

```python
# tests/integration/test_workflow.py
import pytest
from src.service import ServiceClass
from src.repository import RepositoryClass


class TestServiceIntegration:
    """Integration tests for service layer."""
    
    @pytest.fixture
    def service(self) -> ServiceClass:
        """Create service with real dependencies."""
        repo = RepositoryClass()
        return ServiceClass(repo)
    
    def test_complete_workflow(self, service: ServiceClass) -> None:
        """Test end-to-end workflow."""
        # Test multiple components working together
        result = service.process_complete_workflow(data)
        assert result.status == "completed"
```

## Mocking with pytest

```python
from unittest.mock import Mock, patch


def test_with_mock() -> None:
    """Test using mock objects."""
    mock_dependency = Mock()
    mock_dependency.get_data.return_value = {"result": 42}
    
    service = ServiceClass(mock_dependency)
    result = service.process()
    
    mock_dependency.get_data.assert_called_once()
    assert result == 42


@patch('src.module.external_api_call')
def test_with_patch(mock_api: Mock) -> None:
    """Test with patched external dependency."""
    mock_api.return_value = "mocked response"
    result = function_using_api()
    assert result == "processed: mocked response"
```

## Best Practices

1. **One assertion per test** - Each test should verify one specific behavior
2. **Descriptive names** - Test names should clearly state what they test
3. **Arrange-Act-Assert** - Structure tests with clear phases
4. **Independent tests** - Tests should not depend on each other
5. **Fast tests** - Keep unit tests fast; use integration tests for slower operations
6. **Test edge cases** - Include boundary conditions, empty inputs, None values
7. **Type hints** - Use type hints in all test code
8. **Docstrings** - Add docstrings to test classes and complex test methods
