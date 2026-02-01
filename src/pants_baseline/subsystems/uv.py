"""uv subsystem for dependency management and security auditing."""

from __future__ import annotations

from pants.option.option_types import BoolOption, StrListOption, StrOption
from pants.option.subsystem import Subsystem


class UvSubsystem(Subsystem):
    """Configuration for uv dependency management and security auditing.

    uv is Astral's ultra-fast Python package installer and resolver,
    written in Rust. It's 10-100x faster than pip for dependency resolution.

    This subsystem configures uv for:
    - Dependency security auditing (vulnerability scanning)
    - Lock file management
    - Virtual environment management
    """

    options_scope = "baseline-uv"
    help = "uv dependency management and security auditing configuration for baseline plugin."

    version = StrOption(
        default="0.5.0",
        help="Version of uv to use.",
    )

    # Security auditing
    audit_enabled = BoolOption(
        default=True,
        help="Enable dependency security auditing.",
    )

    audit_ignore_vulns = StrListOption(
        default=[],
        help="Vulnerability IDs to ignore (e.g., 'GHSA-xxxx-xxxx-xxxx').",
    )

    audit_fail_on_warning = BoolOption(
        default=False,
        help="Fail the audit if any warnings are found (not just errors).",
    )

    # Lock file settings
    lock_file = StrOption(
        default="uv.lock",
        help="Path to the uv lock file.",
    )

    require_lock = BoolOption(
        default=True,
        help="Require a lock file to exist for auditing.",
    )

    # Output format
    output_format = StrOption(
        default="text",
        help="Output format for audit results ('text', 'json', 'github').",
    )

    # Additional arguments
    extra_args = StrListOption(
        default=[],
        help="Additional arguments to pass to uv commands.",
    )
