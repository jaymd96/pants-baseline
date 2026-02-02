"""Type check goal for ty type checking."""

from __future__ import annotations

from typing import Iterable

from pants.core.goals.check import CheckResults
from pants.engine.console import Console
from pants.engine.goal import Goal, GoalSubsystem
from pants.engine.rules import Get, collect_rules, goal_rule
from pants.engine.target import FilteredTargets

from pants_baseline.rules.typecheck_rules import TyCheckRequest, TyFieldSet
from pants_baseline.subsystems.baseline import BaselineSubsystem
from pants_baseline.subsystems.ty import TySubsystem
from pants_baseline.targets import BaselineSourcesField


class BaselineTypecheckSubsystem(GoalSubsystem):
    """Subsystem for the baseline-typecheck goal."""

    name = "baseline-typecheck"
    help = "Run ty type checking with baseline configuration."


class BaselineTypecheck(Goal):
    """Goal to run ty type checking."""

    subsystem_cls = BaselineTypecheckSubsystem
    environment_behavior = Goal.EnvironmentBehavior.LOCAL_ONLY


@goal_rule
async def run_baseline_typecheck(
    console: Console,
    targets: FilteredTargets,
    baseline_subsystem: BaselineSubsystem,
    ty_subsystem: TySubsystem,
) -> BaselineTypecheck:
    """Run ty type checking on all targets."""
    if not baseline_subsystem.enabled:
        console.print_stdout("Python baseline is disabled.")
        return BaselineTypecheck(exit_code=0)

    # Filter targets that have BaselineSourcesField
    applicable_targets = [
        t for t in targets
        if t.has_field(BaselineSourcesField)
    ]

    if not applicable_targets:
        console.print_stdout("No baseline_python_project targets found.")
        return BaselineTypecheck(exit_code=0)

    # Create field sets for each target
    field_sets = [
        TyFieldSet.create(t)
        for t in applicable_targets
    ]

    # Create the check request and run it
    request = TyCheckRequest(field_sets)
    results = await Get(CheckResults, TyCheckRequest, request)

    # Print results
    exit_code = 0
    for result in results.results:
        if result.stdout:
            console.print_stdout(result.stdout)
        if result.stderr:
            console.print_stderr(result.stderr)
        if result.exit_code != 0:
            exit_code = result.exit_code

    if exit_code == 0:
        console.print_stdout(f"✓ Type checked {len(field_sets)} target(s) successfully")
    else:
        console.print_stderr(f"✗ Type checking failed with exit code {exit_code}")

    return BaselineTypecheck(exit_code=exit_code)


def rules() -> Iterable:
    """Return all typecheck goal rules."""
    return collect_rules()
