import pandas as pd
import pytest
from app.history import History
from app.calculation import Calculation
from app.exceptions import HistoryError

def test_history_push_undo_redo():
    h = History(max_size=10)
    h.push(Calculation.create('add',1,2,3))
    h.push(Calculation.create('add',2,2,4))
    assert h.can_undo()
    h.undo()
    assert h.can_redo()
    h.redo()
    assert not h.can_redo()

def test_to_dataframe_and_from_dataframe(tmp_path):
    h = History(max_size=10)
    h.push(Calculation.create('add',1,2,3))
    df = h.to_dataframe()
    assert list(df.columns) == ['operation','operand1','operand2','result','timestamp']
    path = tmp_path / 'h.csv'
    h.save_csv(str(path))
    h2 = History(max_size=10)
    h2.load_csv(str(path))
    assert len(h2.items) == 1
    assert h2.items[0].result == 3
