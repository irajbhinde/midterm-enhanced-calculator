import pytest
from app.operations import OperationFactory
from app.exceptions import OperationError

@pytest.mark.parametrize('op,a,b,expected', [
    ('add', 2, 3, 5),
    ('subtract', 5, 7, -2),
    ('multiply', 3, 4, 12),
    ('divide', 8, 2, 4),
    ('power', 2, 3, 8),
    ('root', 27, 3, 3),
    ('modulus', 10, 3, 1),
    ('int_divide', 7, 2, 3),
    ('percent', 5, 20, 25.0),
    ('abs_diff', -5, 2, 7),
])
def test_operations_happy(op, a, b, expected):
    opi = OperationFactory.create(op)
    assert opi.execute(a, b) == expected

def test_divide_by_zero():
    with pytest.raises(OperationError):
        OperationFactory.create('divide').execute(1, 0)

def test_modulus_by_zero():
    with pytest.raises(OperationError):
        OperationFactory.create('modulus').execute(1, 0)

def test_int_divide_by_zero():
    with pytest.raises(OperationError):
        OperationFactory.create('int_divide').execute(1, 0)

def test_percent_by_zero():
    with pytest.raises(OperationError):
        OperationFactory.create('percent').execute(1, 0)

def test_unknown_operation():
    with pytest.raises(OperationError):
        OperationFactory.create('nope')
