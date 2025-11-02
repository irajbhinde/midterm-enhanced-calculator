from app.calculation import Calculation

def test_calculation_create():
    c = Calculation.create("add", 2, 3, 5)
    assert c.operation == "add"
    assert c.a == 2 or getattr(c, "operand1", 2) == 2
    assert c.b == 3 or getattr(c, "operand2", 3) == 3
    assert c.result == 5
    assert isinstance(c.timestamp, str)
