"""Pytest configuration and shared fixtures for Python Baseline plugin tests."""

from __future__ import annotations

import pytest

from pants.testutil.rule_runner import RuleRunner

from pants_baseline.register import rules, target_types


@pytest.fixture
def rule_runner() -> RuleRunner:
    """Create a RuleRunner with all Python Baseline rules and targets."""
    return RuleRunner(
        rules=rules(),
        target_types=target_types(),
    )


@pytest.fixture
def sample_python_source() -> str:
    """Return sample Python source code for testing."""
    return '''"""Sample module for testing."""

from typing import List


def greet(name: str) -> str:
    """Return a greeting message.

    Args:
        name: The name to greet.

    Returns:
        A greeting string.
    """
    return f"Hello, {name}!"


def add_numbers(numbers: List[int]) -> int:
    """Sum a list of numbers.

    Args:
        numbers: List of integers to sum.

    Returns:
        The sum of all numbers.
    """
    return sum(numbers)


class Calculator:
    """A simple calculator class."""

    def __init__(self, initial_value: int = 0) -> None:
        """Initialize the calculator.

        Args:
            initial_value: Starting value for calculations.
        """
        self.value = initial_value

    def add(self, x: int) -> int:
        """Add a number to the current value.

        Args:
            x: Number to add.

        Returns:
            The new value.
        """
        self.value += x
        return self.value

    def reset(self) -> None:
        """Reset the calculator to zero."""
        self.value = 0
'''


@pytest.fixture
def sample_test_source() -> str:
    """Return sample test code for testing."""
    return '''"""Tests for the sample module."""

import pytest

from sample import Calculator, add_numbers, greet


class TestGreet:
    """Tests for the greet function."""

    def test_greet_returns_greeting(self) -> None:
        """Test that greet returns a proper greeting."""
        result = greet("World")
        assert result == "Hello, World!"

    def test_greet_with_empty_string(self) -> None:
        """Test greet with empty string."""
        result = greet("")
        assert result == "Hello, !"


class TestAddNumbers:
    """Tests for the add_numbers function."""

    def test_add_numbers_with_list(self) -> None:
        """Test adding a list of numbers."""
        result = add_numbers([1, 2, 3, 4, 5])
        assert result == 15

    def test_add_numbers_empty_list(self) -> None:
        """Test adding an empty list."""
        result = add_numbers([])
        assert result == 0


class TestCalculator:
    """Tests for the Calculator class."""

    def test_calculator_initial_value(self) -> None:
        """Test calculator initialization."""
        calc = Calculator(10)
        assert calc.value == 10

    def test_calculator_add(self) -> None:
        """Test calculator add method."""
        calc = Calculator()
        result = calc.add(5)
        assert result == 5
        assert calc.value == 5

    def test_calculator_reset(self) -> None:
        """Test calculator reset method."""
        calc = Calculator(100)
        calc.reset()
        assert calc.value == 0
'''
