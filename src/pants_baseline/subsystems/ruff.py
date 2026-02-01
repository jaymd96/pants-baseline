"""Ruff subsystem for linting and formatting configuration."""

from __future__ import annotations

from pants.option.option_types import BoolOption, StrListOption, StrOption
from pants.option.subsystem import Subsystem


class RuffSubsystem(Subsystem):
    """Configuration for Ruff linting and formatting.

    Ruff is an extremely fast Python linter and formatter, written in Rust.
    It replaces Black, isort, Flake8, and many other tools in a single binary.
    """

    options_scope = "ruff"
    help = "Ruff linting and formatting configuration."

    version = StrOption(
        default="0.2.0",
        help="Version of Ruff to use.",
    )

    # Linting configuration
    select = StrListOption(
        default=[
            "E",      # pycodestyle errors
            "W",      # pycodestyle warnings
            "F",      # pyflakes
            "I",      # isort
            "N",      # pep8-naming
            "UP",     # pyupgrade
            "B",      # flake8-bugbear
            "C4",     # flake8-comprehensions
            "SIM",    # flake8-simplify
            "ASYNC",  # flake8-async
            "DTZ",    # flake8-datetimez
            "PIE",    # flake8-pie
            "RUF",    # Ruff-specific rules
        ],
        help="Rule codes to enable for linting.",
    )

    ignore = StrListOption(
        default=[
            "E501",   # line too long (handled by formatter)
            "W292",   # blank line at end of file
        ],
        help="Rule codes to ignore.",
    )

    # Formatting configuration
    quote_style = StrOption(
        default="double",
        help="Quote style for formatting ('double' or 'single').",
    )

    indent_style = StrOption(
        default="space",
        help="Indentation style ('space' or 'tab').",
    )

    # Auto-fix
    fix = BoolOption(
        default=True,
        help="Automatically fix auto-fixable issues.",
    )

    unsafe_fixes = BoolOption(
        default=False,
        help="Allow unsafe fixes that may change code behavior.",
    )

    # Per-file ignores (common patterns)
    skip_tests_rules = StrListOption(
        default=[
            "F401",   # unused imports OK in tests
            "F811",   # redefined function OK in tests
            "S101",   # assert OK in tests
        ],
        help="Rules to skip in test files.",
    )

    skip_init_rules = StrListOption(
        default=[
            "F401",   # unused imports (exports)
            "F403",   # star imports OK for namespace
        ],
        help="Rules to skip in __init__.py files.",
    )
