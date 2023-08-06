class Calculator:

    def __init__(self, num=0.0):
        self.num = num

    def __str__(self):
        return f"Number in memory: {self.num}"

    def add(self, x: float) -> float:
        """ Returns the sum of number in memory and number x """
        self.num = self.num + x
        return self.num

    def subtract(self, x: float) -> float:
        """ Returns the difference between number in memory and number x """
        self.num = self.num - x
        return self.num

    def multiply(self, x: float) -> float:
        """ Returns the product of number in memory and number x """
        self.num = self.num * x
        return self.num

    def divide(self, x: float) -> float:
        """ Returns the ratio of number in memory and number x """
        assert x != 0, " Denominator is equal to zero! "

        self.num = self.num / x
        return self.num

    def root(self, x: int) -> float:
        """ Returns the x-th root of number in memory """
        assert isinstance(x, int), f"Root {x} is not an integer!"
        assert x > 0, " Degree of the root is less or equal to zero! "
        assert self.num >= 0, f"Radicand {self.num} is negative!"

        self.num = self.num ** (1 / x)
        return self.num

    def reset(self) -> float:
        """ Resets memory to zero """
        self.num = 0.0
        return self.num
