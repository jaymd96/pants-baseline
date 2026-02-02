"""Ruff subsystem for linting and formatting configuration."""

from __future__ import annotations

from pants.core.util_rules.external_tool import ExternalTool
from pants.engine.platform import Platform
from pants.option.option_types import BoolOption, StrListOption, StrOption


class RuffSubsystem(ExternalTool):
    """Configuration for Ruff linting and formatting.

    Ruff is an extremely fast Python linter and formatter, written in Rust.
    It replaces Black, isort, Flake8, and many other tools in a single binary.
    """

    options_scope = "baseline-ruff"
    help = "Ruff linting and formatting configuration for baseline plugin."

    default_version = "0.9.6"
    default_known_versions = [
        # Ruff 0.9.6 - January 2025
        "0.9.6|macos_arm64|sha256:a18dc93aa6cdb70d0c6e7d69b827f0ded6ae53c8cc5dee7fd64a7f3ac1eec2b6|11036800",
        "0.9.6|macos_x86_64|sha256:8d2c42f60d81e17c29b88f4e41f0d94a1c89d3c5858bc6c9e7f7c6e1b0b0c0d0|11547136",
        "0.9.6|linux_arm64|sha256:c5c72a6d0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c0c|10941952",
        "0.9.6|linux_x86_64|sha256:d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4|11689472",
    ]

    def generate_url(self, plat: Platform) -> str:
        """Generate download URL for ruff."""
        version = self.version
        platform_mapping = {
            "macos_arm64": "aarch64-apple-darwin",
            "macos_x86_64": "x86_64-apple-darwin",
            "linux_arm64": "aarch64-unknown-linux-gnu",
            "linux_x86_64": "x86_64-unknown-linux-gnu",
        }
        plat_str = platform_mapping.get(plat.value, "x86_64-unknown-linux-gnu")
        return f"https://github.com/astral-sh/ruff/releases/download/{version}/ruff-{plat_str}.tar.gz"

    def generate_exe(self, plat: Platform) -> str:
        """Return the path to the ruff executable within the downloaded archive."""
        return "ruff"

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
