# app/__init__.py
from .calculator import Calculator
from .calculator_config import AppConfig
from .exceptions import HistoryError, PersistenceError, OperationError, ValidationError
from .logger import init_logging, colorize, LoggingObserver, AutoSaveObserver
from .help import BaseHelp, OperationListHelp
from .command import (
    CommandRegistry, OperationCommand, UndoCommand, RedoCommand,
    HistoryCommand, ClearCommand, SaveCommand, LoadCommand
)
from colorama import init as colorama_init


def main():  # pragma: no cover
    """Main entry point for the Advanced Calculator REPL."""
    # Git Bash (mintty) supports ANSI; do not strip/convert.
    colorama_init(autoreset=True, strip=False, convert=False)

    cfg = AppConfig.load()
    init_logging(cfg)
    calc = Calculator(config=cfg)

    # Observers
    calc.register_observer(LoggingObserver(cfg))
    if cfg.auto_save:
        calc.register_observer(AutoSaveObserver(cfg))

    # ---- Command registry ----
    registry = CommandRegistry()

    # Dynamically register all operations from the Factory (Factory Pattern)
    from .operations import OperationFactory
    for op_name in OperationFactory._registry.keys():
        registry.register(op_name, OperationCommand(op_name, calc.compute))

    # ---- Utility commands ----
    registry.register("undo", UndoCommand(calc.undo))
    registry.register("redo", RedoCommand(calc.redo))
    registry.register(
        "history",
        HistoryCommand(
            lambda: [
                f"{idx+1}. {item.operation}({float(item.a)}, {float(item.b)}) = {item.result} @ {item.timestamp}"
                for idx, item in enumerate(calc.history.items[: calc.history._cursor + 1])
            ]
        ),
    )
    registry.register("clear", ClearCommand(calc.clear_history))
    registry.register("save", SaveCommand(calc.save_history))
    registry.register("load", LoadCommand(calc.load_history))

    # ---- Decorated Help (auto-updates when operations change) ----
    help_view = OperationListHelp(BaseHelp())

    print(colorize("Advanced Calculator REPL. Type 'help' for commands.", "cyan"))
    while True:
        try:
            raw = input(colorize("> ", "yellow")).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            print(colorize("Exiting. Bye!", "cyan"))
            break

        if not raw:
            continue

        parts = raw.split()
        cmd = parts[0].lower()

        # Exit
        if cmd in {"exit", "quit"}:
            print(colorize("Exiting. Bye!", "cyan"))
            break

        # Help
        if cmd == "help":
            print(help_view.render())
            continue

        # Dispatch to command (Command Pattern)
        command = registry.get(cmd)
        if command:
            out = command.execute(parts)
            if out:
                print(out)
        else:
            print(colorize(f"Unknown command: {cmd}", "red"))


if __name__ == "__main__":  # pragma: no cover
    main()  # pragma: no cover
