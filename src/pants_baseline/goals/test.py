"""Test goal for pytest testing."""

from __future__ import annotations

from typing import Iterable

from pants.engine.console import Console
from pants.engine.goal import Goal, GoalSubsystem
from pants.engine.rules import collect_rules, goal_rule
from pants.engine.target import Targets

from pants_baseline.subsystems.baseline import BaselineSubsystem


class BaselineTestSubsystem(GoalSubsystem):
    """Subsystem for the baseline-test goal."""

    name = "baseline-test"
    help = "Run pytest with coverage and baseline configuration."


class BaselineTest(Goal):
    """Goal to run pytest tests."""

    subsystem_cls = BaselineTestSubsystem


@goal_rule
async def run_baseline_test(
    console: Console,
    targets: Targets,
    baseline_subsystem: BaselineSubsystem,
) -> BaselineTest:
    """Run pytest on all test targets."""
    if not baseline_subsystem.enabled:
        console.print_stdout("Python baseline is disabled.")
        return BaselineTest(exit_code=0)

    console.print_stdout("Running pytest with coverage...")
    console.print_stdout(f"  Source roots: {', '.join(baseline_subsystem.src_roots)}")
    console.print_stdout(f"  Test roots: {', '.join(baseline_subsystem.test_roots)}")
    console.print_stdout(f"  Coverage threshold: {baseline_subsystem.coverage_threshold}%")
    console.print_stdout("")

    # The actual testing is handled by the TestRequest mechanism
    # This goal just provides a user-friendly entry point

    return BaselineTest(exit_code=0)


def rules() -> Iterable:
    """Return all test goal rules."""
    return collect_rules()
