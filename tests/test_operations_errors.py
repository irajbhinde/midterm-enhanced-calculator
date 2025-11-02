import importlib
import pytest

ops_mod = importlib.import_module("app.operations")
Factory = getattr(ops_mod, "OperationFactory")
OperationError = getattr(importlib.import_module("app.exceptions"), "OperationError")

def test_operationfactory_unknown_raises():
    with pytest.raises(OperationError):
        Factory.create("__definitely_unknown__")
