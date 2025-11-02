from .calculator import Calculator
from .calculator_config import AppConfig
from .input_validators import parse_two_numbers, ValidationError
from .exceptions import OperationError, HistoryError, PersistenceError
from .logger import init_logging, colorize, LoggingObserver, AutoSaveObserver
from colorama import init as colorama_init
import sys

def main():
    colorama_init(autoreset=True, strip=False, convert=False)
    cfg = AppConfig.load()
    init_logging(cfg)
    calc = Calculator(config=cfg)

    # Register observers
    calc.register_observer(LoggingObserver(cfg))
    if cfg.auto_save:
        calc.register_observer(AutoSaveObserver(cfg))

    print(colorize("Advanced Calculator REPL. Type 'help' for commands.", 'cyan'))
    while True:
        try:
            raw = input(colorize("> ", 'yellow')).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            print(colorize("Exiting. Bye!", 'cyan'))
            break
        if not raw:
            continue
        parts = raw.split()
        cmd = parts[0].lower()

        if cmd in {'exit', 'quit'}:
            print(colorize("Exiting. Bye!", 'cyan'))
            break
        elif cmd == 'help':
            print(colorize("Commands:", 'cyan'))
            print(" add|subtract|multiply|divide|power|root|modulus|int_divide|percent|abs_diff a b")
            print(" history | clear | undo | redo | save | load | help | exit")
            continue
        elif cmd == 'history':
            for idx, item in enumerate(calc.history.items):
                print(f"{idx+1}. {item.operation}({item.a}, {item.b}) = {item.result} @ {item.timestamp}" )
            continue
        elif cmd == 'clear':
            calc.clear_history()
            print(colorize("History cleared.", 'green'))
            continue
        elif cmd == 'undo':
            try:
                calc.undo()
                print(colorize("Undo completed.", 'green'))
            except HistoryError as e:
                print(colorize(str(e), 'red'))
            continue
        elif cmd == 'redo':
            try:
                calc.redo()
                print(colorize("Redo completed.", 'green'))
            except HistoryError as e:
                print(colorize(str(e), 'red'))
            continue
        elif cmd == 'save':
            try:
                calc.save_history()
                print(colorize("History saved.", 'green'))
            except PersistenceError as e:
                print(colorize(str(e), 'red'))
            continue
        elif cmd == 'load':
            try:
                calc.load_history()
                print(colorize("History loaded.", 'green'))
            except PersistenceError as e:
                print(colorize(str(e), 'red'))
            continue

        # operations expecting two numbers
        if cmd in {'add','subtract','multiply','divide','power','root','modulus','int_divide','percent','abs_diff'}:
            try:
                a, b = parse_two_numbers(parts[1:])
                result = calc.compute(cmd, a, b)
                print(colorize(f"{cmd}({a}, {b}) = {result}", 'green'))
            except (ValidationError, OperationError) as e:
                print(colorize(str(e), 'red'))
            except IndexError:
                print(colorize("Usage: <operation> a b", 'red'))
        else:
            print(colorize(f"Unknown command: {cmd}", 'red'))

if __name__ == '__main__':  # pragma: no cover
    main()  # pragma: no cover
