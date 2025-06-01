"""
A sample Python file for testing the Vaahai CLI review command.
"""

def add_numbers(a, b):
    """Add two numbers and return the result."""
    return a + b

def subtract_numbers(a, b):
    """Subtract b from a and return the result."""
    return a - b

class Calculator:
    """A simple calculator class."""
    
    def __init__(self):
        """Initialize the calculator."""
        self.result = 0
    
    def add(self, a, b):
        """Add two numbers and store the result."""
        self.result = a + b
        return self.result
    
    def subtract(self, a, b):
        """Subtract b from a and store the result."""
        self.result = a - b
        return self.result
    
    def multiply(self, a, b):
        """Multiply two numbers and store the result."""
        self.result = a * b
        return self.result
    
    def divide(self, a, b):
        """Divide a by b and store the result."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        self.result = a / b
        return self.result

# Example usage
if __name__ == "__main__":
    calc = Calculator()
    print(calc.add(5, 3))       # 8
    print(calc.subtract(5, 3))  # 2
    print(calc.multiply(5, 3))  # 15
    print(calc.divide(6, 3))    # 2.0
