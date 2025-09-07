import logging

from event_tracker.strategies.logger_strategy import (
    LoggerConfig,
    LoggerStrategy,
)


def test_logger_strategy_init_with_config():

    logger = logging.getLogger("EventTracker.LoggerStrategy")
    logger.handlers = []

    logger_handler = logging.StreamHandler()
    config = LoggerConfig(logger_handler=logger_handler)
    LoggerStrategy(config)

    logger = logging.getLogger("EventTracker.LoggerStrategy")
    assert len(logger.handlers) == 1
    assert logger.handlers[0] == logger_handler

    logger = logging.getLogger("EventTracker.LoggerStrategy")
    assert len(logger.handlers) == 1
    assert logger.handlers[0] == logger_handler
