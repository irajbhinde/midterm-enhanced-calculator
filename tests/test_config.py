import importlib
from app import calculator_config as cfg

def test_config_imports_and_has_appconfig():
    importlib.reload(cfg)
    assert hasattr(cfg, "AppConfig")
    C = cfg.AppConfig()
    assert isinstance(C.precision, int) and C.precision >= 0
    assert isinstance(C.max_input_value, (int, float))
    assert isinstance(C.auto_save, bool)

def test_config_paths_exist_as_strings():
    import app.calculator_config as cfg
    C = cfg.AppConfig()
    assert isinstance(C.log_dir, str)
    assert isinstance(C.log_file, str)
    assert isinstance(C.history_dir, str)
    assert isinstance(C.history_file, str)
