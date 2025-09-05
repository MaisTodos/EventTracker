from enum import Enum


class EventTrackerTags(str, Enum):
    """Example tags for event tracking"""

    ERROR = "ERROR"
    STATUS_CODE = "STATUS_CODE"
    USER_ID = "USER_ID"
    DATABASE_OPERATION = "DATABASE_OPERATION"
    PARTNER = "PARTNER"
    USE_CASE = "USE_CASE"
    AUTH_STATUS = "AUTH_STATUS"
