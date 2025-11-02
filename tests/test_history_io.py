import importlib
import pandas as pd

hist_mod = importlib.import_module("app.history")
calc_mod = importlib.import_module("app.calculation")

History = getattr(hist_mod, "History")
Calculation = getattr(calc_mod, "Calculation")

def _calc(op, a, b, result):
    return Calculation.create(operation=op, a=a, b=b, result=result)

def test_history_csv_roundtrip(tmp_path):
    h = History()
    h.push(_calc("add", 2, 3, 5))
    h.push(_calc("subtract", 7, 4, 3))

    p = tmp_path / "hist.csv"
    h.save_csv(str(p))

    h2 = History()
    h2.load_csv(str(p))

    df1 = h.to_dataframe()
    df2 = h2.to_dataframe()
    assert isinstance(df1, pd.DataFrame) and isinstance(df2, pd.DataFrame)
    assert len(df2) == len(df1) == 2

def test_history_dataframe_roundtrip_types():
    h = History()
    h.push(_calc("multiply", 3, 4, 12))

    df = h.to_dataframe()
    assert isinstance(df, pd.DataFrame)

    cols = set(df.columns)
    numeric_pairs_ok = (
        {"a", "b"}.issubset(cols) or
        {"operand1", "operand2"}.issubset(cols)
    )
    assert numeric_pairs_ok, f"Unexpected dataframe columns: {sorted(cols)}"

    assert "operation" in cols
    assert "result" in cols
    assert "timestamp" in cols

    h3 = History.from_dataframe(df)
    df3 = h3.to_dataframe()
    assert isinstance(df3, pd.DataFrame)
    assert len(df3) == 1
