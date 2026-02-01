"""Target types for the Python Baseline plugin."""

from __future__ import annotations

from pants.engine.target import (
    COMMON_TARGET_FIELDS,
    BoolField,
    IntField,
    StringField,
    StringSequenceField,
    Target,
)


class BaselineSourcesField(StringSequenceField):
    """Source files for the baseline Python project."""

    alias = "sources"
    default = ("**/*.py",)
    help = "Python source files to include in baseline checks."


class BaselineTestSourcesField(StringSequenceField):
    """Test source files for the baseline Python project."""

    alias = "test_sources"
    default = ("tests/**/*.py",)
    help = "Test files to include in baseline checks."


class PythonVersionField(StringField):
    """Target Python version for the project."""

    alias = "python_version"
    default = "3.11"
    help = "Target Python version (e.g., '3.11', '3.12')."


class LineLengthField(IntField):
    """Maximum line length for formatting."""

    alias = "line_length"
    default = 120
    help = "Maximum line length for code formatting."


class StrictModeField(BoolField):
    """Enable strict mode for all checks."""

    alias = "strict"
    default = True
    help = "Enable strict mode for type checking and linting."


class CoverageThresholdField(IntField):
    """Minimum coverage percentage required."""

    alias = "coverage_threshold"
    default = 80
    help = "Minimum code coverage percentage required."


class SkipLintField(BoolField):
    """Skip linting for this target."""

    alias = "skip_lint"
    default = False
    help = "Skip Ruff linting for this target."


class SkipFormatField(BoolField):
    """Skip formatting for this target."""

    alias = "skip_fmt"
    default = False
    help = "Skip Ruff formatting for this target."


class SkipTypecheckField(BoolField):
    """Skip type checking for this target."""

    alias = "skip_typecheck"
    default = False
    help = "Skip ty type checking for this target."


class SkipTestField(BoolField):
    """Skip testing for this target."""

    alias = "skip_test"
    default = False
    help = "Skip pytest for this target."


class SkipAuditField(BoolField):
    """Skip security audit for this target."""

    alias = "skip_audit"
    default = False
    help = "Skip uv security audit for this target."


class BaselinePythonProject(Target):
    """A Python project with baseline quality checks.

    This target type enables opinionated code quality checks using the
    Astral ecosystem (Ruff, ty, uv) plus pytest for testing.

    Example:

        baseline_python_project(
            name="my_project",
            sources=["src/**/*.py"],
            test_sources=["tests/**/*.py"],
            python_version="3.11",
            line_length=120,
            strict=True,
            coverage_threshold=80,
        )
    """

    alias = "baseline_python_project"
    help = "A Python project with baseline quality checks."

    core_fields = (
        *COMMON_TARGET_FIELDS,
        BaselineSourcesField,
        BaselineTestSourcesField,
        PythonVersionField,
        LineLengthField,
        StrictModeField,
        CoverageThresholdField,
        SkipLintField,
        SkipFormatField,
        SkipTypecheckField,
        SkipTestField,
        SkipAuditField,
    )
