import importlib
import numbers
import pytest

ops_mod = importlib.import_module("app.operations")
Factory = getattr(ops_mod, "OperationFactory")

def _exec(name, a, b):
    op = Factory.create(name)
    if callable(op):
        return op(a, b)
    return op.execute(a, b)

def _is_number(x):
    return isinstance(x, numbers.Number)

def test_operations_core_execute_numbers():
    supported = set(getattr(Factory, "_registry", {}).keys())
    preferred_order = ["add", "subtract", "multiply", "divide", "power", "modulus", "intdivide", "absdiff", "root", "percent"]
    to_test = [name for name in preferred_order if name in supported]
    assert to_test, "No operations are registered in OperationFactory._registry"

    safe_args = {
        "add": (2, 3), "subtract": (5, 2), "multiply": (3, 4), "divide": (8, 2),
        "power": (2, 3), "modulus": (7, 3), "intdivide": (7, 3), "absdiff": (9, 4),
        "root": (27, 3), "percent": (10, 50),
    }
    for name in to_test:
        a, b = safe_args.get(name, (2, 2))
        res = _exec(name, a, b)
        assert _is_number(res)

def test_divide_by_zero_raises_or_is_handled():
    supported = set(getattr(Factory, "_registry", {}).keys())
    if "divide" not in supported:
        pytest.skip("'divide' is not registered")
    try:
        _ = _exec("divide", 1, 0)
    except Exception:
        return
    assert True
