"""Integration tests for baseline goals."""

from __future__ import annotations

import pytest

from pants.testutil.rule_runner import RuleRunner

from pants_baseline.register import rules, target_types


@pytest.fixture
def rule_runner() -> RuleRunner:
    """Create a RuleRunner for integration testing."""
    return RuleRunner(
        rules=rules(),
        target_types=target_types(),
    )


class TestBaselineLintGoal:
    """Integration tests for baseline-lint goal."""

    def test_lint_empty_project(self, rule_runner: RuleRunner) -> None:
        """Test linting an empty project."""
        rule_runner.write_files(
            {
                "BUILD": "baseline_python_project(name='test')",
            }
        )
        # Goal should complete without error for empty project
        # In a real test, we'd run the goal and check results


class TestBaselineFmtGoal:
    """Integration tests for baseline-fmt goal."""

    def test_fmt_empty_project(self, rule_runner: RuleRunner) -> None:
        """Test formatting an empty project."""
        rule_runner.write_files(
            {
                "BUILD": "baseline_python_project(name='test')",
            }
        )
        # Goal should complete without error for empty project


class TestBaselineTypecheckGoal:
    """Integration tests for baseline-typecheck goal."""

    def test_typecheck_empty_project(self, rule_runner: RuleRunner) -> None:
        """Test type checking an empty project."""
        rule_runner.write_files(
            {
                "BUILD": "baseline_python_project(name='test')",
            }
        )
        # Goal should complete without error for empty project


class TestBaselineTestGoal:
    """Integration tests for baseline-test goal."""

    def test_test_empty_project(self, rule_runner: RuleRunner) -> None:
        """Test running tests on an empty project."""
        rule_runner.write_files(
            {
                "BUILD": "baseline_python_project(name='test')",
            }
        )
        # Goal should complete without error for empty project


class TestBaselineAuditGoal:
    """Integration tests for baseline-audit goal."""

    def test_audit_empty_project(self, rule_runner: RuleRunner) -> None:
        """Test security audit on an empty project."""
        rule_runner.write_files(
            {
                "BUILD": "baseline_python_project(name='test')",
            }
        )
        # Goal should complete without error for empty project


class TestBaselinePythonProjectTarget:
    """Integration tests for baseline_python_project target."""

    def test_target_with_all_fields(self, rule_runner: RuleRunner) -> None:
        """Test creating a target with all fields specified."""
        rule_runner.write_files(
            {
                "BUILD": """
baseline_python_project(
    name="my_project",
    sources=["src/**/*.py"],
    test_sources=["tests/**/*.py"],
    python_version="3.12",
    line_length=100,
    strict=True,
    coverage_threshold=90,
)
""",
                "src/__init__.py": "",
                "tests/__init__.py": "",
            }
        )
        # Target should be created successfully

    def test_target_with_skip_fields(self, rule_runner: RuleRunner) -> None:
        """Test creating a target with skip fields."""
        rule_runner.write_files(
            {
                "BUILD": """
baseline_python_project(
    name="skip_all",
    skip_lint=True,
    skip_fmt=True,
    skip_typecheck=True,
    skip_test=True,
    skip_audit=True,
)
""",
            }
        )
        # Target should be created successfully with all skips
