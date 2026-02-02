"""Register the Python Baseline plugin with Pants.

This module is the entry point for the Pants plugin system.
It registers all rules, targets, and subsystems provided by this plugin.

This plugin integrates with Pants' built-in lint, fmt, and check goals
rather than providing custom goals.
"""

from typing import Iterable, Type

from pants.engine.rules import Rule
from pants.option.subsystem import Subsystem

from pants_baseline.rules import fmt_rules, lint_rules
from pants_baseline.subsystems.baseline import BaselineSubsystem
from pants_baseline.subsystems.ruff import RuffSubsystem
from pants_baseline.targets import BaselinePythonProject


def rules() -> Iterable[Rule]:
    """Return all rules provided by this plugin.

    Each module's rules() function returns both @rule decorated functions
    AND UnionRule registrations. We must call the rules() functions directly
    rather than using collect_rules() which only collects @rule functions.
    """
    return [
        # Tool rules (integrate with Pants built-in lint/fmt goals)
        *lint_rules.rules(),
        *fmt_rules.rules(),
    ]


def target_types() -> Iterable[type]:
    """Return all custom target types provided by this plugin."""
    return [BaselinePythonProject]


def subsystems() -> Iterable[Type[Subsystem]]:
    """Return all subsystems provided by this plugin."""
    return [
        BaselineSubsystem,
        RuffSubsystem,
    ]
