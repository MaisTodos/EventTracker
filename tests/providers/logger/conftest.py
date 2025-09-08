import pytest

from tracker.providers.logger import LoggerCore, _logger_contexts, _logger_tags


@pytest.fixture()
def logger_core():
    return LoggerCore(LoggerCore.LoggerConfig())


@pytest.fixture(autouse=True)
def clear_logger_contexts_and_tags():
    _logger_contexts.set({})
    _logger_tags.set({})
    yield
    _logger_contexts.set({})
    _logger_tags.set({})
