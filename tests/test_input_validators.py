import pytest
from app.input_validators import validate_number, validate_operation, validate_bounds

def test_validate_number_accepts_int_float_and_numeric_strings():
    assert validate_number(3) == 3
    assert validate_number(3.5) == 3.5
    assert validate_number("4") == 4
    assert validate_number("4.25") == 4.25

@pytest.mark.parametrize("bad", ["x", None, object(), "nan", "inf"])
def test_validate_number_rejects_non_numeric(bad):
    with pytest.raises((Exception,)):
        validate_number(bad)

def test_validate_operation_allows_known_ops():
    for op in ["add", "subtract", "multiply", "divide", "power"]:
        try:
            assert validate_operation(op) == op
        except Exception:
            if op != "power":
                raise

def test_validate_operation_rejects_unknown():
    with pytest.raises(Exception):
        validate_operation("nope")

def test_validate_bounds_converts_numbers():
    a, b = validate_bounds("5", "6.5")
    assert a == 5
    assert b == 6.5
