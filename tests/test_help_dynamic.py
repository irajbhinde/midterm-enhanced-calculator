from app.help import BaseHelp, OperationListHelp
from app.operations import OperationFactory

def test_help_includes_all_ops():
    view = OperationListHelp(BaseHelp())
    txt = view.render()
    for op in OperationFactory._registry.keys():
        assert op in txt
    # sanity: includes usage and examples
    assert "Usage:" in txt
    assert "Operation commands:" in txt
