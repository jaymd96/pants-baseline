"""Register the Python Baseline plugin with Pants.

This module is the entry point for the Pants plugin system.
It registers all rules, targets, and subsystems provided by this plugin.
"""

from typing import Iterable

from pants.engine.rules import Rule, collect_rules

from pants_baseline.goals import audit as audit_goal
from pants_baseline.goals import fmt as fmt_goal
from pants_baseline.goals import lint as lint_goal
from pants_baseline.goals import test as test_goal
from pants_baseline.goals import typecheck as typecheck_goal
from pants_baseline.rules import audit_rules, fmt_rules, lint_rules, test_rules, typecheck_rules
from pants_baseline.subsystems.baseline import BaselineSubsystem
from pants_baseline.subsystems.ruff import RuffSubsystem
from pants_baseline.subsystems.ty import TySubsystem
from pants_baseline.subsystems.uv import UvSubsystem
from pants_baseline.targets import BaselinePythonProject


def rules() -> Iterable[Rule]:
    """Return all rules provided by this plugin."""
    return [
        *collect_rules(lint_rules),
        *collect_rules(fmt_rules),
        *collect_rules(typecheck_rules),
        *collect_rules(test_rules),
        *collect_rules(audit_rules),
        *collect_rules(lint_goal),
        *collect_rules(fmt_goal),
        *collect_rules(typecheck_goal),
        *collect_rules(test_goal),
        *collect_rules(audit_goal),
        *BaselineSubsystem.rules(),
        *RuffSubsystem.rules(),
        *TySubsystem.rules(),
        *UvSubsystem.rules(),
    ]


def target_types() -> Iterable[type]:
    """Return all custom target types provided by this plugin."""
    return [BaselinePythonProject]
