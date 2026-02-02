# jaymd96-pants-baseline

An opinionated Python code quality baseline plugin for the [Pants](https://www.pantsbuild.org/) build system.

## Overview

This plugin integrates modern, high-performance tools from the Astral ecosystem to enforce consistent code quality standards across Python projects:

| Tool | Purpose | Performance |
|------|---------|-------------|
| **Ruff** | Linting & Formatting | 100-1000x faster than Flake8/Black |
| **ty** | Type Checking | 10-60x faster than MyPy |
| **uv** | Dependency Security Audit | 10-100x faster than pip |
| **pytest** | Testing with Coverage | Industry standard |

## Installation

Add the plugin to your `pants.toml`:

```toml
[GLOBAL]
backend_packages = [
    "pants.backend.python",
    "pants_baseline",
]

plugins = [
    "jaymd96-pants-baseline==0.2.0",
]
```

## Quick Start

### 1. Define a baseline project

Create a `BUILD` file in your project root:

```python
baseline_python_project(
    name="my_project",
    sources=["src/**/*.py"],
    test_sources=["tests/**/*.py"],
    python_version="3.13",
    line_length=120,
    strict=True,
    coverage_threshold=80,
)
```

### 2. Run quality checks

```bash
# Lint with Ruff
pants baseline-lint ::

# Format with Ruff
pants baseline-fmt ::

# Type check with ty
pants baseline-typecheck ::

# Run tests with coverage
pants baseline-test ::

# Security audit with uv
pants baseline-audit ::
```

## Configuration

### Global Configuration (`pants.toml`)

```toml
[python-baseline]
# Enable/disable all baseline checks
enabled = true

# Target Python version
python_version = "3.13"

# Maximum line length
line_length = 120

# Source and test directories
src_roots = ["src"]
test_roots = ["tests"]

# Minimum coverage threshold
coverage_threshold = 80

# Enable strict mode for all tools
strict_mode = true

# Patterns to exclude
exclude_patterns = [
    ".venv",
    "__pycache__",
    "migrations",
]
```

### Ruff Configuration

```toml
[ruff]
version = "0.2.0"

# Lint rules to enable
select = [
    "E",      # pycodestyle errors
    "W",      # pycodestyle warnings
    "F",      # pyflakes
    "I",      # isort
    "N",      # pep8-naming
    "UP",     # pyupgrade
    "B",      # flake8-bugbear
    "C4",     # flake8-comprehensions
    "SIM",    # flake8-simplify
    "RUF",    # Ruff-specific
]

# Rules to ignore
ignore = ["E501"]

# Formatting options
quote_style = "double"
indent_style = "space"

# Auto-fix options
fix = true
unsafe_fixes = false
```

### ty Configuration

```toml
[ty]
version = "0.1.0"

# Enable strict type checking
strict = true

# Reporting options
report_missing_imports = true
report_unused_imports = true
report_unused_variables = true

# Include/exclude paths
include = ["src", "tests"]
exclude = [".venv", "dist"]

# Output format (text, json, github)
output_format = "text"
```

### uv Configuration

```toml
[uv]
version = "0.5.0"

# Security auditing
audit_enabled = true
audit_ignore_vulns = []
audit_fail_on_warning = false

# Lock file
lock_file = "uv.lock"
require_lock = true

# Output format
output_format = "text"
```

## Target Fields

The `baseline_python_project` target supports the following fields:

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `sources` | `list[str]` | `["**/*.py"]` | Python source file patterns |
| `test_sources` | `list[str]` | `["tests/**/*.py"]` | Test file patterns |
| `python_version` | `str` | `"3.13"` | Target Python version |
| `line_length` | `int` | `120` | Maximum line length |
| `strict` | `bool` | `True` | Enable strict mode |
| `coverage_threshold` | `int` | `80` | Minimum coverage % |
| `skip_lint` | `bool` | `False` | Skip Ruff linting |
| `skip_fmt` | `bool` | `False` | Skip Ruff formatting |
| `skip_typecheck` | `bool` | `False` | Skip ty type checking |
| `skip_test` | `bool` | `False` | Skip pytest |
| `skip_audit` | `bool` | `False` | Skip uv security audit |

## Goals

### `baseline-lint`

Run Ruff linting on Python files.

```bash
pants baseline-lint src/::
```

### `baseline-fmt`

Format Python files with Ruff.

```bash
pants baseline-fmt src/::

# Check formatting without modifying files
pants baseline-fmt --check src/::
```

### `baseline-typecheck`

Run ty type checking.

```bash
pants baseline-typecheck src/::
```

### `baseline-test`

Run pytest with coverage.

```bash
pants baseline-test tests/::

# Run specific test markers
pants baseline-test --pytest-args="-m unit" tests/::
```

### `baseline-audit`

Run uv security audit on dependencies.

```bash
pants baseline-audit ::

# Ignore specific vulnerabilities
pants --uv-audit-ignore-vulns="['GHSA-xxxx']" baseline-audit ::
```

## Example Project Structure

```
my-project/
├── BUILD
├── pants.toml
├── pyproject.toml
├── uv.lock
├── src/
│   └── my_package/
│       ├── BUILD
│       ├── __init__.py
│       └── main.py
└── tests/
    ├── BUILD
    ├── conftest.py
    └── test_main.py
```

### Root `BUILD` file

```python
baseline_python_project(
    name="my_project",
    sources=["src/**/*.py"],
    test_sources=["tests/**/*.py"],
)
```

### `pants.toml`

```toml
[GLOBAL]
pants_version = "2.30.1"
backend_packages = [
    "pants.backend.python",
    "pants_baseline",
]
plugins = ["jaymd96-pants-baseline==0.2.0"]

[python]
interpreter_constraints = ["CPython>=3.13,<4"]

[python-baseline]
python_version = "3.13"
line_length = 120
coverage_threshold = 80

[ruff]
select = ["E", "F", "I", "B", "UP", "RUF"]

[ty]
strict = true
```

## Why This Stack?

### Performance Comparison

| Task | Traditional Stack | Baseline Stack | Speedup |
|------|-------------------|----------------|---------|
| Lint (50K LOC) | 20s (Flake8) | 0.4s (Ruff) | **50x** |
| Format (50K LOC) | 8s (Black) | 0.3s (Ruff) | **26x** |
| Type Check | 45s (MyPy) | 4.7ms (ty) | **9500x** |
| Pre-commit | 18s | 0.3s | **60x** |

### Tool Consolidation

| Traditional | Baseline |
|-------------|----------|
| Black | Ruff format |
| isort | Ruff (I rules) |
| Flake8 + plugins | Ruff lint |
| MyPy/Pyright | ty |
| pip-audit | uv audit |

## Claude Code Integration

This plugin bundles recommended [Claude Code](https://claude.ai/code) plugins for enhanced AI-assisted development workflows.

### Install Bundled Claude Plugins

When combined with [jaymd96-pants-claude-plugins](https://github.com/jaymd96/pants-claude-plugins):

```toml
# pants.toml
[GLOBAL]
plugins = [
    "jaymd96-pants-baseline==0.2.0",
    "jaymd96-pants-claude-plugins>=0.2.0",
]
backend_packages = [
    "pants_baseline",
    "pants_claude_plugins",
]
```

Then run:

```bash
pants claude-install --include-bundled ::
```

This automatically installs:
- **github** - GitHub integration for PR workflows and issue management
- **commit-commands** - Git workflow commands for commits, pushes, and PRs

## Development

### Setup

```bash
cd python-baseline
hatch env create
```

### Run tests

```bash
hatch run test
hatch run test-cov
```

### Lint and format

```bash
hatch run lint
hatch run fmt
```

## License

Apache License 2.0

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting a PR.

## Credits

Built with tools from:
- [Astral](https://astral.sh/) - Ruff, ty, uv
- [Pants](https://www.pantsbuild.org/) - Build system
- [pytest](https://docs.pytest.org/) - Testing framework
