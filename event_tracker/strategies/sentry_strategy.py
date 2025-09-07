import logging
from dataclasses import dataclass
from typing import Optional, Union

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

from ..messages import Contexts, Tags
from ..provider_strategy import IProviderConfig, IProviderStrategy


@dataclass
class SentryConfig(IProviderConfig):
    dsn: str
    environment: str
    traces_sample_rate: Optional[float] = None


class SentryStrategy(IProviderStrategy):
    name: str = "sentry"

    def __init__(self, config: SentryConfig):
        # Setup Sentry SDK to not capture log error as issues
        sentry_logging_integration = LoggingIntegration(  # pragma: no mutate
            level=logging.DEBUG,
            event_level=None,
        )

        sentry_sdk.init(
            dsn=config.dsn,
            integrations=[sentry_logging_integration],
            environment=config.environment,
            traces_sample_rate=config.traces_sample_rate,
            enable_tracing=config.traces_sample_rate is not None
            and config.traces_sample_rate > 0,
        )

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

        if isinstance(event, Exception):
            sentry_sdk.capture_exception(event)
        else:
            sentry_sdk.capture_message(event)

    def set_tags(self, tags: Tags):
        for key, value in tags.items():
            sentry_sdk.set_tag(key, value)

    def set_contexts(self, context: Contexts):
        for key, value in context.items():
            sentry_sdk.set_context(key, value)
