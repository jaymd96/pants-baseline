"""Bundled Claude Code plugins for pants-baseline.

These plugins are automatically discovered and installed when users run:
    pants claude-install --include-bundled ::

This requires the jaymd96-pants-claude-plugins package to be installed.
"""

# Marketplaces to add before installing plugins
# The demo marketplace contains commit-commands and other workflow plugins
BUNDLED_MARKETPLACES = [
    "anthropics/claude-code",  # Demo plugins marketplace
]

# Claude Code plugins to install
BUNDLED_CLAUDE_PLUGINS = [
    {
        "plugin": "github",
        "marketplace": "claude-plugins-official",
        "scope": "project",
        "description": "GitHub integration for PR workflows and issue management",
    },
    {
        "plugin": "commit-commands",
        "marketplace": "anthropics-claude-code",
        "scope": "project",
        "description": "Git workflow commands for commits, pushes, and PRs",
    },
]
