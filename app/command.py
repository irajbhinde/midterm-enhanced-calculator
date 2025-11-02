# app/command.py
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Callable, Dict, Optional, Tuple
from .exceptions import ValidationError, HistoryError, PersistenceError, OperationError
from .input_validators import parse_two_numbers
from .logger import colorize

class Command(ABC):
    """Encapsulate a REQ with execute()."""
    @abstractmethod
    def execute(self, line_parts: list[str]) -> Optional[str]: ...

class CommandRegistry:
    def __init__(self):
        self._registry: Dict[str, Command] = {}

    def register(self, name: str, cmd: Command):
        self._registry[name] = cmd

    def get(self, name: str) -> Optional[Command]:
        return self._registry.get(name)

    @property
    def names(self):
        return sorted(self._registry.keys())

# ---- Concrete Commands ----

class OperationCommand(Command):
    """Wraps a calculator.compute(op, a, b) call."""
    def __init__(self, op_name: str, compute: Callable[[str, float, float], float]):
        self.op_name = op_name
        self._compute = compute

    def execute(self, line_parts: list[str]) -> str:
        # Expect exactly two args
        try:
            a, b = parse_two_numbers(line_parts[1:])
            result = self._compute(self.op_name, a, b)
            return colorize(f"{self.op_name}({a}, {b}) = {result}", "green")
        except (ValidationError, OperationError) as e:
            return colorize(str(e), "red")

class UndoCommand(Command):
    def __init__(self, undo: Callable[[], None]):
        self._undo = undo
    def execute(self, _: list[str]) -> str:
        try:
            self._undo()
            return colorize("Undo completed.", "green")
        except HistoryError as e:
            return colorize(str(e), "red")

class RedoCommand(Command):
    def __init__(self, redo: Callable[[], None]):
        self._redo = redo
    def execute(self, _: list[str]) -> str:
        try:
            self._redo()
            return colorize("Redo completed.", "green")
        except HistoryError as e:
            return colorize(str(e), "red")

class HistoryCommand(Command):
    def __init__(self, iter_history: Callable[[], list[str]]):
        self._iter = iter_history
    def execute(self, _: list[str]) -> str:
        items = self._iter()
        return "\n".join(items) if items else colorize("(empty)", "yellow")

class ClearCommand(Command):
    def __init__(self, clear: Callable[[], None]):
        self._clear = clear
    def execute(self, _: list[str]) -> str:
        self._clear()
        return colorize("History cleared.", "green")

class SaveCommand(Command):
    def __init__(self, save: Callable[[], None]):
        self._save = save
    def execute(self, _: list[str]) -> str:
        try:
            self._save()
            return colorize("History saved.", "green")
        except PersistenceError as e:
            return colorize(str(e), "red")

class LoadCommand(Command):
    def __init__(self, load: Callable[[], None]):
        self._load = load
    def execute(self, _: list[str]) -> str:
        try:
            self._load()
            return colorize("History loaded.", "green")
        except PersistenceError as e:
            return colorize(str(e), "red")
