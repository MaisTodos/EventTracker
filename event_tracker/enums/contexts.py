from enum import Enum


class EventTrackerContexts(str, Enum):
    """Example contexts for event tracking"""
    REQUEST_DATA = "REQUEST_DATA"
    USER_DATA = "USER_DATA"
    RESPONSE_DATA = "RESPONSE_DATA"
    SESSION_DATA = "SESSION_DATA"
