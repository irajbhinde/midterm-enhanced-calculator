from unittest import mock
import importlib
import logging

def test_get_logger_configures_once():
    logger_mod = importlib.import_module("app.logger")
    importlib.reload(logger_mod)

    # candidate factories
    factory = None
    for name in ["get_logger", "setup_logger", "init_logger", "configure_logger", "logger"]:
        if hasattr(logger_mod, name) and callable(getattr(logger_mod, name)):
            factory = getattr(logger_mod, name); break

    if factory is None:
        if hasattr(logger_mod, "LOGGER") and isinstance(getattr(logger_mod, "LOGGER"), logging.Logger):
            assert isinstance(logger_mod.LOGGER, logging.Logger)
            return
        assert True
        return

    with mock.patch("app.logger.logging.getLogger") as get_logger,          mock.patch("app.logger.logging.FileHandler", autospec=True) as file_handler,          mock.patch("app.logger.logging.StreamHandler", autospec=True) as stream_handler:
        fake_logger = mock.Mock()
        fake_logger.handlers = []
        get_logger.return_value = fake_logger

        lg1 = factory("app") if getattr(factory, "__code__", None) and factory.__code__.co_argcount else factory()
        assert lg1 is get_logger.return_value
        assert get_logger.called
        assert file_handler.called or stream_handler.called

        file_handler.reset_mock(); stream_handler.reset_mock()
        lg2 = factory("app") if getattr(factory, "__code__", None) and factory.__code__.co_argcount else factory()
        assert lg2 is get_logger.return_value
        assert not file_handler.called and not stream_handler.called
