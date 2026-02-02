"""uv subsystem for dependency management and security auditing."""

from __future__ import annotations

from pants.core.goals.generate_lockfiles import ExportableTool
from pants.core.util_rules.external_tool import ExternalTool
from pants.engine.platform import Platform
from pants.engine.rules import collect_rules
from pants.engine.unions import UnionRule
from pants.option.option_types import BoolOption, StrListOption, StrOption


class UvSubsystem(ExternalTool):
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

    default_version = "0.5.21"
    default_known_versions = [
        # uv 0.5.21
        "0.5.21|macos_arm64|sha256:0000000000000000000000000000000000000000000000000000000000000000|15000000",
        "0.5.21|macos_x86_64|sha256:0000000000000000000000000000000000000000000000000000000000000000|15000000",
        "0.5.21|linux_arm64|sha256:0000000000000000000000000000000000000000000000000000000000000000|15000000",
        "0.5.21|linux_x86_64|sha256:0000000000000000000000000000000000000000000000000000000000000000|15000000",
    ]

    def generate_url(self, plat: Platform) -> str:
        """Generate download URL for uv."""
        version = self.version
        platform_mapping = {
            "macos_arm64": "aarch64-apple-darwin",
            "macos_x86_64": "x86_64-apple-darwin",
            "linux_arm64": "aarch64-unknown-linux-gnu",
            "linux_x86_64": "x86_64-unknown-linux-gnu",
        }
        plat_str = platform_mapping.get(plat.value, "x86_64-unknown-linux-gnu")
        return f"https://github.com/astral-sh/uv/releases/download/{version}/uv-{plat_str}.tar.gz"

    def generate_exe(self, plat: Platform) -> str:
        """Return the path to the uv executable within the downloaded archive."""
        return "uv"

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


def rules():
    """Return rules for the uv subsystem."""
    return (
        *collect_rules(),
        UnionRule(ExportableTool, UvSubsystem),
    )
