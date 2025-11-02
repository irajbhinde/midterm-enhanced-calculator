from abc import ABC, abstractmethod
import math
from .exceptions import OperationError

class Operation(ABC):
    @abstractmethod
    def execute(self, a: float, b: float) -> float: ...

class Add(Operation):
    def execute(self, a, b): return a + b

class Subtract(Operation):
    def execute(self, a, b): return a - b

class Multiply(Operation):
    def execute(self, a, b): return a * b

class Divide(Operation):
    def execute(self, a, b):
        if b == 0:
            raise OperationError("Division by zero.")
        return a / b

class Power(Operation):
    def execute(self, a, b):
        try:
            return a ** b
        except Exception as e:  # pragma: no cover (math domain is covered in tests)
            raise OperationError(str(e))

class Root(Operation):
    def execute(self, a, b):
        if b == 0:
            raise OperationError("Zeroth root is undefined.")
        if a < 0 and b % 2 == 0:
            raise OperationError("Even root of a negative number is not real.")
        try:
            return a ** (1.0 / b)
        except Exception as e:  # pragma: no cover
            raise OperationError(str(e))

class Modulus(Operation):
    def execute(self, a, b):
        if b == 0:
            raise OperationError("Modulus by zero.")
        return a % b

class IntDivide(Operation):
    def execute(self, a, b):
        if b == 0:
            raise OperationError("Integer division by zero.")
        return a // b

class Percent(Operation):
    def execute(self, a, b):
        if b == 0:
            raise OperationError("Percentage undefined when denominator is zero.")
        return (a / b) * 100.0

class AbsDiff(Operation):
    def execute(self, a, b):
        return abs(a - b)

class OperationFactory:
    _registry = {
    "add": Add(),
    "subtract": Subtract(),
    "multiply": Multiply(),
    "divide": Divide(),
    "power": Power(),
    "root": Root(),
    "modulus": Modulus(),
    "int_divide": IntDivide(),
    "percent": Percent(),
    "abs_diff": AbsDiff(),   
}

    @classmethod
    def create(cls, name: str) -> Operation:
        op = cls._registry.get(name)
        if not op:
            raise OperationError(f"Unknown operation: {name}")
        return op