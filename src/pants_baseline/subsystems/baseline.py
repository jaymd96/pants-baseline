"""Main baseline subsystem for coordinating all quality tools."""

from __future__ import annotations

from pants.option.option_types import BoolOption, IntOption, StrListOption, StrOption
from pants.option.subsystem import Subsystem


class BaselineSubsystem(Subsystem):
    """Configuration for the Python Baseline quality framework.

    This subsystem provides global configuration for all baseline tools
    including Ruff, ty, pytest, and uv audit.
    """

    options_scope = "python-baseline"
    help = "Opinionated Python code quality baseline configuration."

    # Global settings
    enabled = BoolOption(
        default=True,
        help="Whether to enable the Python baseline checks globally.",
    )

    python_version = StrOption(
        default="3.11",
        help="Target Python version for all tools (e.g., '3.11', '3.12').",
    )

    line_length = IntOption(
        default=120,
        help="Maximum line length for formatting and linting.",
    )

    src_roots = StrListOption(
        default=["src"],
        help="Source root directories for Python code.",
    )

    test_roots = StrListOption(
        default=["tests"],
        help="Test root directories.",
    )

    exclude_patterns = StrListOption(
        default=[
            ".venv",
            ".git",
            "__pycache__",
            "dist",
            "build",
            ".pytest_cache",
            ".ruff_cache",
            "migrations",
        ],
        help="Patterns to exclude from all baseline checks.",
    )

    # Coverage threshold
    coverage_threshold = IntOption(
        default=80,
        help="Minimum code coverage percentage required.",
    )

    # Strictness level
    strict_mode = BoolOption(
        default=True,
        help="Enable strict mode for all tools (more rigorous checks).",
    )

    def get_python_target_version(self) -> str:
        """Return Python version in format suitable for tools (e.g., 'py311')."""
        version = self.python_version.replace(".", "")
        return f"py{version}"
