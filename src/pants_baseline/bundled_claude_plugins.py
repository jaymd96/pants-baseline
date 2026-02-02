"""Bundled Claude Code plugins for pants-baseline.

These plugins are automatically discovered and installed when users run:
    pants claude-install --include-bundled ::

This requires the jaymd96-pants-claude-plugins package to be installed.
"""

# Marketplaces to add before installing plugins
# Format: GitHub "owner/repo" - the marketplace name comes from marketplace.json
BUNDLED_MARKETPLACES = [
    "anthropics/claude-code",  # Adds marketplace named "claude-code-plugins"
    "jaymd96/pants-baseline",  # Adds marketplace named "pants-baseline"
]

# Claude Code plugins to install
# Note: "marketplace" must match the "name" field in the marketplace.json, NOT the GitHub path
BUNDLED_CLAUDE_PLUGINS = [
    # Official Anthropic plugins (from claude-plugins-official, pre-configured)
    {
        "plugin": "github",
        "marketplace": "claude-plugins-official",
        "scope": "project",
        "description": "GitHub integration for PR workflows and issue management",
    },
    # From anthropics/claude-code marketplace (named "claude-code-plugins")
    {
        "plugin": "commit-commands",
        "marketplace": "claude-code-plugins",
        "scope": "project",
        "description": "Git workflow commands for commits, pushes, and PRs",
    },
    # pants-baseline skills plugin (from jaymd96/pants-baseline, named "pants-baseline")
    {
        "plugin": "pants-baseline",
        "marketplace": "pants-baseline",
        "scope": "project",
        "description": "Intelligent skills for baseline-lint, baseline-fmt, baseline-typecheck, baseline-test, baseline-audit",
    },
]
