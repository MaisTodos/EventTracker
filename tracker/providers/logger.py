import logging
from contextvars import ContextVar
from dataclasses import dataclass
from typing import Any, Dict, Optional

from ..dtos import TrackerException, TrackerMessage
from ..helpers import default_dict
from ..interfaces import ITrackerHandlerException, ITrackerHandlerMessage
from ..types import Contexts, Tags

_logger_tags = ContextVar("logger_tags", default=default_dict)
_logger_contexts = ContextVar("logger_contexts", default=default_dict)


class LoggerCore:
    @dataclass
    class LoggerConfig:
        logger_handler: Optional[logging.Handler] = None

    def __init__(self, config: LoggerConfig):
        self.logger = logging.getLogger("Tracker.LoggerCore")

        if len(self.logger.handlers):
            # Avoid adding multiple handlers
            return

        if config.logger_handler:
            self.logger.addHandler(config.logger_handler)
        else:
            handler = logging.StreamHandler()
            self.logger.addHandler(handler)

    def set_tags(self, tags: Tags):
        temp_logger_tags = _logger_tags.get().copy()
        temp_logger_tags.update(tags)
        _logger_tags.set(temp_logger_tags)

    def set_contexts(self, contexts: Contexts):
        temp_logger_contexts = _logger_contexts.get().copy()
        temp_logger_contexts.update(contexts)
        _logger_contexts.set(temp_logger_contexts)


class LoggerMessageHandler(ITrackerHandlerMessage):
    def __init__(self, core: LoggerCore):
        self.core = core

    def set_tags(self, tags: Tags):
        self.core.set_tags(tags)

    def set_contexts(self, contexts: Contexts):
        self.core.set_contexts(contexts)

    def capture_message(self, tracker_message: TrackerMessage):
        extra = {"tags": _logger_tags.get(), "contexts": _logger_contexts.get()}

        if tracker_message.tags:
            extra["tags"].update(tracker_message.tags)

        if tracker_message.contexts:
            extra["contexts"].update(tracker_message.contexts)

        self.core.logger.info(tracker_message.message.value, extra=extra)


class LoggerExceptionHandler(ITrackerHandlerException):
    def __init__(self, core: LoggerCore):
        self.core = core

    def set_tags(self, tags: Tags):
        self.core.set_tags(tags)

    def set_contexts(self, contexts: Contexts):
        self.core.set_contexts(contexts)

    def capture_exception(self, tracker_exception: TrackerException):
        extra = {
            "tags": _logger_tags.get(),
            "contexts": _logger_contexts.get(),
        }

        if tracker_exception.tags:
            extra["tags"].update(tracker_exception.tags)

        if tracker_exception.contexts:
            extra["contexts"].update(tracker_exception.contexts)

        self.core.logger.error(
            tracker_exception.exception.__class__.__name__,
            exc_info=tracker_exception.exception,
            extra=extra,
        )
