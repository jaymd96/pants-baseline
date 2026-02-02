---
description: Run security audit on dependencies with vulnerability remediation
user_invocable: true
triggers:
  - security audit
  - check vulnerabilities
  - dependency audit
  - uv audit
  - baseline audit
arguments: "[targets]"
---

# Baseline Security Audit Skill

Run uv security audit on project dependencies with vulnerability analysis and remediation guidance.

## Workflow

### Step 1: Run Security Audit

Run the audit:

```bash
pants baseline-audit ::
```

### Step 2: Analyze Vulnerabilities

If vulnerabilities are found, analyze each one:

1. **Severity level** - Critical, High, Medium, Low
2. **Affected package** - Which dependency is vulnerable
3. **Vulnerability ID** - CVE or GHSA identifier
4. **Description** - What the vulnerability allows
5. **Fixed version** - Version that patches the issue

### Step 3: Prioritize Fixes

Focus on vulnerabilities in this order:

1. **Critical/High in direct dependencies** - Fix immediately
2. **Critical/High in transitive dependencies** - Update parent package
3. **Medium severity** - Plan to fix
4. **Low severity** - Track but may defer

### Step 4: Remediation Strategies

#### Update to Fixed Version

If a patched version exists:

```bash
# Update specific package
uv pip install "package>=fixed_version"

# Or update in pyproject.toml
# [project.dependencies]
# package = ">=2.0.1"  # Fixed CVE-XXXX

# Regenerate lock file
uv lock
```

#### Pin to Safe Version

If latest has issues but older version is safe:

```toml
# pyproject.toml
[project.dependencies]
package = ">=1.5.0,<2.0.0"  # 2.x has vulnerability
```

#### Replace Vulnerable Package

If no fix is available:

1. Find alternative packages
2. Evaluate migration effort
3. Replace usage throughout codebase

#### Accept Risk (Temporary)

If vulnerability doesn't apply to your use case:

```toml
# pants.toml
[baseline-uv]
audit_ignore_vulns = ["GHSA-xxxx-yyyy-zzzz"]
```

Document why this is acceptable.

### Step 5: Verify Fix

After updating dependencies:

```bash
# Regenerate lock file
uv lock

# Re-run audit
pants baseline-audit ::
```

## Understanding Vulnerability Reports

### CVE Format

```
CVE-2024-12345: SQL Injection in package-name
Severity: HIGH
Affected: <2.0.0
Fixed: >=2.0.0
```

### GHSA Format

```
GHSA-xxxx-yyyy-zzzz: Remote Code Execution
Package: vulnerable-lib
Vulnerable: 1.0.0 - 1.5.2
Patched: 1.5.3
```

## Error Recovery

### "Lock file not found"

Create a lock file:

```bash
uv lock
```

Or configure the path:

```toml
# pants.toml
[baseline-uv]
lock_file = "requirements.lock"
```

### "uv not available"

uv is downloaded automatically. If issues persist:

1. Check network connectivity
2. Clear cache: `pants clean-all`
3. Verify uv version in pants.toml

### False Positives

If a vulnerability doesn't apply to your usage:

1. Document why it's not applicable
2. Add to ignore list with comment
3. Create issue to track removal of ignore

```toml
# pants.toml
[baseline-uv]
# GHSA-xxxx: Only affects Windows, we're Linux-only
audit_ignore_vulns = ["GHSA-xxxx-yyyy-zzzz"]
```

## Best Practices

1. **Run audits regularly** - Add to CI/CD pipeline
2. **Update dependencies proactively** - Don't wait for vulnerabilities
3. **Monitor security advisories** - Subscribe to package security lists
4. **Minimize dependencies** - Fewer deps = smaller attack surface
5. **Use lock files** - Pin exact versions for reproducibility
6. **Document exceptions** - Explain why vulnerabilities are ignored
