import logging
import os
from dataclasses import dataclass
from colorama import Fore, Style
from .calculation import Calculation

def colorize(text: str, color: str) -> str:
    """
    Colorize text unless NO_COLOR is set or we're running under CI.
    This also keeps output plain during GitHub Actions tests.
    """
    import os
    if os.environ.get("NO_COLOR") or os.environ.get("CI"):
        return text

    from colorama import Fore, Style
    mapping = {
        'red': Fore.RED, 'green': Fore.GREEN, 'yellow': Fore.YELLOW,
        'cyan': Fore.CYAN, 'blue': Fore.BLUE, 'magenta': Fore.MAGENTA, 'white': Fore.WHITE,
    }
    return f"{mapping.get(color, Fore.WHITE)}{text}{Style.RESET_ALL}"

def init_logging(cfg) -> None:
    import logging, os
    os.makedirs(cfg.log_dir, exist_ok=True)
    log_path = os.path.join(cfg.log_dir, cfg.log_file)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.handlers.clear()  # avoid duplicate handlers on repeated runs

    # File logs (keep timestamps + levels)
    file_handler = logging.FileHandler(log_path, encoding=cfg.encoding)
    file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))

    # Console logs (clean output, no timestamp/level)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("%(message)s"))

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logging.info("Logger initialized.")

class Observer:
    def on_new_calculation(self, calc: Calculation):  # pragma: no cover (simple interface)
        pass

@dataclass
class LoggingObserver(Observer):
    cfg: object
    def on_new_calculation(self, calc: Calculation):
        logging.info(f"CALC {calc.operation}({calc.a}, {calc.b}) = {calc.result} @ {calc.timestamp}")

@dataclass
class AutoSaveObserver(Observer):
    cfg: object
    def on_new_calculation(self, calc: Calculation):
        # Defer to Calculator.save_history; observer just a hook here
        try:
            # The calculator will call save explicitly after notifying observers.
            pass  # pragma: no cover
        except Exception:
            # We intentionally avoid raising from observers to not break UI.
            pass  # pragma: no cover