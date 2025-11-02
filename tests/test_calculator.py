import os
import pandas as pd
import pytest
from app.calculator import Calculator
from app.calculator_config import AppConfig
from app.exceptions import HistoryError, ValidationError

def cfg(tmp_path):
    cfg = AppConfig.load()
    cfg.log_dir = str(tmp_path / 'logs')
    cfg.history_dir = str(tmp_path / 'hist')
    cfg.history_file = 'hist.csv'
    cfg.auto_save = False
    cfg.max_input_value = 1e6
    cfg.ensure_dirs()
    return cfg

def test_compute_and_history(tmp_path):
    c = Calculator(config=cfg(tmp_path))
    res = c.compute('add', 2, 3)
    assert res == 5
    assert len(c.history.items) == 1

def test_undo_redo(tmp_path):
    c = Calculator(config=cfg(tmp_path))
    c.compute('add', 1, 1)
    c.compute('add', 2, 2)
    c.undo()
    assert c.history.can_redo()
    c.redo()
    assert not c.history.can_redo()

def test_save_load_history(tmp_path):
    c = Calculator(config=cfg(tmp_path))
    c.compute('multiply', 3, 3)
    c.save_history()
    path = c.config.history_path
    assert os.path.exists(path)
    # Load into new instance
    c2 = Calculator(config=cfg(tmp_path))
    c2.load_history()
    assert len(c2.history.items) == 1
    assert c2.history.items[0].result == 9

def test_bounds_validation(tmp_path):
    c = Calculator(config=cfg(tmp_path))
    with pytest.raises(ValidationError):
        c.compute('add', 1e9, 1)

def test_precision_rounding(tmp_path):
    c = Calculator(config=cfg(tmp_path))
    c.config.precision = 2
    res = c.compute('divide', 1, 3)
    assert res == 0.33
