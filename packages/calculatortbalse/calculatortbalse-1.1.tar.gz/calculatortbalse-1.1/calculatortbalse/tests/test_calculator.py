import pytest
from ..calculator import Calculator
import random
import math


random.seed(5)
SMALL_UPPER_BOUND = 1
SMALL_LOWER_BOUND = -1
BIG_UPPER_BOUND = 10000
BIG_LOWER_BOUND = -10000
TOLERANCE = 0.001
TEST_REPEAT_COUNT = 100


def get_float(calculator_output: str) -> float:
    """Get float from Calculator output string."""
    return float(calculator_output.split()[-1])


def test_operations():
    """Test add, subtract, multiply, divide operations
    with big and small numbers.
    """
    calculator_memory = 1.0
    calculator = Calculator(calculator_memory)
    operations_available = ["add", "subtract", "multiply", "divide"]
    operations_order = random.choices(operations_available, k=TEST_REPEAT_COUNT)
    small_numbers = lambda: random.uniform(SMALL_LOWER_BOUND, SMALL_UPPER_BOUND)
    big_numbers = lambda: random.uniform(BIG_LOWER_BOUND, BIG_UPPER_BOUND)

    for operation in operations_order:
        number = random.choice((small_numbers(), big_numbers()))
        calculator_function = getattr(calculator, operation)
        function_output = get_float(calculator_function(number))
        if operation == "add":
            assert math.isclose(calculator_memory + number, function_output, abs_tol=TOLERANCE)
        elif operation == "subtract":
            assert math.isclose(calculator_memory - number, function_output, abs_tol=TOLERANCE)
        elif operation == "multiply":
            assert math.isclose(calculator_memory * number, function_output, abs_tol=TOLERANCE)
        elif operation == "divide":
            assert math.isclose(calculator_memory / number, function_output, abs_tol=TOLERANCE)

        calculator_memory = function_output


def test_root_and_reset():
    """Test the root and reset operations."""
    calculator_memory = -1.0
    calculator = Calculator(calculator_memory)
    # Root of a negative number should raise a Value Error.
    with pytest.raises(ValueError):
        calculator.root(2)

    small_numbers = lambda: random.uniform(0, SMALL_UPPER_BOUND)
    big_numbers = lambda: random.uniform(0, BIG_UPPER_BOUND)
    for _ in range(TEST_REPEAT_COUNT):
        calculator_memory = random.choice((small_numbers(), big_numbers()))
        degree = random.choice((small_numbers(), big_numbers()))
        calculator.reset(calculator_memory)
        function_output = get_float(calculator.root(degree))
        assert math.isclose(calculator_memory ** (1 / degree), function_output, abs_tol=TOLERANCE)


def test_operations_zero():
    """Test Calculator operations with zero as input."""
    ZERO = 0

    calculator = Calculator(ZERO)
    calculator_output = get_float(str(calculator))
    assert calculator_output == ZERO

    calculator_output = get_float(calculator.add(ZERO))
    assert calculator_output == ZERO

    calculator_output = get_float(calculator.subtract(ZERO))
    assert calculator_output == ZERO

    calculator_output = get_float(calculator.multiply(ZERO))
    assert calculator_output == ZERO

    with pytest.raises(ZeroDivisionError):
        calculator.divide(ZERO)

    with pytest.raises(ZeroDivisionError):
        calculator.root(ZERO)


def test_types():
    """Test that Calculator raises appropriate error when
    non-float/int is given.
    """
    test_types = ["hi", [5], {"number": 5}]
    test_errors = [ValueError, TypeError, TypeError]

    for test_type, test_error in zip(test_types, test_errors):
        with pytest.raises(test_error):
            calculator = Calculator(test_type)

        calculator = Calculator()
        with pytest.raises(test_error):
            calculator.add(test_type)
        with pytest.raises(test_error):
            calculator.subtract(test_type)
        with pytest.raises(test_error):
            calculator.multiply(test_type)
        with pytest.raises(test_error):
            calculator.divide(test_type)
        with pytest.raises(test_error):
            calculator.root(test_type)
        with pytest.raises(test_error):
            calculator.reset(test_type)
