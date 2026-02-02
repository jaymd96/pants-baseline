---
description: Run Ruff linting with intelligent error handling and auto-fix support
user_invocable: true
triggers:
  - lint python
  - run linter
  - check code style
  - ruff lint
  - baseline lint
arguments: "[targets]"
---

# Baseline Lint Skill

Run Ruff linting on Python code with intelligent error handling, auto-fix support, and guidance for manual fixes.

## Workflow

### Step 1: Run Initial Lint Check

Run the linter to identify issues:

```bash
pants baseline-lint ${targets:-::}
```

### Step 2: Analyze Results

If linting passes (exit code 0):
- Report success and summarize what was checked
- Suggest running `baseline-fmt` if not already done

If linting fails, analyze the output to categorize issues:

1. **Auto-fixable issues** - Can be fixed with `--fix`
2. **Unsafe fixes available** - Require user confirmation
3. **Manual fixes required** - Need code changes

### Step 3: Handle Auto-Fixable Issues

If there are auto-fixable issues, offer to apply safe fixes:

```bash
pants baseline-lint --baseline-ruff-fix=true ${targets:-::}
```

Report which files were modified and what was fixed.

### Step 4: Handle Unsafe Fixes

If there are issues that require unsafe fixes (marked with `[*]` in Ruff output):

1. **Explain what unsafe fixes do** - They may change code behavior
2. **List specific unsafe fixes** being suggested
3. **Ask user for confirmation** before applying

If user approves:
```bash
pants baseline-lint --baseline-ruff-fix=true --baseline-ruff-unsafe-fixes=true ${targets:-::}
```

If user declines, provide guidance on manual alternatives.

### Step 5: Handle Remaining Issues

For issues that cannot be auto-fixed:

1. **Group by error type** (e.g., all F401 unused imports together)
2. **Provide specific fix guidance** for each category
3. **Offer to fix manually** by editing the files

Common issue categories and fixes:

| Code | Issue | Fix Approach |
|------|-------|--------------|
| F401 | Unused import | Remove the import or add `# noqa: F401` if intentional |
| F841 | Unused variable | Remove or prefix with `_` |
| E501 | Line too long | Break into multiple lines (usually handled by formatter) |
| B006 | Mutable default | Use `None` default with body assignment |
| UP035 | Deprecated import | Update to new import path |

### Step 6: Re-run Verification

After fixes are applied, re-run linting to verify:

```bash
pants baseline-lint ${targets:-::}
```

If issues remain, repeat the analysis and fix cycle.

## Error Recovery

### "No baseline_python_project targets found"

The project may not have baseline targets defined. Check for:
1. Missing `BUILD` files
2. Need to define `baseline_python_project` targets

### "Python baseline is disabled"

Enable in `pants.toml`:
```toml
[baseline-python]
enabled = true
```

### Ruff binary not found

Pants will auto-download Ruff. If issues persist:
1. Check network connectivity
2. Verify Ruff version in `pants.toml`

## Tips

- Run `pants baseline-fmt ::` first to fix formatting issues
- Use `--baseline-ruff-select` to focus on specific rules
- Add `# noqa: XXXX` comments sparingly for intentional violations
- Configure project-wide ignores in `pants.toml` under `[baseline-ruff]`
