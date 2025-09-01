from typing import Any, Dict, Union, Optional
from enum import Enum

import sentry_sdk


class EventTracker:
    @staticmethod
    def _extract_value(value: Any) -> Any:
        """Extract value from enum or return as-is"""
        return value.value if isinstance(value, Enum) else value

    @classmethod
    def set_contexts(cls, context: Dict[Union[str, Enum], Dict]) -> None:
        """Set context data on Sentry"""
        context = context or {}

        for key, value in context.items():
            sentry_sdk.set_context(cls._extract_value(key), value)

    @classmethod
    def set_tags(cls, tags: Dict[Union[str, Enum], Union[str, Enum]]) -> None:
        """Set tags (for filtering/indexing)"""
        tags = tags or {}

        for key, value in tags.items():
            sentry_sdk.set_tag(cls._extract_value(key), cls._extract_value(value))

    @classmethod
    def track(
        cls,
        event: Union[str, Enum],
        *,
        tags: Optional[Dict[Union[str, Enum], Any]] = None,
        context: Optional[Dict[str, Any]] = None,
        level: Optional[str] = None,
        error: Optional[Exception] = None,
    ) -> None:
        """
        Track an event with tags, context, and error handling

        Args:
            event: Event name or enum
            tags: Key-value pairs for indexing and filtering
            context: Rich data for detailed event analysis
            level: Severity level (info, warning, error)
            error: Associated exception (if any)
        """

        event_name = cls._extract_value(event)

        if tags:
            for tag, value in tags.items():
                tag_name = cls._extract_value(tag)
                processed_value = cls._extract_value(value)
                sentry_sdk.set_tag(tag_name, processed_value)

        if context:
            cls.set_contexts(context)

        if error:
            sentry_sdk.capture_exception(error)
            if event_name:
                sentry_sdk.capture_message(f"{event_name}", level=level
                                           or "error")
        else:
            sentry_sdk.capture_message(event_name, level=level)
