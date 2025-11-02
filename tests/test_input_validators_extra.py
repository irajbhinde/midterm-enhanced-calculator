import math
import pytest
from app.input_validators import (
    validate_number,
    validate_bounds,
    parse_two_numbers,
    ValidationError,
)

def test_validate_number_rejects_float_nan_inf():
    # These exercise early float guards (lines ~19, 21)
    with pytest.raises(ValidationError):
        validate_number(float("nan"))
    with pytest.raises(ValidationError):
        validate_number(float("inf"))
    with pytest.raises(ValidationError):
        validate_number(float("-inf"))

def test_validate_number_rejects_string_nan_inf_case_insensitive():
    for s in ["NaN", "nan", "INF", "Inf", "+Inf", "-Inf"]:
        with pytest.raises(ValidationError):
            validate_number(s)

def test_validate_bounds_accepts_extra_args_compat():
    # Hits the *args, **__ path of validate_bounds
    a, b = validate_bounds("5", "6.5", object(), config=True)
    assert a == 5 and math.isclose(b, 6.5)

def test_parse_two_numbers_accepts_list_and_tuple():
    # Covers list/tuple unpacking branch (lines ~71-80)
    a, b = parse_two_numbers(["7", "8"])
    assert a == 7 and b == 8
    a2, b2 = parse_two_numbers(("9.5", "0.5"))
    assert math.isclose(a2, 9.5) and math.isclose(b2, 0.5)

def test_parse_two_numbers_too_few_items_raises():
    with pytest.raises(ValidationError):
        parse_two_numbers(["10"])   # not enough numbers

def test_parse_two_numbers_missing_second_value_raises():
    with pytest.raises(ValidationError):
        parse_two_numbers("11")  # single non-iterable; b is None → should raise
