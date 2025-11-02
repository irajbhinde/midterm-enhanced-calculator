# app/help.py
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, Iterable
from .operations import OperationFactory
from .logger import colorize

class HelpComponent(ABC):
    @abstractmethod
    def render(self) -> str: ...

class BaseHelp(HelpComponent):
    """Static core help (non-operation commands)."""
    def render(self) -> str:
        core = (
            f"{colorize('Core commands:', 'cyan')}\n"
            "  history  - Show calculation history\n"
            "  clear    - Clear calculation history\n"
            "  undo     - Undo last calculation\n"
            "  redo     - Redo last undone calculation\n"
            "  save     - Save calculation history to CSV\n"
            "  load     - Load calculation history from CSV\n"
            "  help     - Show this help\n"
            "  exit     - Exit the application\n"
        )
        return core

class HelpDecorator(HelpComponent):
    def __init__(self, component: HelpComponent):
        self._component = component
    def render(self) -> str:
        return self._component.render()

class OperationListHelp(HelpDecorator):
    """
    Decorator that dynamically adds available operation commands from the
    OperationFactory registry. Adding a new operation auto-appears here.
    """
    def __init__(self, component: HelpComponent, extra_ops: Iterable[str] | None = None):
        super().__init__(component)
        self._extra_ops = list(extra_ops or [])

    def render(self) -> str:
        base = self._component.render()
        ops = sorted(set(list(OperationFactory._registry.keys()) + self._extra_ops))
        ops_line = colorize("Operation commands:", "cyan") + "\n  " + ", ".join(ops) + "\n"
        usage = colorize("Usage:", "cyan") + "\n  <operation> <a> <b>\n"
        examples = (
            colorize("Examples:", "cyan") + "\n"
            "  add 2 3\n"
            "  power 2 8\n"
            "  percent 5 20\n"
        )
        return ops_line + base + "\n" + usage + examples
