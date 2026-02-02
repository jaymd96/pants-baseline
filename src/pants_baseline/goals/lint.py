"""Lint goal for Ruff linting."""

from __future__ import annotations

from typing import Iterable

from pants.core.goals.lint import LintResult
from pants.engine.console import Console
from pants.engine.goal import Goal, GoalSubsystem
from pants.engine.rules import Get, collect_rules, goal_rule
from pants.engine.target import FieldSet, FilteredTargets

from pants_baseline.rules.lint_rules import RuffLintFieldSet, RuffLintRequest
from pants_baseline.subsystems.baseline import BaselineSubsystem
from pants_baseline.subsystems.ruff import RuffSubsystem
from pants_baseline.targets import BaselineSourcesField


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
    targets: FilteredTargets,
    baseline_subsystem: BaselineSubsystem,
    ruff_subsystem: RuffSubsystem,
) -> BaselineLint:
    """Run Ruff linting on all targets."""
    if not baseline_subsystem.enabled:
        console.print_stdout("Python baseline is disabled.")
        return BaselineLint(exit_code=0)

    # Filter targets that have BaselineSourcesField
    applicable_targets = [
        t for t in targets
        if t.has_field(BaselineSourcesField)
    ]

    if not applicable_targets:
        console.print_stdout("No baseline_python_project targets found.")
        return BaselineLint(exit_code=0)

    # Create field sets for each target
    field_sets = [
        RuffLintFieldSet.create(t)
        for t in applicable_targets
    ]

    # Create the lint request and run it
    request = RuffLintRequest(field_sets)
    result = await Get(LintResult, RuffLintRequest, request)

    # Print results
    if result.stdout:
        console.print_stdout(result.stdout)
    if result.stderr:
        console.print_stderr(result.stderr)

    if result.exit_code == 0:
        console.print_stdout(f"✓ Linted {len(field_sets)} target(s) successfully")
    else:
        console.print_stderr(f"✗ Linting failed with exit code {result.exit_code}")

    return BaselineLint(exit_code=result.exit_code)


def rules() -> Iterable:
    """Return all lint goal rules."""
    return collect_rules()
