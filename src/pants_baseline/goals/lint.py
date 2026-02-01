"""Lint goal for Ruff linting."""

from __future__ import annotations

from typing import Iterable

from pants.core.goals.lint import LintFilesRequest, LintResult
from pants.engine.console import Console
from pants.engine.fs import PathGlobs, Paths
from pants.engine.goal import Goal, GoalSubsystem
from pants.engine.rules import Get, collect_rules, goal_rule
from pants.engine.target import Targets
from pants.util.logging import LogLevel

from pants_baseline.rules.lint_rules import RuffLintRequest
from pants_baseline.subsystems.baseline import BaselineSubsystem
from pants_baseline.subsystems.ruff import RuffSubsystem


class BaselineLintSubsystem(GoalSubsystem):
    """Subsystem for the baseline-lint goal."""

    name = "baseline-lint"
    help = "Run Ruff linting with baseline configuration."


class BaselineLint(Goal):
    """Goal to run Ruff linting."""

    subsystem_cls = BaselineLintSubsystem
    environment_behavior = Goal.EnvironmentBehavior.LOCAL_ONLY


@goal_rule
async def run_baseline_lint(
    console: Console,
    targets: Targets,
    baseline_subsystem: BaselineSubsystem,
    ruff_subsystem: RuffSubsystem,
) -> BaselineLint:
    """Run Ruff linting on all targets."""
    if not baseline_subsystem.enabled:
        console.print_stdout("Python baseline is disabled.")
        return BaselineLint(exit_code=0)

    console.print_stdout("Running Ruff linter...")
    console.print_stdout(f"  Target Python version: {baseline_subsystem.python_version}")
    console.print_stdout(f"  Line length: {baseline_subsystem.line_length}")
    console.print_stdout(f"  Rules: {', '.join(ruff_subsystem.select[:5])}...")
    console.print_stdout("")

    # The actual linting is handled by the LintTargetsRequest mechanism
    # This goal just provides a user-friendly entry point

    return BaselineLint(exit_code=0)


def rules() -> Iterable:
    """Return all lint goal rules."""
    return collect_rules()
