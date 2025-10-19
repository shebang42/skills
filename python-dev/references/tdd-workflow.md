# Test-Driven Development Workflow

## TDD Cycle

Follow this strict cycle for every feature:

1. **Write Failing Test** - Define expected behavior
2. **Run Test** - Verify it fails (Red phase)
3. **Write Minimal Code** - Just enough to pass
4. **Run Test** - Verify it passes (Green phase)
5. **Refactor** - Improve code quality
6. **Move to Next** - Only after tests pass

## Example: Shopping Cart

### Iteration 1: Empty Cart

```python
# Step 1: Write test
def test_empty_cart_has_zero_total() -> None:
    """Test empty cart returns zero."""
    cart = ShoppingCart()
    assert cart.total() == 0

# Step 2: Run (fails - ShoppingCart doesn't exist)

# Step 3: Write code
class ShoppingCart:
    def total(self) -> int:
        return 0

# Step 4: Run (passes)
# Step 5: Refactor (not needed)
```

### Iteration 2: Add Item

```python
# Step 1: Write test
def test_add_item_updates_total() -> None:
    """Test adding item updates total."""
    cart = ShoppingCart()
    cart.add_item(price=100)
    assert cart.total() == 100

# Step 2: Run (fails - add_item doesn't exist)

# Step 3: Write code
class ShoppingCart:
    def __init__(self) -> None:
        self._total = 0
    
    def add_item(self, price: int) -> None:
        self._total += price
    
    def total(self) -> int:
        return self._total

# Step 4: Run (passes)
# Step 5: Refactor
class ShoppingCart:
    def __init__(self) -> None:
        self._items: list[int] = []
    
    def add_item(self, price: int) -> None:
        self._items.append(price)
    
    def total(self) -> int:
        return sum(self._items)
```

## Best Practices

1. **One test at a time** - Don't write multiple failing tests
2. **Minimal implementation** - Write least code to pass
3. **Refactor with confidence** - Tests protect against regression
4. **Test behavior, not implementation** - Test what, not how
5. **Keep tests independent** - Tests shouldn't depend on each other
6. **Fast feedback** - Keep tests fast to run frequently
