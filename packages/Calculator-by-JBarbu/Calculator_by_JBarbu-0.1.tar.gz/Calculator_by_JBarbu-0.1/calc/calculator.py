from typing import Optional


class Calculator:
    def __init__(self):
        self.memory = 0.0

    def set_memory(self, x: float):
        ''' Changes the number set in calculator memory. When instance
        is created, the initial value stored in memory is 0. Functions
        takes the number provided as an argument and stores it into
        memory.

        For example:

            >>> calculator = Calculator() # creating calculator instance
            >>> calculator.memory
            0.0
            >>> calculator.set_memory(13.0)
            >>> calculator.memory
            13.0
        '''
        self.memory = x

    def reset_memory(self):
        ''' Resets the number set in the calculator memory to 0.

        For example:

            >>> calculator = Calculator() # creating calculator instance
            >>> calculator.set_memory(13.0)
            >>> calculator.memory
            13.0
            >>> calculator.reset_memory()
            >>> calculator.memory
            0.0
        '''
        self.memory = 0.0

    def add(self, a: float, b: Optional[float] = None) -> float:
        ''' Function calculates the sum of two numbers. Function adds both
        arguments, in case only one argument is provided, second one is
        taken from calculator memory. The result is stored in the calculator
        memory.

        For example:

            >>> calculator = Calculator() # creating calculator instance
            >>> calculator.add(6.7, 7.3)
            14.0
            >>> calculator.memory
            14.0
            >>> calculator.add(1.4)
            15.4
        '''
        if b is None:
            b = self.memory
        self.memory = a + b
        return self.memory

    def subtract(self, a: float, b: Optional[float] = None) -> float:
        ''' Function subtracts number provided as the first argument from
        second. In case only one argument is provided, first argument is taken
        from calculator memory. The result is stored in the calculator
        memory.

        For example:

            >>> calculator = Calculator() # creating calculator instance
            >>> calculator.subtract(14.3, 4.3)
            10.0
            >>> calculator.memory
            10.0
            >>> calculator.subtract(1.4)
            8.6
        '''
        if b is None:
            b = self.memory
            self.memory = b - a
        else:
            self.memory = a - b
        return self.memory

    def multiply(self, a: float, b: Optional[float] = None) -> float:
        ''' Function multiplies two numbers provided as arguments. In case
        only one argument is provided, second one is taken from calculator
        memory. The result is stored in the calculator memory.

        For example:

            >>> calculator = Calculator() # creating calculator instance
            >>> calculator.multiply(4.0, 2.5)
            10.0
            >>> calculator.memory
            10.0
            >>> calculator.multiply(3.4)
            34.0
        '''
        if b is None:
            b = self.memory
        self.memory = a * b
        return self.memory

    def divide(self, a: float, b: Optional[float] = None) -> float:
        ''' Function divides number provided as the first argument from
        second. In case only one argument is provided, first argument is taken
        from calculator memory. The result is stored in the calculator
        memory. In case argument provided is 0, function raises ValueError as
        division by 0 is not possible.

        For example:

            >>> calculator = Calculator() # creating calculator instance
            >>> calculator.divide(13.0, 2.0)
            6.5
            >>> calculator.memory
            6.5
            >>> calculator.divide(2.0)
            3.25
            >>> calculator.divide(0)
            Traceback (most recent call last):
            ...
            ValueError: Division by zero not possible
        '''
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

    def nth_root(self, a: float, b: Optional[float] = None) -> float:
        ''' Function calculates (n) root of the number. First argument is used
        as radicand and second argument is used as a degree. In case only one
        argument is provided, it is used as a degree. In case the
        argument provided is 0, function takes root of degree 0. If radicant
        is negative and degree is even, function raises ValueError as even
        root of negative number is not a real number.

        For example:

            >>> calculator = Calculator() # creating calculator instance
            >>> calculator.nth_root(16.0, 2.0)
            4.0
            >>> calculator.nth_root(0.0)
            1.0
            >>> calculator.subtract(2.0)
            -1.0
            >>> calculator.nth_root(2.0)
            Traceback (most recent call last):
            ...
            ValueError: Even root of negative number is not a real number

        '''
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


if __name__ == '__main__':

    import doctest

    print(doctest.testmod())
