"""Rules for uv security auditing."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from pants.engine.console import Console
from pants.engine.fs import Digest
from pants.engine.goal import Goal, GoalSubsystem
from pants.engine.process import FallibleProcessResult, Process
from pants.engine.rules import Get, collect_rules, goal_rule, rule
from pants.engine.target import Targets
from pants.util.logging import LogLevel

from pants_baseline.subsystems.baseline import BaselineSubsystem
from pants_baseline.subsystems.uv import UvSubsystem


@dataclass(frozen=True)
class AuditResult:
    """Result of running uv audit."""

    exit_code: int
    stdout: str
    stderr: str
    vulnerabilities_found: int


class AuditSubsystem(GoalSubsystem):
    """Subsystem for the audit goal."""

    name = "baseline-audit"
    help = "Run security audit on dependencies using uv."


class Audit(Goal):
    """Goal to run security audit."""

    subsystem_cls = AuditSubsystem


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


@goal_rule
async def run_audit_goal(
    console: Console,
    targets: Targets,
    uv_subsystem: UvSubsystem,
    baseline_subsystem: BaselineSubsystem,
) -> Audit:
    """Execute the security audit goal."""
    if not baseline_subsystem.enabled or not uv_subsystem.audit_enabled:
        console.print_stdout("Security audit is disabled.")
        return Audit(exit_code=0)

    console.print_stdout("Running security audit with uv...")

    result = await Get(
        AuditResult,
        UvAuditRequest(
            lock_file=uv_subsystem.lock_file,
            ignore_vulns=tuple(uv_subsystem.audit_ignore_vulns),
            output_format=uv_subsystem.output_format,
        ),
    )

    console.print_stdout(result.stdout)
    if result.stderr:
        console.print_stderr(result.stderr)

    if result.vulnerabilities_found > 0:
        console.print_stderr(
            f"\nFound {result.vulnerabilities_found} vulnerabilities!"
        )
    else:
        console.print_stdout("\nNo vulnerabilities found.")

    return Audit(exit_code=result.exit_code)


def rules() -> Iterable:
    """Return all audit rules."""
    return collect_rules()
