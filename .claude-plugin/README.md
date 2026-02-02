# pants-baseline Claude Code Plugin

This plugin provides Claude Code skills for intelligent interaction with the pants-baseline Python quality toolchain.

## Skills

| Skill | Command | Description |
|-------|---------|-------------|
| `baseline-lint` | `/baseline-lint [targets]` | Run Ruff linting with auto-fix support |
| `baseline-fmt` | `/baseline-fmt [targets]` | Run Ruff formatting |
| `baseline-typecheck` | `/baseline-typecheck [targets]` | Run ty type checking |
| `baseline-test` | `/baseline-test [targets]` | Run pytest with coverage |
| `baseline-audit` | `/baseline-audit` | Run security audit |
| `baseline-check` | `/baseline-check [targets]` | Run all checks in sequence |

## What Makes These Skills Intelligent

Unlike running Pants commands directly, these skills provide:

1. **Error Analysis** - Categorizes issues and suggests appropriate fixes
2. **Auto-Fix Support** - Safely applies fixable issues, asks before unsafe fixes
3. **Recovery Guidance** - Helps when things don't go as planned
4. **Incremental Fixing** - Works through issues systematically
5. **Context Awareness** - Reads source files to understand issues

## Usage Examples

### Quick Quality Check

```
/baseline-check
```

Runs all checks (format, lint, typecheck, test, audit) with intelligent error handling at each step.

### Fix Linting Issues

```
/baseline-lint src/::
```

Runs linting, auto-fixes safe issues, asks about unsafe fixes, provides guidance for manual fixes.

### Investigate Test Failures

```
/baseline-test tests/::
```

Runs tests, analyzes failures, reads relevant source code, suggests fixes.

## Installation

This plugin is bundled with pants-baseline. To use it:

1. Install the Claude Code marketplace:
   ```bash
   claude /plugin marketplace add jaymd96/pants-baseline
   ```

2. Install the plugin:
   ```bash
   claude /plugin install pants-baseline@jaymd96-pants-baseline
   ```

Or if using with pants-claude-plugins:
```bash
pants claude-install --include-bundled ::
```

## Requirements

- pants-baseline installed and configured
- Claude Code CLI
- Pants build system
