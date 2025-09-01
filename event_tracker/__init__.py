from typing import Any, Dict, Union

import sentry_sdk


class EventTracker:
    @staticmethod
    def set_tags(
        tags: Dict[str, str] = None,
    ) -> None:
        tags = tags or {}

        for key, value in tags.items():
            # TODO: ensure key and value are Enum or String
            sentry_sdk.set_tag(key, value)


    @staticmethod
    def set_contexts(
        contexts: Dict[str, Dict[Any, Any]] = None,
    ) -> None:
        contexts = contexts or {}
        for key, value in contexts.items():
            # TODO: ensure key and value are Enum or String
            sentry_sdk.set_context(key, value)


    @staticmethod
    def track(
        event: Union[str, Exception],
        tags: Dict[str, str] = None,
        contexts: Dict[str, Dict[Any, Any]] = None,
    ) -> None:
        EventTracker.set_tags(tags)
        EventTracker.set_contexts(contexts)

        if isinstance(event, Exception):
            sentry_sdk.capture_exception(event)

        else:
            sentry_sdk.capture_message(event)
