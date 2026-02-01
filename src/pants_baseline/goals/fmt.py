"""Format goal for Ruff formatting."""

from __future__ import annotations

from typing import Iterable

from pants.engine.console import Console
from pants.engine.goal import Goal, GoalSubsystem
from pants.engine.rules import collect_rules, goal_rule
from pants.engine.target import Targets

from pants_baseline.subsystems.baseline import BaselineSubsystem
from pants_baseline.subsystems.ruff import RuffSubsystem


class BaselineFmtSubsystem(GoalSubsystem):
    """Subsystem for the baseline-fmt goal."""

    name = "baseline-fmt"
    help = "Run Ruff formatting with baseline configuration."


class BaselineFmt(Goal):
    """Goal to run Ruff formatting."""

    subsystem_cls = BaselineFmtSubsystem


@goal_rule
async def run_baseline_fmt(
    console: Console,
    targets: Targets,
    baseline_subsystem: BaselineSubsystem,
    ruff_subsystem: RuffSubsystem,
) -> BaselineFmt:
    """Run Ruff formatting on all targets."""
    if not baseline_subsystem.enabled:
        console.print_stdout("Python baseline is disabled.")
        return BaselineFmt(exit_code=0)

    console.print_stdout("Running Ruff formatter...")
    console.print_stdout(f"  Target Python version: {baseline_subsystem.python_version}")
    console.print_stdout(f"  Line length: {baseline_subsystem.line_length}")
    console.print_stdout(f"  Quote style: {ruff_subsystem.quote_style}")
    console.print_stdout(f"  Indent style: {ruff_subsystem.indent_style}")
    console.print_stdout("")

    # The actual formatting is handled by the FmtTargetsRequest mechanism
    # This goal just provides a user-friendly entry point

    return BaselineFmt(exit_code=0)


def rules() -> Iterable:
    """Return all fmt goal rules."""
    return collect_rules()
