from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class Calculation:
    operation: str
    a: float
    b: float
    result: float
    timestamp: str

    @staticmethod
    def create(operation: str, a: float, b: float, result: float) -> 'Calculation':
        return Calculation(operation=operation, a=a, b=b, result=result, timestamp=datetime.utcnow().isoformat())