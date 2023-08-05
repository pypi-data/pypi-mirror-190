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
    >>> calculator.add(2)
    'Currently calculator reads: 4.0'
    >>> calculator.subtract(1)
    'Currently calculator reads: 3.0'
    >>> calculator.multiply(5)
    'Currently calculator reads: 15.0'
    >>> calculator.divide(2.5)
    'Currently calculator reads: 6.0'
    >>> calculator.root(3)
    'Currently calculator reads: 1.8171205928321397'
    >>> calculator.reset()
    >>> print(calculator)
    Currently calculator reads: 0.0
    """

    def __init__(self, memory=0.0) -> None:
        self.__memory = float(memory)

    def __str__(self) -> str:
        return f"Currently calculator reads: {self.__memory}"

    def add(self, number: float) -> str:
        """Addition arithmetic operation.

        Adds provided number to internal memory and returns the
        result as string.
        """
        self.__memory += float(number)
        return str(self)

    def subtract(self, number: float) -> str:
        """Subtraction arithmetic operation.

        Subtracts provided number from internal memory and returns the
        result as string.
        """
        self.__memory -= float(number)
        return str(self)

    def multiply(self, number: float) -> str:
        """Multiplication arithmetic operation.

        Multiplies provided number by number stored in internal memory.
        Returns the result as string.
        """
        self.__memory *= float(number)
        return str(self)

    def divide(self, number: float) -> str:
        """Division arithmetic operation.

        Divides the number stored in internal memory by the provided number.
        Returns the result as string.
        """
        self.__memory /= float(number)
        return str(self)

    def root(self, degree: float) -> str:
        """Take n-th degree root.

        Takes n-th degree root of the number stored in internal memory.
        Can only take roots of positive numbers.
        Returns the result as string.
        """
        if self.__memory < 0:
            raise ValueError("Can only take roots of positive numbers.")
        self.__memory = self.__memory ** (1 / float(degree))
        return str(self)

    def reset(self, memory=0.0) -> None:
        """Reset internal memory.

        Takes provided number and stores it in internal memory, overriding
        the previous value.
        """
        self.__memory = float(memory)


if __name__ == "__main__":
    import doctest

    print(doctest.testmod())
