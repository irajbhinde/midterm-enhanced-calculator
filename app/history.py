from __future__ import annotations
from typing import List
import pandas as pd
import os
from .calculation import Calculation
from .calculator_memento import CalculatorMemento
from .exceptions import HistoryError, PersistenceError

class History:
    def __init__(self, max_size: int = 1000):
        self.items: List[Calculation] = []
        self._cursor = -1  # last applied index
        self.max_size = max_size

    # Memento controls
    def save(self) -> CalculatorMemento:
        return CalculatorMemento(items=self.items.copy(), index=self._cursor)

    def restore(self, m: CalculatorMemento) -> None:
        self.items = m.items.copy()
        self._cursor = m.index

    # History stack methods
    def push(self, calc: Calculation) -> None:
        # if we add a new item after undoing, drop the "future"
        if self._cursor < len(self.items) - 1:
            self.items = self.items[: self._cursor + 1]
        self.items.append(calc)
        # enforce max_size (drop oldest)
        if len(self.items) > self.max_size:
            self.items = self.items[-self.max_size:]
        self._cursor = len(self.items) - 1

    def can_undo(self) -> bool:
        return self._cursor >= 0

    def can_redo(self) -> bool:
        return self._cursor < len(self.items) - 1

    def undo(self) -> None:
        if not self.can_undo():
            raise HistoryError("Nothing to undo.")
        self._cursor -= 1

    def redo(self) -> None:
        if not self.can_redo():
            raise HistoryError("Nothing to redo.")
        self._cursor += 1

    # Persistence
    def to_dataframe(self) -> pd.DataFrame:
        data = [
            {'operation': c.operation, 'operand1': c.a, 'operand2': c.b, 'result': c.result, 'timestamp': c.timestamp}
            for c in self.items[: self._cursor + 1]
        ]
        return pd.DataFrame(data)

    def save_csv(self, path: str, encoding: str = 'utf-8') -> None:
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            df = self.to_dataframe()
            df.to_csv(path, index=False, encoding=encoding)
        except Exception as e:
            raise PersistenceError(f"Failed to save history: {e}")

    @staticmethod
    def from_dataframe(df: pd.DataFrame) -> 'History':
        h = History()
        for _, row in df.iterrows():
            h.items.append(Calculation(
                operation=row['operation'],
                a=float(row['operand1']),
                b=float(row['operand2']),
                result=float(row['result']),
                timestamp=str(row['timestamp'])
            ))
        h._cursor = len(h.items) - 1
        return h

    def load_csv(self, path: str) -> None:
        try:
            if not os.path.exists(path):
                raise PersistenceError("History file does not exist.")
            df = pd.read_csv(path)
            newh = History.from_dataframe(df)
            self.items = newh.items
            self._cursor = newh._cursor
        except PersistenceError:
            raise
        except Exception as e:
            raise PersistenceError(f"Failed to load history: {e}")