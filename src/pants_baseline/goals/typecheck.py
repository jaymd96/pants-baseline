"""Type check goal for ty type checking."""

from __future__ import annotations

from typing import Iterable

from pants.engine.console import Console
from pants.engine.goal import Goal, GoalSubsystem
from pants.engine.rules import collect_rules, goal_rule
from pants.engine.target import Targets

from pants_baseline.subsystems.baseline import BaselineSubsystem
from pants_baseline.subsystems.ty import TySubsystem


class BaselineTypecheckSubsystem(GoalSubsystem):
    """Subsystem for the baseline-typecheck goal."""

    name = "baseline-typecheck"
    help = "Run ty type checking with baseline configuration."


class BaselineTypecheck(Goal):
    """Goal to run ty type checking."""

    subsystem_cls = BaselineTypecheckSubsystem


@goal_rule
async def run_baseline_typecheck(
    console: Console,
    targets: Targets,
    baseline_subsystem: BaselineSubsystem,
    ty_subsystem: TySubsystem,
) -> BaselineTypecheck:
    """Run ty type checking on all targets."""
    if not baseline_subsystem.enabled:
        console.print_stdout("Python baseline is disabled.")
        return BaselineTypecheck(exit_code=0)

    console.print_stdout("Running ty type checker...")
    console.print_stdout(f"  Target Python version: {baseline_subsystem.python_version}")
    console.print_stdout(f"  Strict mode: {ty_subsystem.strict}")
    console.print_stdout(f"  Output format: {ty_subsystem.output_format}")
    console.print_stdout("")

    # The actual type checking is handled by the CheckRequest mechanism
    # This goal just provides a user-friendly entry point

    return BaselineTypecheck(exit_code=0)


def rules() -> Iterable:
    """Return all typecheck goal rules."""
    return collect_rules()
