from dataclasses import dataclass
from typing import List
from .calculation import Calculation

@dataclass(frozen=True)
class CalculatorMemento:
    items: List[Calculation]
    index: int