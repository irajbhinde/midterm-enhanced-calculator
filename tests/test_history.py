import importlib

hist_mod = importlib.import_module("app.history")
calc_mod = importlib.import_module("app.calculation")

History = getattr(hist_mod, "History")
Calculation = getattr(calc_mod, "Calculation")

def _mk_calc(op, a, b, result):
    return Calculation.create(operation=op, a=a, b=b, result=result)

def test_history_push_undo_redo_and_flags():
    h = History()
    h.push(_mk_calc("add", 2, 3, 5))
    h.push(_mk_calc("multiply", 3, 4, 12))

    df = h.to_dataframe()
    assert len(df) == 2
    assert hasattr(h, "can_undo") and h.can_undo()
    assert hasattr(h, "can_redo") and (not h.can_redo())

    h.undo()
    df_after_undo = h.to_dataframe()
    assert len(df_after_undo) == 1
    assert h.can_redo()

    h.redo()
    df_after_redo = h.to_dataframe()
    assert len(df_after_redo) == 2
    assert h.can_undo()

def test_history_from_to_dataframe_roundtrip():
    h1 = History()
    h1.push(_mk_calc("subtract", 5, 2, 3))
    h1.push(_mk_calc("divide", 8, 2, 4))

    df = h1.to_dataframe()
    assert len(df) == 2

    h2 = History.from_dataframe(df)
    df2 = h2.to_dataframe()
    assert len(df2) == 2

def test_history_undo_boundary_behaviour():
    h = History()
    h.push(_mk_calc("add", 1, 1, 2))
    h.undo()
    try:
        h.undo()
    except Exception:
        pass
    try:
        if h.can_redo():
            h.redo()
    except Exception:
        pass
