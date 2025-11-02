# tests/test_help_dynamic.py
from app.help import BaseHelp, OperationListHelp
from app.operations import OperationFactory

def test_help_includes_all_ops():
    view = OperationListHelp(BaseHelp())
    txt = view.render()
    for op in OperationFactory._registry.keys():
        assert op in txt
