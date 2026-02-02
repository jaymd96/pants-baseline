"""Bundled Claude Code plugins for pants-baseline.

These plugins are automatically discovered and installed when users run:
    pants claude-install --include-bundled ::

This requires the jaymd96-pants-claude-plugins package to be installed.
"""

# Marketplaces to add before installing plugins
BUNDLED_MARKETPLACES = [
    "anthropics/claude-code",  # Demo plugins marketplace (for commit-commands)
    "jaymd96/pants-baseline",  # This repo's marketplace (for pants-baseline skills)
]

# Claude Code plugins to install
BUNDLED_CLAUDE_PLUGINS = [
    # Official Anthropic plugins
    {
        "plugin": "github",
        "marketplace": "claude-plugins-official",
        "scope": "project",
        "description": "GitHub integration for PR workflows and issue management",
    },
    # Demo marketplace plugins
    {
        "plugin": "commit-commands",
        "marketplace": "anthropics-claude-code",
        "scope": "project",
        "description": "Git workflow commands for commits, pushes, and PRs",
    },
    # pants-baseline skills plugin (from this repo's marketplace)
    {
        "plugin": "pants-baseline",
        "marketplace": "jaymd96-pants-baseline",
        "scope": "project",
        "description": "Intelligent skills for baseline-lint, baseline-fmt, baseline-typecheck, baseline-test, baseline-audit",
    },
]
