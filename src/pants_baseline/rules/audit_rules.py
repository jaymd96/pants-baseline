"""Rules for uv security auditing."""

from dataclasses import dataclass
from typing import Iterable

from pants.core.util_rules.external_tool import DownloadedExternalTool, ExternalToolRequest
from pants.engine.fs import Digest, MergeDigests, PathGlobs, Snapshot
from pants.engine.platform import Platform
from pants.engine.process import FallibleProcessResult, Process
from pants.engine.rules import Get, collect_rules, rule
from pants.util.logging import LogLevel

from pants_baseline.subsystems.uv import UvSubsystem


@dataclass(frozen=True)
class AuditResult:
    """Result of running uv audit."""

    exit_code: int
    stdout: str
    stderr: str
    vulnerabilities_found: int


@dataclass(frozen=True)
class UvAuditRequest:
    """Request to run uv audit."""

    lock_file: str
    ignore_vulns: tuple[str, ...]
    output_format: str


@rule(desc="Audit dependencies with uv", level=LogLevel.DEBUG)
async def run_uv_audit(
    request: UvAuditRequest,
    uv_subsystem: UvSubsystem,
    platform: Platform,
) -> AuditResult:
    """Run uv audit on dependencies."""
    # Download uv
    downloaded_uv = await Get(
        DownloadedExternalTool,
        ExternalToolRequest,
        uv_subsystem.get_request(platform),
    )

    # Get the lock file if it exists
    lock_file_snapshot = await Get(
        Snapshot,
        PathGlobs([request.lock_file, "pyproject.toml", "requirements.txt"]),
    )

    # Merge the uv binary with lock files
    input_digest = await Get(
        Digest,
        MergeDigests([downloaded_uv.digest, lock_file_snapshot.digest]),
    )

    # Build ignore args
    ignore_args = []
    for vuln in request.ignore_vulns:
        ignore_args.extend(["--ignore", vuln])

    argv = [
        downloaded_uv.exe,
        "pip",
        "audit",
        f"--output-format={request.output_format}",
        *ignore_args,
    ]

    process = Process(
        argv=argv,
        input_digest=input_digest,
        description="Run uv security audit",
        level=LogLevel.DEBUG,
    )

    result = await Get(FallibleProcessResult, Process, process)

    stdout = result.stdout.decode()
    stderr = result.stderr.decode()

    # Parse vulnerability count from output (simplified)
    vulnerabilities_found = 0
    if result.exit_code != 0:
        # Count lines that look like vulnerability reports
        for line in stdout.split("\n"):
            if "vulnerability" in line.lower() or "CVE-" in line or "GHSA-" in line:
                vulnerabilities_found += 1

    return AuditResult(
        exit_code=result.exit_code,
        stdout=stdout,
        stderr=stderr,
        vulnerabilities_found=vulnerabilities_found,
    )


def rules() -> Iterable:
    """Return all audit rules."""
    return collect_rules()
