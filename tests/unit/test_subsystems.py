"""Unit tests for subsystem configurations."""

from __future__ import annotations

import pytest

from pants_baseline.subsystems.baseline import BaselineSubsystem
from pants_baseline.subsystems.ruff import RuffSubsystem
from pants_baseline.subsystems.ty import TySubsystem
from pants_baseline.subsystems.uv import UvSubsystem


class TestBaselineSubsystem:
    """Tests for BaselineSubsystem."""

    def test_default_values(self) -> None:
        """Test that default values are set correctly."""
        # Note: In actual Pants testing, you'd use RuleRunner to test subsystems
        # This is a simplified test showing the expected defaults
        assert BaselineSubsystem.enabled.default is True
        assert BaselineSubsystem.python_version.default == "3.11"
        assert BaselineSubsystem.line_length.default == 120
        assert BaselineSubsystem.coverage_threshold.default == 80
        assert BaselineSubsystem.strict_mode.default is True

    def test_src_roots_default(self) -> None:
        """Test default source roots."""
        assert "src" in BaselineSubsystem.src_roots.default

    def test_test_roots_default(self) -> None:
        """Test default test roots."""
        assert "tests" in BaselineSubsystem.test_roots.default

    def test_exclude_patterns_default(self) -> None:
        """Test default exclude patterns."""
        excludes = BaselineSubsystem.exclude_patterns.default
        assert ".venv" in excludes
        assert "__pycache__" in excludes
        assert ".git" in excludes


class TestRuffSubsystem:
    """Tests for RuffSubsystem."""

    def test_default_version(self) -> None:
        """Test default Ruff version."""
        assert RuffSubsystem.version.default == "0.2.0"

    def test_default_select_rules(self) -> None:
        """Test default selected lint rules."""
        select = RuffSubsystem.select.default
        # Core rules should be enabled by default
        assert "E" in select  # pycodestyle errors
        assert "F" in select  # pyflakes
        assert "I" in select  # isort
        assert "B" in select  # flake8-bugbear

    def test_default_ignore_rules(self) -> None:
        """Test default ignored rules."""
        ignore = RuffSubsystem.ignore.default
        assert "E501" in ignore  # line too long

    def test_default_formatting_options(self) -> None:
        """Test default formatting options."""
        assert RuffSubsystem.quote_style.default == "double"
        assert RuffSubsystem.indent_style.default == "space"

    def test_default_fix_options(self) -> None:
        """Test default fix options."""
        assert RuffSubsystem.fix.default is True
        assert RuffSubsystem.unsafe_fixes.default is False


class TestTySubsystem:
    """Tests for TySubsystem."""

    def test_default_version(self) -> None:
        """Test default ty version."""
        assert TySubsystem.version.default == "0.1.0"

    def test_default_strict_mode(self) -> None:
        """Test default strict mode."""
        assert TySubsystem.strict.default is True

    def test_default_reporting_options(self) -> None:
        """Test default reporting options."""
        assert TySubsystem.report_missing_imports.default is True
        assert TySubsystem.report_unused_imports.default is True
        assert TySubsystem.report_unused_variables.default is True

    def test_default_include_paths(self) -> None:
        """Test default include paths."""
        include = TySubsystem.include.default
        assert "src" in include
        assert "tests" in include

    def test_default_output_format(self) -> None:
        """Test default output format."""
        assert TySubsystem.output_format.default == "text"


class TestUvSubsystem:
    """Tests for UvSubsystem."""

    def test_default_version(self) -> None:
        """Test default uv version."""
        assert UvSubsystem.version.default == "0.5.0"

    def test_default_audit_enabled(self) -> None:
        """Test audit is enabled by default."""
        assert UvSubsystem.audit_enabled.default is True

    def test_default_lock_file(self) -> None:
        """Test default lock file path."""
        assert UvSubsystem.lock_file.default == "uv.lock"

    def test_default_require_lock(self) -> None:
        """Test lock file is required by default."""
        assert UvSubsystem.require_lock.default is True

    def test_default_output_format(self) -> None:
        """Test default output format."""
        assert UvSubsystem.output_format.default == "text"

    def test_default_ignore_vulns_empty(self) -> None:
        """Test no vulnerabilities ignored by default."""
        assert UvSubsystem.audit_ignore_vulns.default == []
