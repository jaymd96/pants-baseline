"""ty subsystem for type checking configuration."""

from __future__ import annotations

from pants.option.option_types import BoolOption, StrListOption, StrOption
from pants.option.subsystem import Subsystem


class TySubsystem(Subsystem):
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

    version = StrOption(
        default="0.1.0",
        help="Version of ty to use.",
    )

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
