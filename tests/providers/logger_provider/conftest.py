import io
import logging

import pytest

from event_tracker.providers.logger_provider import (
    LoggerConfig,
    LoggerProvider,
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
def logger_provider() -> LoggerProvider:
    return LoggerProvider(LoggerConfig())
