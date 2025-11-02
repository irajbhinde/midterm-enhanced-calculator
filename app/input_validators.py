from typing import Sequence, Tuple
from .exceptions import ValidationError
from .calculator_config import AppConfig

def _to_number(x: str) -> float:
    try:
        return float(x)
    except Exception:
        raise ValidationError(f"Invalid number: {x}")

def validate_bounds(a: float, b: float, cfg: AppConfig) -> None:
    for v in (a, b):
        if abs(v) > cfg.max_input_value:
            raise ValidationError(f"Input {v} exceeds max allowed value {cfg.max_input_value}")

def parse_two_numbers(args: Sequence[str]) -> Tuple[float, float]:
    if len(args) < 2:
        raise ValidationError("Two numeric arguments required.")
    return _to_number(args[0]), _to_number(args[1])