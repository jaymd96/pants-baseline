"""Format goal for Ruff formatting."""

from __future__ import annotations

from typing import Iterable

from pants.core.goals.fmt import FmtResult
from pants.engine.console import Console
from pants.engine.goal import Goal, GoalSubsystem
from pants.engine.rules import Get, collect_rules, goal_rule
from pants.engine.target import FilteredTargets

from pants_baseline.rules.fmt_rules import RuffFmtFieldSet, RuffFmtRequest
from pants_baseline.subsystems.baseline import BaselineSubsystem
from pants_baseline.subsystems.ruff import RuffSubsystem
from pants_baseline.targets import BaselineSourcesField


class BaselineFmtSubsystem(GoalSubsystem):
    """Subsystem for the baseline-fmt goal."""

    name = "baseline-fmt"
    help = "Run Ruff formatting with baseline configuration."


class BaselineFmt(Goal):
    """Goal to run Ruff formatting."""

    subsystem_cls = BaselineFmtSubsystem
    environment_behavior = Goal.EnvironmentBehavior.LOCAL_ONLY


@goal_rule
async def run_baseline_fmt(
    console: Console,
    targets: FilteredTargets,
    baseline_subsystem: BaselineSubsystem,
    ruff_subsystem: RuffSubsystem,
) -> BaselineFmt:
    """Run Ruff formatting on all targets."""
    if not baseline_subsystem.enabled:
        console.print_stdout("Python baseline is disabled.")
        return BaselineFmt(exit_code=0)

    # Filter targets that have BaselineSourcesField
    applicable_targets = [
        t for t in targets
        if t.has_field(BaselineSourcesField)
    ]

    if not applicable_targets:
        console.print_stdout("No baseline_python_project targets found.")
        return BaselineFmt(exit_code=0)

    # Create field sets for each target
    field_sets = [
        RuffFmtFieldSet.create(t)
        for t in applicable_targets
    ]

    # Create the fmt request and run it
    request = RuffFmtRequest(field_sets)
    result = await Get(FmtResult, RuffFmtRequest, request)

    # Print results
    if result.stdout:
        console.print_stdout(result.stdout)
    if result.stderr:
        console.print_stderr(result.stderr)

    files_changed = result.input != result.output
    if files_changed:
        console.print_stdout(f"✓ Formatted {len(field_sets)} target(s)")
    else:
        console.print_stdout(f"✓ {len(field_sets)} target(s) already formatted")

    return BaselineFmt(exit_code=0)


def rules() -> Iterable:
    """Return all fmt goal rules."""
    return collect_rules()
