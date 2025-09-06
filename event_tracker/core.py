from typing import List

from .messages import EventTrackerMessage
from .provider_strategy import IProviderStrategy


class EventTracker:
    def __init__(
        self,
        providers: List[IProviderStrategy],
    ):
        self.providers = providers

    # TODO: add add tags and context methods, that will be added to event, after

    def emit(self, event_message: EventTrackerMessage):
        for provider in self.providers:
            provider.track(
                event=event_message.message,
                tags=event_message.tags,
                contexts=event_message.contexts,
            )
