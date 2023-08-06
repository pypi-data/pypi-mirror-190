# Part 5: Calculator

### A project at Turing College

## Installing the package

    pip install calculatortbalse

## Testing the package

After installation, you can launch the test suite from outside the package directory.

    pytest calculatortbalse

## Using the package

### Initiate Calculator object

Calculator has internal memory, initiated at 0.0 by default. All methods can work with any float or int.

```Python
>>> calculator = Calculator()
>>> print(calculator)
Currently calculator reads: 0.0
```

However, you can pass in a number that will be stored in memory instead of 0.0.

```Python
>>> calculator = Calculator(2)
>>> print(calculator)
Currently calculator reads: 2.0
```

### Reset internal memory

Similar to initiating a Calculator object, reset method can store the provided float in memory. Resets to 0.0 if no value is given.

```Python
>>> calculator.reset()
>>> print(calculator)
Currently calculator reads: 0.0
```

### Perform addition, subtraction, multiplication and division

add, subtract, multiply, divide methods accept any float.

```Python
>>> calculator.reset()
>>> calculator.add(2)
Currently calculator reads: 2.0
>>> calculator.subtract(1)
Currently calculator reads: 1.0
>>> calculator.multiply(9)
Currently calculator reads: 9.0
>>> calculator.divide(3)
Currently calculator reads: 3.0
```

### Take n-th degree root

root method takes the n-th degree root of the number curently stored in memory. Can only take roots of positive numbers.

```Python
>>> calculator.reset(8)
>>> calculator.root(3)
Currently calculator reads: 2.0
```

### Chain multiple operations

add, subtract, multiply, divide, root methods can be chained together.

```Python
>>> calculator.reset()
>>> calculator.add(5).multiply(5).root(2)
Currently calculator reads: 5.0
```

### Receive answer as float

The math operations will return the calculator object itself by default. You can terminate the operations chain with the answer method to receive the answer as float.

```Python
>>> calculator.reset()
>>> calculator.add(5).multiply(5).root(2).answer()
5.0
```
