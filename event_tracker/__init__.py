from typing import Any, Dict, Union, Optional
from enum import Enum

import sentry_sdk


class EventTrackerTags(str, Enum):
    ERROR = "ERROR"
    STATUS_CODE = "STATUS_CODE"
    USER_ID = "USER_ID"


class EventTrackerContexts(str, Enum):
    REQUEST_DATA = "REQUEST_DATA"
    RESPONSE_DATA = "RESPONSE_DATA"


class EventTracker:
    @staticmethod
    def _extract_value(value: Any) -> Any:
        """Extract value from enum or return as-is"""
        return value.value if isinstance(value, Enum) else value

    @classmethod
    def set_contexts(cls, context: Dict[Union[str, Enum], Dict]) -> None:
        """Set context data on Sentry"""
        context = context

        for key, value in context.items():
            sentry_sdk.set_context(cls._extract_value(key), value)

    @classmethod
    def set_tags(cls, tags: Dict[Union[str, Enum], Union[str, Enum]]) -> None:
        """Set tags (for filtering/indexing)"""
        tags = tags

        for key, value in tags.items():
            sentry_sdk.set_tag(cls._extract_value(key), cls._extract_value(value))

    @classmethod
    def track(
        cls,
        event: Union[str, Enum, Exception],
        *,
        tags: Optional[Dict[Union[str, Enum], Any]] = None,
        context: Optional[Dict[str, Any]] = None,
        level: Optional[str] = None,
    ) -> None:
        """
        Track an event with tags, context, and error handling

        Args:
            event: Event name or enum or Exception
            tags: Key-value pairs for indexing and filtering
            context: Rich data for detailed event analysis
            level: Severity level (info, warning, error)
        """
        if tags:
            cls.set_tags(tags)

        if context:
            cls.set_contexts(context)

        if isinstance(event, Exception):
            sentry_sdk.capture_exception(event)
        else:
            sentry_sdk.capture_message(cls._extract_value(event), level=level)
