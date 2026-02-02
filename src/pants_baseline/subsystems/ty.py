"""ty subsystem for type checking configuration."""

from __future__ import annotations

from pants.core.util_rules.external_tool import ExternalTool
from pants.engine.platform import Platform
from pants.option.option_types import BoolOption, StrListOption, StrOption


class TySubsystem(ExternalTool):
    """Configuration for ty type checker.

    ty is Astral's next-generation Python type checker, designed for
    exceptional performance (10-60x faster than MyPy, 80x faster than
    Pyright on incremental edits).

    Features:
    - LSP-first architecture for IDE integration
    - Incremental checking optimized for real-time feedback
    - First-class intersection types and reachability analysis
    - Rust implementation with obsessive performance focus
    """

    options_scope = "baseline-ty"
    help = "ty type checker configuration for baseline plugin (Astral's next-gen type checker)."

    default_version = "0.0.1-alpha.10"
    default_known_versions = [
        # ty is still in alpha - these are placeholder hashes
        "0.0.1-alpha.10|macos_arm64|sha256:0000000000000000000000000000000000000000000000000000000000000000|5000000",
        "0.0.1-alpha.10|macos_x86_64|sha256:0000000000000000000000000000000000000000000000000000000000000000|5000000",
        "0.0.1-alpha.10|linux_arm64|sha256:0000000000000000000000000000000000000000000000000000000000000000|5000000",
        "0.0.1-alpha.10|linux_x86_64|sha256:0000000000000000000000000000000000000000000000000000000000000000|5000000",
    ]

    def generate_url(self, plat: Platform) -> str:
        """Generate download URL for ty."""
        version = self.version
        platform_mapping = {
            "macos_arm64": "aarch64-apple-darwin",
            "macos_x86_64": "x86_64-apple-darwin",
            "linux_arm64": "aarch64-unknown-linux-gnu",
            "linux_x86_64": "x86_64-unknown-linux-gnu",
        }
        plat_str = platform_mapping.get(plat.value, "x86_64-unknown-linux-gnu")
        return f"https://github.com/astral-sh/ty/releases/download/{version}/ty-{plat_str}.tar.gz"

    def generate_exe(self, plat: Platform) -> str:
        """Return the path to the ty executable within the downloaded archive."""
        return "ty"

    # Type checking mode
    strict = BoolOption(
        default=True,
        help="Enable strict type checking mode.",
    )

    # Error reporting
    report_missing_imports = BoolOption(
        default=True,
        help="Report errors for missing imports.",
    )

    report_unused_imports = BoolOption(
        default=True,
        help="Report errors for unused imports.",
    )

    report_unused_variables = BoolOption(
        default=True,
        help="Report errors for unused variables.",
    )

    # Include/exclude paths
    include = StrListOption(
        default=["src", "tests"],
        help="Directories to include in type checking.",
    )

    exclude = StrListOption(
        default=[
            ".venv",
            ".git",
            "__pycache__",
            "dist",
            "build",
        ],
        help="Patterns to exclude from type checking.",
    )

    # Type stub handling
    stub_path = StrOption(
        default="",
        help="Path to custom type stubs directory.",
    )

    # Output format
    output_format = StrOption(
        default="text",
        help="Output format for type errors ('text', 'json', 'github').",
    )
