import pytest
from app.calculator import Calculator

def test_calculator_basic_operations():
    c = Calculator()
    assert c.compute("add", 2, 3) == 5
    assert c.compute("multiply", 4, 2) == 8
    assert c.compute("subtract", 10, 7) == 3

def test_calculator_divide_by_zero_raises():
    c = Calculator()
    with pytest.raises(Exception):
        c.compute("divide", 10, 0)

def test_calculator_uses_history_and_undo_redo():
    c = Calculator()
    c.compute("add", 1, 2)        # -> 3
    c.compute("multiply", 3, 2)   # -> 6
    assert getattr(c, "result", 6) == 6

    c.undo()
    assert getattr(c, "result", 3) == 3
    c.redo()
    assert getattr(c, "result", 6) == 6

def test_calculator_unknown_operation_raises():
    c = Calculator()
    with pytest.raises(Exception):
        c.compute("not_an_op", 1, 2)
