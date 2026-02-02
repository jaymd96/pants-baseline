"""Register the Python Baseline plugin with Pants.

This module is the entry point for the Pants plugin system.
It registers all rules, targets, and subsystems provided by this plugin.
"""

from typing import Iterable

from pants.engine.rules import Rule

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
    """Return all rules provided by this plugin.

    Each module's rules() function returns both @rule decorated functions
    AND UnionRule registrations. We must call the rules() functions directly
    rather than using collect_rules() which only collects @rule functions.
    """
    return [
        *lint_rules.rules(),
        *fmt_rules.rules(),
        *typecheck_rules.rules(),
        *test_rules.rules(),
        *audit_rules.rules(),
        *lint_goal.rules(),
        *fmt_goal.rules(),
        *typecheck_goal.rules(),
        *test_goal.rules(),
        *audit_goal.rules(),
    ]


def target_types() -> Iterable[type]:
    """Return all custom target types provided by this plugin."""
    return [BaselinePythonProject]
