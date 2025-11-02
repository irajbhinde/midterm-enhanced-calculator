from app.calculation import Calculation

def test_calculation_create():
    c = Calculation.create('add', 1, 2, 3)
    assert c.operation == 'add'
    assert c.a == 1 and c.b == 2 and c.result == 3
    assert 'T' in c.timestamp or '-' in c.timestamp
