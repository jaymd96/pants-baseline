---
description: Run pytest with coverage analysis and failure debugging
user_invocable: true
triggers:
  - run tests
  - pytest
  - test python
  - baseline test
  - check coverage
arguments: "[targets] [pytest_args]"
---

# Baseline Test Skill

Run pytest with coverage tracking, failure analysis, and fix guidance.

## Workflow

### Step 1: Run Tests

Run the test suite:

```bash
pants baseline-test ${targets:-::}
```

Or with specific pytest arguments:
```bash
pants test --pytest-args="-v -x" ${targets:-tests/::}
```

### Step 2: Analyze Results

#### All Tests Pass

If tests pass:
1. Report test count and time
2. Show coverage summary
3. Check if coverage meets threshold (default 80%)

#### Tests Fail

If tests fail, analyze each failure:

1. **Assertion failures** - Expected vs actual mismatch
2. **Import errors** - Missing dependencies or modules
3. **Fixture errors** - Setup/teardown problems
4. **Timeout errors** - Tests running too long
5. **Collection errors** - Invalid test syntax

### Step 3: Debug Failures

For each failing test:

#### Read the Test File
```bash
# Read the failing test
cat tests/test_module.py
```

#### Understand the Failure
- What is the test checking?
- What was expected vs what happened?
- Is this a test bug or code bug?

#### Read Related Source Code
```bash
# Read the code being tested
cat src/module.py
```

### Step 4: Fix Strategies

#### Assertion Failures

```python
# Error: AssertionError: assert 42 == 43

# Option 1: Fix the code if it's wrong
def calculate() -> int:
    return 42  # Should be 43?

# Option 2: Fix the test if expectation is wrong
def test_calculate():
    assert calculate() == 42  # Not 43
```

#### Import Errors

```python
# Error: ModuleNotFoundError: No module named 'mylib'

# Check if dependency is installed
# Add to requirements.txt or pyproject.toml

# Or fix the import path
from src.mylib import something  # Correct path
```

#### Fixture Errors

```python
# Error: fixture 'db' not found

# Ensure fixture is defined in conftest.py
@pytest.fixture
def db():
    return create_test_db()
```

### Step 5: Re-run Specific Tests

After fixing, re-run just the failing tests:

```bash
pants test --pytest-args="-v tests/test_module.py::test_specific"
```

### Step 6: Check Coverage

If coverage is below threshold:

```bash
pants test --pytest-args="--cov-report=term-missing" tests/::
```

This shows which lines are not covered. Then:
1. Identify uncovered code paths
2. Write tests for missing coverage
3. Or mark intentionally uncovered code with `# pragma: no cover`

## Coverage Improvement

### Find Uncovered Lines

```bash
pants test --pytest-args="--cov-report=html" tests/::
# Open htmlcov/index.html in browser
```

### Common Uncovered Patterns

| Pattern | Solution |
|---------|----------|
| Error handlers | Test with mocked errors |
| Edge cases | Add parameterized tests |
| `if __name__ == "__main__"` | Mark as `# pragma: no cover` |
| Optional branches | Test both paths |

### Writing Missing Tests

```python
# For uncovered function
def risky_operation() -> bool:
    # uncovered code here
    pass

# Add test
def test_risky_operation():
    result = risky_operation()
    assert result is True
```

## Error Recovery

### "No tests found"

Check that:
1. Test files match pattern `test_*.py` or `*_test.py`
2. Test functions start with `test_`
3. Tests are in directories with `__init__.py`

### Fixture scope issues

If fixtures aren't sharing state correctly:
```python
@pytest.fixture(scope="module")  # or "session"
def expensive_setup():
    return create_expensive_resource()
```

### Slow tests

For slow tests:
1. Use `@pytest.mark.slow` and skip in quick runs
2. Mock expensive operations
3. Use smaller test data

```bash
pants test --pytest-args="-m 'not slow'" tests/::
```

## Best Practices

1. **Test one thing per test** - Clear, focused assertions
2. **Use descriptive names** - `test_user_login_with_invalid_password_fails`
3. **Arrange-Act-Assert** - Clear test structure
4. **Mock external dependencies** - Isolate unit tests
5. **Use fixtures for setup** - Avoid repetition
