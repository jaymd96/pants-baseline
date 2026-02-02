---
description: Run all baseline quality checks with incremental error handling
user_invocable: true
triggers:
  - check all
  - run all checks
  - baseline check
  - quality check
  - full check
arguments: "[targets]"
---

# Baseline Full Check Skill

Run all baseline quality checks (format, lint, typecheck, test, audit) with intelligent sequencing and incremental error handling.

## Workflow Overview

Run checks in this order to maximize efficiency:

1. **Format** - Fix formatting first (fast, no-brainer fixes)
2. **Lint** - Fix style issues (may overlap with format)
3. **Type Check** - Catch type errors (deeper analysis)
4. **Test** - Run tests (verify functionality)
5. **Audit** - Security check (verify dependencies)

Stop and fix at each step before proceeding.

## Step 1: Format Code

```bash
pants baseline-fmt ${targets:-::}
```

**On Success:** Proceed to lint
**On Failure:** Formatting should never fail - investigate configuration issues

## Step 2: Lint Code

```bash
pants baseline-lint ${targets:-::}
```

**On Success:** Proceed to type check

**On Failure:**
1. Check for auto-fixable issues:
   ```bash
   pants baseline-lint --baseline-ruff-fix=true ${targets:-::}
   ```

2. If unsafe fixes available, ask user:
   - Explain what changes would be made
   - If approved: `--baseline-ruff-unsafe-fixes=true`

3. For manual fixes:
   - Group errors by type
   - Fix each category
   - Re-run lint

## Step 3: Type Check

```bash
pants baseline-typecheck ${targets:-::}
```

**On Success:** Proceed to tests

**On Failure:**
1. Categorize errors (missing types, mismatches, etc.)
2. Fix highest-impact issues first
3. Consider relaxing strict mode temporarily if overwhelmed
4. Re-run type check

## Step 4: Run Tests

```bash
pants baseline-test ${targets:-::}
```

Or with more detail:
```bash
pants test --pytest-args="-v" ${targets:-tests/::}
```

**On Success:** Check coverage threshold

**On Failure:**
1. Identify failing tests
2. Determine if test bug or code bug
3. Fix issues
4. Re-run failed tests first:
   ```bash
   pants test --pytest-args="--lf" tests/::
   ```

**Coverage Below Threshold:**
1. Identify uncovered lines
2. Write missing tests
3. Or adjust threshold if appropriate

## Step 5: Security Audit

```bash
pants baseline-audit ::
```

**On Success:** All checks passed!

**On Failure:**
1. Prioritize by severity (Critical > High > Medium > Low)
2. Update vulnerable packages
3. Regenerate lock file
4. Re-run audit

## Quick Check Commands

### Check Everything (Strict)

```bash
pants baseline-fmt :: && \
pants baseline-lint :: && \
pants baseline-typecheck :: && \
pants test :: && \
pants baseline-audit ::
```

### Check Specific Directory

```bash
pants baseline-fmt src/mymodule/:: && \
pants baseline-lint src/mymodule/:: && \
pants baseline-typecheck src/mymodule/::
```

### Pre-Commit Check (Fast)

```bash
pants baseline-fmt --check :: && \
pants baseline-lint ::
```

## Error Recovery Strategies

### Too Many Errors

If overwhelmed by errors:

1. **Focus on one module** - Fix `src/core/::` first
2. **Disable strict mode temporarily** - Make incremental progress
3. **Prioritize by impact** - Fix code bugs before style issues
4. **Use baseline incrementally** - Add more checks as codebase improves

### Configuration Issues

If checks aren't running correctly:

1. Verify `pants.toml` configuration
2. Check BUILD file target definitions
3. Ensure baseline is enabled:
   ```toml
   [baseline-python]
   enabled = true
   ```

### CI/CD Integration

For continuous integration:

```yaml
# Example GitHub Actions
- name: Format Check
  run: pants baseline-fmt --check ::

- name: Lint
  run: pants baseline-lint ::

- name: Type Check
  run: pants baseline-typecheck ::

- name: Test
  run: pants test --pytest-args="--cov-fail-under=80" ::

- name: Security Audit
  run: pants baseline-audit ::
```

## Progress Tracking

Use this checklist for a clean codebase:

- [ ] All files formatted (`baseline-fmt`)
- [ ] No lint errors (`baseline-lint`)
- [ ] No type errors (`baseline-typecheck`)
- [ ] All tests pass (`baseline-test`)
- [ ] Coverage >= threshold (default 80%)
- [ ] No security vulnerabilities (`baseline-audit`)

## Best Practices

1. **Run checks before committing** - Catch issues early
2. **Fix format/lint first** - They're the fastest
3. **Don't skip checks** - Each catches different issues
4. **Keep checks green** - Fix failures immediately
5. **Review unsafe fixes** - Don't auto-apply blindly
6. **Track coverage trends** - Don't let it drop
7. **Update dependencies regularly** - Prevent vulnerability buildup
