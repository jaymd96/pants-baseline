"""Pants Python Baseline Plugin.

An opinionated Python code quality baseline plugin for the Pants build system.
Integrates modern, high-performance tools from the Astral ecosystem:

- **Ruff**: Ultra-fast linting and formatting (replaces Black, isort, Flake8)
- **ty**: Next-generation type checker (10-60x faster than MyPy)
- **uv**: Fast dependency management and security auditing
- **pytest**: Industry-standard testing with coverage support

This plugin provides sensible defaults that enforce code quality standards
across Python projects with minimal configuration.
"""

from pants_baseline.__about__ import __version__

__all__ = ["__version__"]
