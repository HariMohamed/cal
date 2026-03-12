"""Calculator module with input validation and clear errors."""
from __future__ import annotations

from numbers import Real


def _validate_number(value: Real, name: str) -> None:
    if not isinstance(value, Real):
        raise TypeError(f"{name} must be a real number, got {type(value).__name__}.")


def _validate_pair(a: Real, b: Real) -> None:
    _validate_number(a, "a")
    _validate_number(b, "b")


class Calculator:
    """Simple calculator for basic arithmetic operations."""

    @staticmethod
    def add(a: Real, b: Real) -> Real:
        _validate_pair(a, b)
        return a + b

    @staticmethod
    def subtract(a: Real, b: Real) -> Real:
        _validate_pair(a, b)
        return a - b

    @staticmethod
    def multiply(a: Real, b: Real) -> Real:
        _validate_pair(a, b)
        return a * b

    @staticmethod
    def divide(a: Real, b: Real) -> float:
        _validate_pair(a, b)
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return a / b


def add(a: Real, b: Real) -> Real:
    return Calculator.add(a, b)


def subtract(a: Real, b: Real) -> Real:
    return Calculator.subtract(a, b)


def multiply(a: Real, b: Real) -> Real:
    return Calculator.multiply(a, b)


def divide(a: Real, b: Real) -> float:
    return Calculator.divide(a, b)
