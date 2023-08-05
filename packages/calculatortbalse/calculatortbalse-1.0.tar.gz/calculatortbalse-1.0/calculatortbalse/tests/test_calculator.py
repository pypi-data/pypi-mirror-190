import pytest
from ..calculator import Calculator
import random
import math


def get_float(calculator_output: str) -> float:
    """Get float from Calculator output string."""
    return float(calculator_output.split()[-1])


def test_operations():
    """Test add, subtract, multiply, divide operations
    with big and small numbers.
    """
    calc_memory = 1.0
    calc = Calculator(calc_memory)
    operations_available = ["add", "subtract", "multiply", "divide"]
    random.seed(5)
    operations_order = random.choices(operations_available, k=100)
    small_numbers = lambda: random.uniform(-1, 1)
    big_numbers = lambda: random.uniform(-10000, 10000)

    for operation in operations_order:
        number = random.choice((small_numbers(), big_numbers()))
        fun = getattr(calc, operation)
        function_output = get_float(fun(number))
        if operation == "add":
            assert math.isclose(calc_memory + number, function_output, abs_tol=0.001)
        elif operation == "subtract":
            assert math.isclose(calc_memory - number, function_output, abs_tol=0.001)
        elif operation == "multiply":
            assert math.isclose(calc_memory * number, function_output, abs_tol=0.001)
        elif operation == "divide":
            assert math.isclose(calc_memory / number, function_output, abs_tol=0.001)

        calc_memory = function_output


def test_root():
    """Test the root operation."""
    calc_memory = -1.0
    calc = Calculator(calc_memory)
    # Root of a negative number should raise a Value Error.
    with pytest.raises(ValueError):
        calc.root(2)

    random.seed(5)
    small_numbers = lambda: random.uniform(0, 1)
    big_numbers = lambda: random.uniform(0, 10000)
    for _ in range(100):
        calc_memory = random.choice((small_numbers(), big_numbers()))
        degree = random.choice((small_numbers(), big_numbers()))
        calc.reset(calc_memory)
        function_output = get_float(calc.root(degree))
        assert math.isclose(calc_memory ** (1 / degree), function_output, abs_tol=0.001)


def test_operations_zero():
    """Test Calculator operations with zero as input."""
    number = 0.0

    calc = Calculator(number)
    calculator_output = get_float(str(calc))
    assert calculator_output == number

    calculator_output = get_float(calc.add(0))
    assert calculator_output == number

    calculator_output = get_float(calc.subtract(0))
    assert calculator_output == number

    calculator_output = get_float(calc.multiply(0))
    assert calculator_output == number

    with pytest.raises(ZeroDivisionError):
        calc.divide(number)

    with pytest.raises(ZeroDivisionError):
        calc.root(number)


def test_types():
    """Test that Calculator raises appropriate error when
    non-float/int is given.
    """
    test_types = ["hi", [5], {"number": 5}]
    test_errors = [ValueError, TypeError, TypeError]

    for test_type, test_error in zip(test_types, test_errors):
        with pytest.raises(test_error):
            calc = Calculator(test_type)
        calc = Calculator()
        with pytest.raises(test_error):
            calc.add(test_type)
        with pytest.raises(test_error):
            calc.subtract(test_type)
        with pytest.raises(test_error):
            calc.multiply(test_type)
        with pytest.raises(test_error):
            calc.divide(test_type)
        with pytest.raises(test_error):
            calc.root(test_type)
        with pytest.raises(test_error):
            calc.reset(test_type)
