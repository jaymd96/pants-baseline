---
description: Run ty type checking with error analysis and fix guidance
user_invocable: true
triggers:
  - type check
  - typecheck
  - check types
  - ty check
  - baseline typecheck
arguments: "[targets]"
---

# Baseline Type Check Skill

Run ty type checking on Python code with intelligent error analysis and fix guidance.

## Workflow

### Step 1: Run Type Check

Run the type checker:

```bash
pants baseline-typecheck ${targets:-::}
```

### Step 2: Analyze Type Errors

If type checking fails, categorize errors:

1. **Missing type annotations** - Functions/variables need types
2. **Type mismatches** - Incompatible types assigned/returned
3. **Missing imports** - Type stubs not available
4. **Optional handling** - None checks missing
5. **Generic type issues** - Type parameters incorrect

### Step 3: Fix Common Issues

#### Missing Return Type

Error: `Function is missing a return type annotation`

Fix by adding return type:
```python
# Before
def get_name():
    return "hello"

# After
def get_name() -> str:
    return "hello"
```

#### Type Mismatch

Error: `Expected str, got int`

Fix by correcting the type or adding conversion:
```python
# Option 1: Fix the value
name: str = "hello"  # Not: name: str = 42

# Option 2: Convert
name: str = str(42)
```

#### Optional/None Handling

Error: `X is possibly None`

Fix by adding None check:
```python
# Before
def process(value: str | None) -> str:
    return value.upper()  # Error!

# After
def process(value: str | None) -> str:
    if value is None:
        return ""
    return value.upper()
```

#### Missing Type Stubs

Error: `Cannot find module 'some_library'`

Options:
1. Install type stubs: `pip install types-some_library`
2. Add to `py.typed` package
3. Create stub file (`.pyi`)
4. Use `# type: ignore` as last resort

### Step 4: Apply Fixes

For each error:
1. Read the file containing the error
2. Understand the context
3. Apply the appropriate fix
4. Re-run type check to verify

### Step 5: Handle Strict Mode Issues

If `strict_mode = true` in `pants.toml`, additional checks apply:

| Check | Description | Fix |
|-------|-------------|-----|
| `no-any` | Disallow `Any` type | Use specific types |
| `no-untyped-def` | Require all function types | Add annotations |
| `strict-optional` | Require explicit None handling | Add None checks |

To temporarily relax:
```toml
[baseline-ty]
strict = false
```

## Error Recovery

### "ty not found" or download issues

ty is downloaded automatically. If issues persist:
1. Check network connectivity
2. Verify ty version compatibility
3. Clear Pants cache: `pants clean-all`

### Too many errors to fix at once

Focus on one file or module at a time:
```bash
pants baseline-typecheck src/mymodule/::
```

### Third-party library type issues

For libraries without type stubs:
```python
import some_library  # type: ignore[import-untyped]
```

Or configure globally in `pants.toml`:
```toml
[baseline-ty]
ignore_missing_imports = true
```

## Best Practices

1. **Start with core modules** - Fix types in critical code first
2. **Use gradual typing** - Don't try to type everything at once
3. **Prefer explicit types** - Avoid `Any` when possible
4. **Document complex types** - Use TypeAlias for readability
5. **Test after fixing** - Type fixes can change behavior
