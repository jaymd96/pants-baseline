"""Rules for uv security auditing."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from pants.engine.process import FallibleProcessResult, Process
from pants.engine.rules import Get, collect_rules, rule
from pants.util.logging import LogLevel


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
) -> AuditResult:
    """Run uv audit on dependencies."""
    # Build ignore args
    ignore_args = []
    for vuln in request.ignore_vulns:
        ignore_args.extend(["--ignore", vuln])

    argv = [
        "uv",
        "audit",
        f"--output-format={request.output_format}",
        *ignore_args,
    ]

    process = Process(
        argv=argv,
        description="Run uv security audit",
        level=LogLevel.DEBUG,
    )

    result = await Get(FallibleProcessResult, {Process: process})

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
