import pytest

from event_tracker.strategies.logger_strategy import (
    LoggerConfig,
    LoggerStrategy,
    _logger_contexts,
    _logger_tags,
)


@pytest.fixture(autouse=True)
def reset_logger_contextvars():

    _logger_tags.set({})
    _logger_contexts.set({})
    yield
    _logger_tags.set({})
    _logger_contexts.set({})


@pytest.fixture()
def logger_strategy() -> LoggerStrategy:
    return LoggerStrategy(LoggerConfig())
