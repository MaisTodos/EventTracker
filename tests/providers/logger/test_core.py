import logging

from tracker.providers.logger import LoggerCore, _logger_contexts, _logger_tags


def test_logger_core_context_vars_and_tags_initial_state():
    assert _logger_tags.get() == {}
    assert _logger_contexts.get() == {}


def test_logger_core_init_with_config():
    logger = logging.getLogger("Tracker.LoggerCore")
    logger.handlers = []

    stream_handler = logging.StreamHandler()
    LoggerCore(LoggerCore.LoggerConfig(logger_handler=stream_handler))

    logger = logging.getLogger("Tracker.LoggerCore")
    assert len(logger.handlers) == 1
    assert logger.handlers[0] == stream_handler

    LoggerCore(LoggerCore.LoggerConfig())

    # No new handler added
    logger = logging.getLogger("Tracker.LoggerCore")
    assert len(logger.handlers) == 1
    assert logger.handlers[0] == stream_handler


def test_logger_core_init_without_config():
    logger = logging.getLogger("Tracker.LoggerCore")
    logger.handlers = []

    LoggerCore(LoggerCore.LoggerConfig())

    logger = logging.getLogger("Tracker.LoggerCore")
    assert len(logger.handlers) == 1
    assert isinstance(logger.handlers[0], logging.StreamHandler)


def test_logger_core_set_multiple_tags(logger_core):
    logger_core.set_tags({"tag1": "value1", "tag2": "value2"})
    logger_core.set_tags({"tag3": "value3"})

    assert _logger_tags.get() == {"tag1": "value1", "tag2": "value2", "tag3": "value3"}


def test_logger_core_set_multiple_contexts(logger_core):
    logger_core.set_contexts({"context1": "value1", "context2": "value2"})
    logger_core.set_contexts({"context3": "value3"})

    assert _logger_contexts.get() == {
        "context1": "value1",
        "context2": "value2",
        "context3": "value3",
    }
