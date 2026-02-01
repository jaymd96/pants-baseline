"""Unit tests for target types."""

from __future__ import annotations

import pytest

from pants_baseline.targets import (
    BaselinePythonProject,
    BaselineSourcesField,
    BaselineTestSourcesField,
    CoverageThresholdField,
    LineLengthField,
    PythonVersionField,
    SkipAuditField,
    SkipFormatField,
    SkipLintField,
    SkipTestField,
    SkipTypecheckField,
    StrictModeField,
)


class TestBaselinePythonProject:
    """Tests for BaselinePythonProject target."""

    def test_target_alias(self) -> None:
        """Test target alias is correct."""
        assert BaselinePythonProject.alias == "baseline_python_project"

    def test_has_required_fields(self) -> None:
        """Test that target has all required fields."""
        field_types = {f.__class__.__name__ for f in BaselinePythonProject.core_fields}

        # Check for baseline-specific fields
        assert "BaselineSourcesField" in str(BaselinePythonProject.core_fields)
        assert "BaselineTestSourcesField" in str(BaselinePythonProject.core_fields)


class TestBaselineSourcesField:
    """Tests for BaselineSourcesField."""

    def test_alias(self) -> None:
        """Test field alias."""
        assert BaselineSourcesField.alias == "sources"

    def test_default_pattern(self) -> None:
        """Test default source pattern."""
        assert BaselineSourcesField.default == ("**/*.py",)


class TestBaselineTestSourcesField:
    """Tests for BaselineTestSourcesField."""

    def test_alias(self) -> None:
        """Test field alias."""
        assert BaselineTestSourcesField.alias == "test_sources"

    def test_default_pattern(self) -> None:
        """Test default test pattern."""
        assert BaselineTestSourcesField.default == ("tests/**/*.py",)


class TestPythonVersionField:
    """Tests for PythonVersionField."""

    def test_alias(self) -> None:
        """Test field alias."""
        assert PythonVersionField.alias == "python_version"

    def test_default_version(self) -> None:
        """Test default Python version."""
        assert PythonVersionField.default == "3.11"


class TestLineLengthField:
    """Tests for LineLengthField."""

    def test_alias(self) -> None:
        """Test field alias."""
        assert LineLengthField.alias == "line_length"

    def test_default_length(self) -> None:
        """Test default line length."""
        assert LineLengthField.default == 120


class TestStrictModeField:
    """Tests for StrictModeField."""

    def test_alias(self) -> None:
        """Test field alias."""
        assert StrictModeField.alias == "strict"

    def test_default_enabled(self) -> None:
        """Test strict mode enabled by default."""
        assert StrictModeField.default is True


class TestCoverageThresholdField:
    """Tests for CoverageThresholdField."""

    def test_alias(self) -> None:
        """Test field alias."""
        assert CoverageThresholdField.alias == "coverage_threshold"

    def test_default_threshold(self) -> None:
        """Test default coverage threshold."""
        assert CoverageThresholdField.default == 80


class TestSkipFields:
    """Tests for skip fields."""

    def test_skip_lint_default(self) -> None:
        """Test skip_lint default is False."""
        assert SkipLintField.default is False

    def test_skip_fmt_default(self) -> None:
        """Test skip_fmt default is False."""
        assert SkipFormatField.default is False

    def test_skip_typecheck_default(self) -> None:
        """Test skip_typecheck default is False."""
        assert SkipTypecheckField.default is False

    def test_skip_test_default(self) -> None:
        """Test skip_test default is False."""
        assert SkipTestField.default is False

    def test_skip_audit_default(self) -> None:
        """Test skip_audit default is False."""
        assert SkipAuditField.default is False
