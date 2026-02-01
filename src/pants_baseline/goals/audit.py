"""Audit goal for uv security scanning."""

from typing import Iterable

from pants.engine.console import Console
from pants.engine.goal import Goal, GoalSubsystem
from pants.engine.rules import Get, collect_rules, goal_rule
from pants.engine.target import Targets

from pants_baseline.rules.audit_rules import AuditResult, UvAuditRequest
from pants_baseline.subsystems.baseline import BaselineSubsystem
from pants_baseline.subsystems.uv import UvSubsystem


class BaselineAuditSubsystem(GoalSubsystem):
    """Subsystem for the baseline-audit goal."""

    name = "baseline-audit"
    help = "Run uv security audit on dependencies."


class BaselineAudit(Goal):
    """Goal to run uv security audit."""

    subsystem_cls = BaselineAuditSubsystem


@goal_rule
async def run_baseline_audit(
    console: Console,
    targets: Targets,
    baseline_subsystem: BaselineSubsystem,
    uv_subsystem: UvSubsystem,
) -> BaselineAudit:
    """Run uv security audit on dependencies."""
    if not baseline_subsystem.enabled:
        console.print_stdout("Python baseline is disabled.")
        return BaselineAudit(exit_code=0)

    if not uv_subsystem.audit_enabled:
        console.print_stdout("Security audit is disabled.")
        return BaselineAudit(exit_code=0)

    console.print_stdout("Running uv security audit...")
    console.print_stdout(f"  Lock file: {uv_subsystem.lock_file}")
    if uv_subsystem.audit_ignore_vulns:
        console.print_stdout(f"  Ignoring: {', '.join(uv_subsystem.audit_ignore_vulns)}")
    console.print_stdout("")

    audit_request: UvAuditRequest = UvAuditRequest(
        lock_file=uv_subsystem.lock_file,
        ignore_vulns=tuple(uv_subsystem.audit_ignore_vulns),
        output_format=uv_subsystem.output_format,
    )
    result = await Get(AuditResult, UvAuditRequest, audit_request)

    if result.stdout:
        console.print_stdout(result.stdout)
    if result.stderr:
        console.print_stderr(result.stderr)

    if result.exit_code == 0:
        console.print_stdout("\nNo vulnerabilities found.")
    else:
        console.print_stderr(
            f"\nFound {result.vulnerabilities_found} vulnerabilities!"
        )

    return BaselineAudit(exit_code=result.exit_code)


def rules() -> Iterable:
    """Return all audit goal rules."""
    return collect_rules()
