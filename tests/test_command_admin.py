from pathlib import Path
from app.calculator import Calculator
from app.calculator_config import AppConfig
from app.command import UndoCommand, RedoCommand, HistoryCommand, ClearCommand, SaveCommand, LoadCommand

def _cfg(tmp_path):
    cfg = AppConfig.load()
    cfg.log_dir = str(tmp_path / "logs")
    cfg.history_dir = str(tmp_path / "hist")
    cfg.history_file = "hist.csv"
    cfg.auto_save = False
    cfg.ensure_dirs()
    return cfg

def test_undo_redo_history_and_persistence(tmp_path):
    c = Calculator(config=_cfg(tmp_path))
    # seed two calcs
    c.compute("add", 1, 1)
    c.compute("add", 2, 2)

    hist_cmd = HistoryCommand(lambda: [
        f"{idx+1}. {item.operation}({float(item.a)}, {float(item.b)}) = {item.result} @ {item.timestamp}"
        for idx, item in enumerate(c.history.items[: c.history._cursor + 1])
    ])

    # history shows 2 entries
    txt = hist_cmd.execute([])
    assert "add(1.0, 1.0) = 2.0" in txt and "add(2.0, 2.0) = 4.0" in txt

    # undo then redo
    undo_cmd = UndoCommand(c.undo); redo_cmd = RedoCommand(c.redo)
    assert "Undo completed." in undo_cmd.execute([])
    txt = hist_cmd.execute([])
    assert "add(2.0, 2.0) = 4.0" not in txt
    assert "Redo completed." in redo_cmd.execute([])

    # save
    save_cmd = SaveCommand(c.save_history)
    assert "History saved." in save_cmd.execute([])
    path = Path(c.config.history_path)
    assert path.exists()

    # clear then load
    clear_cmd = ClearCommand(c.clear_history)
    assert "History cleared." in clear_cmd.execute([])
    assert "(empty)" in hist_cmd.execute([])

    load_cmd = LoadCommand(c.load_history)
    assert "History loaded." in load_cmd.execute([])
    txt = hist_cmd.execute([])
    assert "add(1.0, 1.0) = 2.0" in txt and "add(2.0, 2.0) = 4.0" in txt
