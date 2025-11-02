from __future__ import annotations
from typing import List, Callable
import math
import os
import logging
import pandas as pd

from .operations import OperationFactory
from .calculation import Calculation
from .history import History
from .calculator_memento import CalculatorMemento
from .exceptions import OperationError, HistoryError, PersistenceError, ValidationError
from .calculator_config import AppConfig
from .input_validators import validate_bounds

class Calculator:
    def __init__(self, config: AppConfig | None = None):
        self.config = config or AppConfig.load()
        self.history = History(max_size=self.config.max_history_size)
        self._observers: List[Callable[[Calculation], None]] = []

    # Observer registration
    def register_observer(self, observer) -> None:
        if hasattr(observer, 'on_new_calculation'):
            self._observers.append(observer.on_new_calculation)

    def _notify(self, calc: Calculation) -> None:
        for fn in self._observers:
            try:
                fn(calc)
            except Exception:
                pass  # observers are best-effort

    # Core compute
    def compute(self, op_name: str, a: float, b: float) -> float:
        validate_bounds(a, b, self.config)
        op = OperationFactory.create(op_name)
        result = op.execute(a, b)
        # round to configured precision for display/persistence
        result = float(round(result, self.config.precision))
        calc = Calculation.create(op_name, a, b, result)
        self.history.push(calc)
        self._notify(calc)
        if self.config.auto_save:
            # best-effort save after notify
            try:
                self.save_history()
            except Exception:
                pass
        return result

    # Undo/redo via memento
    def undo(self) -> None:
        self.history.undo()

    def redo(self) -> None:
        self.history.redo()

    def clear_history(self) -> None:
        self.history = History(max_size=self.config.max_history_size)

    # Persistence
    def save_history(self) -> None:
        self.history.save_csv(self.config.history_path, encoding=self.config.encoding)

    def load_history(self) -> None:
        self.history.load_csv(self.config.history_path)