from typing import Tuple, Union

NumberLike = Union[int, float, str]


class ValidationError(ValueError):
    """Raised when input validation fails."""


def validate_number(value: NumberLike) -> Union[int, float]:
    """
    Accept int/float or numeric strings. Returns int if integer-like, else float.
    Rejects NaN/Inf and non-numeric inputs.
    """
    if isinstance(value, (int, float)):
        # Reject NaN/Inf explicitly
        if isinstance(value, float):
            if value != value:  # NaN
                raise ValidationError("NaN is not allowed.")
            if value in (float("inf"), float("-inf")):
                raise ValidationError("Infinity is not allowed.")
        return value

    if isinstance(value, str):
        s = value.strip()
        low = s.lower()
        if low in {"nan", "inf", "+inf", "-inf"}:
            raise ValidationError("Special float values are not allowed.")
        try:
            if "." in s or "e" in low:
                return float(s)
            return int(s)
        except Exception as exc:
            raise ValidationError(f"Not a valid number: {value!r}") from exc

    raise ValidationError(f"Unsupported type for number: {type(value).__name__}")


_ALLOWED_OPS = {"add", "subtract", "multiply", "divide", "power"}


def validate_operation(op: str) -> str:
    if not isinstance(op, str):
        raise ValidationError("Operation must be a string.")
    normalized = op.strip().lower()
    if normalized not in _ALLOWED_OPS:
        raise ValidationError(f"Unknown operation: {op!r}")
    return normalized


def validate_bounds(a: NumberLike, b: NumberLike, *_, **__) -> Tuple[Union[int, float], Union[int, float]]:
    """
    Validates two numeric inputs and returns normalized numbers (a, b).
    Accepts and ignores extra positional/keyword args to stay compatible with callers
    that pass a config object (e.g., validate_bounds(a, b, config)).
    """
    return validate_number(a), validate_number(b)


# Back-compat for app.__init__ imports
def parse_two_numbers(a, b=None, *_, **__):
    """
    Accepts either:
      - two positional values: parse_two_numbers(a, b)
      - a single iterable:    parse_two_numbers([a, b]) or parse_two_numbers((a, b))
    Returns (a_num, b_num) after validation.

    Extra positional/keyword args are ignored for compatibility with callers.
    """
    # If only one arg was given and it's an iterable of 2+ items, unpack it
    if b is None and isinstance(a, (list, tuple)):
        if len(a) < 2:
            raise ValidationError("Expected two numbers, got fewer.")
        a, b = a[0], a[1]

    if b is None:
        # Still missing the second value
        raise ValidationError("Expected two numbers (a, b).")

    return validate_bounds(a, b)
