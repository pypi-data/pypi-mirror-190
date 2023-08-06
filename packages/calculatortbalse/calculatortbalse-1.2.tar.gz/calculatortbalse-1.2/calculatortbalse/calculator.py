from typing import  TypeVar

TCalculator = TypeVar("TCalculator", bound="Calculator")

class Calculator:
    """Calculator with internal memory.

    The calculator is capable of addition, subtraction, multiplication,
    division, taking n-th root, reseting internal memory.

    Parameters
    ----------
    memory: float, default=0
        initial internal memory used for all arithmetic operations.

    Examples
    --------
    >>> calculator = Calculator(2)
    >>> print(calculator)
    Currently calculator reads: 2.0
    >>> calculator.answer()
    2.0
    >>> calculator.add(2)
    Currently calculator reads: 4.0
    >>> calculator.subtract(1)
    Currently calculator reads: 3.0
    >>> calculator.multiply(5)
    Currently calculator reads: 15.0
    >>> calculator.divide(2.5)
    Currently calculator reads: 6.0
    >>> calculator.root(3)
    Currently calculator reads: 1.8171205928321397
    >>> calculator.reset()
    >>> print(calculator)
    Currently calculator reads: 0.0
    >>> calculator.add(5).multiply(5).root(2).answer()
    5.0
    """

    def __init__(self, memory=0.0) -> None:
        self.__memory = float(memory)

    def __str__(self) -> str:
        return f"Currently calculator reads: {self.__memory}"

    def __repr__(self) -> str:
        return str(self)

    def add(self: TCalculator, number: float) -> TCalculator:
        """Addition arithmetic operation.

        Adds provided number to internal memory. 
        Returns self for further operations.
        """
        self.__memory += float(number)
        return self

    def subtract(self: TCalculator, number: float) -> TCalculator:
        """Subtraction arithmetic operation.

        Subtracts provided number from internal memory.
        Returns self for further operations.
        """
        self.__memory -= float(number)
        return self

    def multiply(self: TCalculator, number: float) -> TCalculator:
        """Multiplication arithmetic operation.

        Multiplies provided number by number stored in internal memory.
        Returns self for further operations.
        """
        self.__memory *= float(number)
        return self

    def divide(self: TCalculator, number: float) -> TCalculator:
        """Division arithmetic operation.

        Divides the number stored in internal memory by the provided number.
        Returns self for further operations.
        """
        self.__memory /= float(number)
        return self

    def root(self: TCalculator, degree: float) -> TCalculator:
        """Take n-th degree root.

        Takes n-th degree root of the number stored in internal memory.
        Can only take roots of positive numbers.
        Returns self for further operations.

        Raises
        ------
        ValueError: if value in memory is negative.
        """
        if self.__memory < 0:
            raise ValueError("Can only take roots of positive numbers.")
        self.__memory = self.__memory ** (1 / float(degree))
        return self

    def reset(self, memory=0.0) -> None:
        """Reset internal memory.

        Takes provided number and stores it in internal memory, overriding
        the previous value.
        """
        self.__memory = float(memory)

    def answer(self) -> float:
        """Return number stored in memory as float"""
        return self.__memory


if __name__ == "__main__":
    import doctest

    print(doctest.testmod())
