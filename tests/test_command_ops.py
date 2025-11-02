import pytest
from app.calculator import Calculator
from app.calculator_config import AppConfig
from app.command import OperationCommand
from app.exceptions import ValidationError

def _cfg(tmp_path):
    cfg = AppConfig.load()
    cfg.log_dir = str(tmp_path / "logs")
    cfg.history_dir = str(tmp_path / "hist")
    cfg.history_file = "hist.csv"
    cfg.auto_save = False
    cfg.ensure_dirs()
    return cfg

@pytest.mark.parametrize("op,a,b,contains", [
    ("add", 2, 3, "add(2.0, 3.0) = 5.0"),
    ("percent", 5, 20, "percent(5.0, 20.0) = 25.0"),
    ("abs_diff", -5, 2, "abs_diff(-5.0, 2.0) = 7.0"),
])
def test_operation_command_success(tmp_path, op, a, b, contains):
    c = Calculator(config=_cfg(tmp_path))
    cmd = OperationCommand(op, c.compute)
    out = cmd.execute([op, str(a), str(b)])
    assert contains in out

def test_operation_command_validation_error(tmp_path):
    c = Calculator(config=_cfg(tmp_path))
    cmd = OperationCommand("add", c.compute)
    out = cmd.execute(["add", "not_a_number", "3"])
    assert "Invalid number" in out

def test_operation_command_divide_by_zero(tmp_path):
    c = Calculator(config=_cfg(tmp_path))
    cmd = OperationCommand("divide", c.compute)
    out = cmd.execute(["divide", "1", "0"])
    assert "Division by zero" in out
