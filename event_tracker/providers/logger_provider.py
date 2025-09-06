import logging
from contextvars import ContextVar
from typing import Optional, Union

from ..messages import Contexts, Tags
from ..provider_strategy import IProviderConfig, IProviderStrategy

_logger_tags = ContextVar("logger_tags", default={})
_logger_contexts = ContextVar("logger_contexts", default={})


class LoggerConfig(IProviderConfig):
    logger_formatter = None


class LoggerProvider(IProviderStrategy):

    def __init__(self, config: LoggerConfig):
        self.__logger = logging.getLogger("EventTracker")

        # TODO: avoid adding multiple handlers if multiple instances are created

        # handler = logging.StreamHandler()
        # if config.logger_formatter:
        #     handler.setFormatter(config.logger_formatter)
        # self.__logger.addHandler(handler)

    def set_tags(self, tags: Tags):
        temp_logger_tags = _logger_tags.get().copy()
        temp_logger_tags.update(tags)
        _logger_tags.set(temp_logger_tags)

    def set_contexts(self, contexts: Contexts):
        temp_logger_contexts = _logger_contexts.get().copy()
        temp_logger_contexts.update(contexts)
        _logger_contexts.set(temp_logger_contexts)

    def track(
        self,
        event: Union[str, Exception],
        tags: Optional[Tags] = None,
        contexts: Optional[Contexts] = None,
    ):

        if tags:
            self.set_tags(tags)

        if contexts:
            self.set_contexts(contexts)

        extra = {"tags": _logger_tags.get(), "contexts": _logger_contexts.get()}

        if isinstance(event, Exception):
            self.__logger.error(repr(event), exc_info=event, extra=extra)
        else:
            self.__logger.info(event, extra=extra)
        