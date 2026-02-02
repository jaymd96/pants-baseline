---
description: Run Ruff formatting on Python code with change reporting
user_invocable: true
triggers:
  - format python
  - format code
  - ruff format
  - baseline fmt
  - fix formatting
arguments: "[targets]"
---

# Baseline Format Skill

Run Ruff formatting on Python code with intelligent change reporting and verification.

## Workflow

### Step 1: Check Current State (Optional)

To see what would change without modifying files:

```bash
pants baseline-fmt --check ${targets:-::}
```

This shows files that need formatting without changing them.

### Step 2: Apply Formatting

Run the formatter to fix all formatting issues:

```bash
pants baseline-fmt ${targets:-::}
```

### Step 3: Report Changes

After formatting:
1. **List modified files** - Show which files were changed
2. **Summarize changes** - Quote style, line length, import sorting
3. **Verify consistency** - Confirm all files now pass

### Step 4: Handle Conflicts

If formatting conflicts with linting rules:

1. **Import sorting conflicts** - Ruff handles both isort and formatting
2. **Line length issues** - Formatter respects `line_length` setting
3. **Quote style** - Configured via `baseline-ruff-quote-style`

Check configuration in `pants.toml`:
```toml
[baseline-ruff]
quote_style = "double"
indent_style = "space"
```

### Step 5: Verify with Lint

After formatting, run lint to ensure no new issues:

```bash
pants baseline-lint ${targets:-::}
```

## Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| `quote_style` | `"double"` | Use double or single quotes |
| `indent_style` | `"space"` | Use spaces or tabs |
| `line_length` | `120` | Maximum line length |

## Error Recovery

### "No baseline_python_project targets found"

Define baseline targets in BUILD files:
```python
baseline_python_project(
    name="my_project",
    sources=["src/**/*.py"],
)
```

### Files not being formatted

Check that files match the `sources` pattern in your target definition.

### Formatting undone by other tools

Ensure no other formatters (Black, autopep8) are configured. Ruff replaces them.

## Integration Tips

1. **Run before committing** - Format before lint and type check
2. **CI verification** - Use `--check` flag in CI to fail on unformatted code
3. **Pre-commit hooks** - Consider adding format check to git hooks
4. **Editor integration** - Configure editor to format on save with Ruff
