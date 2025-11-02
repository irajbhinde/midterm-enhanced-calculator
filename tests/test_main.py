import importlib

def test_dunder_main_imports_cleanly():
    mod = importlib.import_module("app.__main__")
    importlib.reload(mod)
    assert hasattr(mod, "__name__")
