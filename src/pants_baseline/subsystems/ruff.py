"""Ruff subsystem for linting and formatting configuration."""

from __future__ import annotations

from pants.core.util_rules.external_tool import ExternalTool
from pants.engine.platform import Platform
from pants.engine.rules import collect_rules
from pants.engine.unions import UnionRule
from pants.option.option_types import BoolOption, SkipOption, StrListOption, StrOption
from pants.core.goals.generate_lockfiles import ExportableTool


class RuffSubsystem(ExternalTool):
    """Configuration for Ruff linting and formatting.

    Ruff is an extremely fast Python linter and formatter, written in Rust.
    It replaces Black, isort, Flake8, and many other tools in a single binary.
    """

    options_scope = "baseline-ruff"
    help = "Ruff linting and formatting configuration for baseline plugin."

    default_version = "0.9.6"
    default_known_versions = [
        # Ruff 0.9.6 - Format: version|platform|sha256_hash|file_size_bytes
        "0.9.6|macos_arm64|a3132eb5e3d95f36d378144082276fbed0309789dadb19d8a4c41ec5e80451fb|11124436",
        "0.9.6|macos_x86_64|ec88c095036b25e95391ea202fcc9496d565f4e43152db10785eb9757ea0815d|11663591",
        "0.9.6|linux_arm64|cf796c953def5a7102002372893942fac875ac718355698a4a70405104dfbb6c|11946730",
        "0.9.6|linux_x86_64|bed850f15d4d5aaaef2b6a131bfecd5b9d7d3191596249d07e576bd9fd37078e|12511815",
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
        platform_mapping = {
            "macos_arm64": "aarch64-apple-darwin",
            "macos_x86_64": "x86_64-apple-darwin",
            "linux_arm64": "aarch64-unknown-linux-gnu",
            "linux_x86_64": "x86_64-unknown-linux-gnu",
        }
        plat_str = platform_mapping.get(plat.value, "x86_64-unknown-linux-gnu")
        return f"ruff-{plat_str}/ruff"

    # Skip option required by Pants for tool subsystems
    skip = SkipOption("lint", "fmt")

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


def rules():
    """Return rules for the Ruff subsystem."""
    return (
        *collect_rules(),
        UnionRule(ExportableTool, RuffSubsystem),
    )
