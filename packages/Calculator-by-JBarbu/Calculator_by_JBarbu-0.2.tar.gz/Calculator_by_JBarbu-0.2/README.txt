# Calculator package description

## Introduction

Module calculator in this package should be used as a mini calculator version which has severeal functions: addition, subtraction, multiplication, division,
taking (n) root of a number and making changes to calculator memory. It is a very simple package and might be used as a prototype on how to structure your 
created packages.

## Installation

For installing the package use command

`pip install Calculator-by-JBarbu==0.2`

All the dependencies will be installed together with the package installation.

## Usage

Below are several examples and key concepts on how to use the module:

`import calc`			                      imports the module

`cal = calc.calculator.Calculator()`		creates class instance

Use functions add, subtract, multiply, divide and nth_root to make calculations. The calculations are made based on the two arguments provided in the function, 
if only one argument is provided, the second one is taken from calculator memory. Functions set_memory and reset_memory work with calculator memory.

## API reference

### Class

`class Calculator`

Calculator class where all attributes and functions are defined. It has 1 attribute and 7 functions available.

### Attributes

`self.memory = 0.0`

Single class attribute to be used as calculators memory. Whenever an instance is created, the memory is set to be 0.

### Methods

*Set memory*

```
def set_memory(self, x: float):
    self.memory = x
```
Changes the number set in calculator memory. When instance is created, the initial value stored in memory is 0. Function takes the number provided as an 
argument and stores it into memory.

*Reset memory*

```
def reset_memory(self):
    self.memory = 0.0
```
Resets the number set in the calculator memory to 0.

*Addition*

```
def add(self, a: float, b: Optional[float] = None) -> float:
    if b is None:
        b = self.memory
    self.memory = a + b
    return self.memory
```
Function calculates the sum of two numbers. Function adds both arguments, in case only one argument is provided, second one is taken from calculator memory.
The result is stored in the calculator memory.

*Subtraction*

```
def subtract(self, a: float, b: Optional[float] = None) -> float:
    if b is None:
        b = self.memory
        self.memory = b - a
    else:
        self.memory = a - b
    return self.memory
```
Function subtracts number provided as the first argument from second. In case only one argument is provided, first argument is taken from calculator memory.
The result is stored in the calculator memory.

*Multiplication*

```
def multiply(self, a: float, b: Optional[float] = None) -> float:
    if b is None:
        b = self.memory
    self.memory = a * b
    return self.memory
```
Function multiplies two numbers provided as arguments. In case only one argument is provided, second one is taken from calculatorvmemory. The result is stored
in the calculator memory.

*Division*

```
def divide(self, a: float, b: Optional[float] = None) -> float:
    if b is None:
        b = self.memory
        if a == 0:
            raise ValueError("Division by zero not possible")
        else:
            self.memory = b / a
    elif b == 0.0:
        raise ValueError("Division by zero not possible")
    else:
        self.memory = a / b
    return self.memory
```
Function divides number provided as the first argument from second. In case only one argument is provided, first argument is taken from calculator memory.
The result is stored in the calculator memory. In case argument provided is 0, function raises ValueError as division by 0 is not possible.

*(N) root of number*

```
def nth_root(self, a: float, b: Optional[float] = None) -> float:
    if b is None:
        b = self.memory
        if a == 0:
            self.memory = pow(b, a)
        elif b < 0 and a % 2 == 0:
            raise ValueError("Even root of negative number is not a real number")
        else:
            self.memory = pow(b, 1/a)
    else:
        if b == 0:
            self.memory = pow(a, b)
        elif a < 0 and b % 2 == 0:
            raise ValueError("Even root of negative number is not a real number")
        else:
            self.memory = pow(a, 1/b)
    return self.memory
```
Function calculates (n) root of the number. First argument is used as radicand and second argument is used as a degree. In case only one argument is provided,
it is used as a degree. In case the argument provided is 0, function takes root of degree 0. If radicant is negative and degree is even, function raises
ValueError as even root of negative number is not a real number.

## Contributing

In case any bugs need to be reported or code contributions are to be made, please contact the developer via email.

## License

The MIT License (MIT)

Copyright (c) 2023 Justas Barbuska

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

## Acknowledgments

Module uses mypy for type hinting and doctest to perform tests.
