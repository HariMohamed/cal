import pytest

from Cal import Calculator as CalCalculator
from Calculator import Calculator, add, divide, multiply, subtract


def test_basic_operations_with_class_methods() -> None:
    assert Calculator.add(2, 3) == 5
    assert Calculator.subtract(8, 3) == 5
    assert Calculator.multiply(4, 3) == 12
    assert Calculator.divide(10, 2) == 5


def test_basic_operations_with_module_functions() -> None:
    assert add(2, 3) == 5
    assert subtract(8, 3) == 5
    assert multiply(4, 3) == 12
    assert divide(10, 2) == 5


def test_division_by_zero_raises() -> None:
    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
        divide(4, 0)


@pytest.mark.parametrize(
    "a,b",
    [("1", 2), (1, "2"), (None, 2), (2, object())],
)
def test_invalid_types_raise_type_error(a, b) -> None:
    with pytest.raises(TypeError, match="must be a real number"):
        add(a, b)


def test_cal_module_exports_the_same_calculator_class() -> None:
    assert CalCalculator is Calculator
