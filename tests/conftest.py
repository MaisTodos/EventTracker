from enum import Enum
from unittest.mock import Mock

import pytest

from tracker import TrackerEvent, TrackerException, TrackerMessage


class TestEnum(Enum):
    TEST_EVENT = "test_event"
    ANOTHER_TEST_EVENT = "another_test_event"
    TEST_MESSAGE = "test_message"
    ANOTHER_TEST_MESSAGE = "another_test_message"


@pytest.fixture()
def tracker_event():
    return TrackerEvent(event=TestEnum.TEST_EVENT, tags=None, contexts=None)


@pytest.fixture()
def tracker_exception():
    return TrackerException(
        exception=Exception("Test Exception"), tags=None, contexts=None
    )


@pytest.fixture()
def tracker_message():
    return TrackerMessage(message=TestEnum.TEST_MESSAGE, tags=None, contexts=None)


@pytest.fixture()
def handlers_mocks():
    event_handlers = [Mock(), Mock()]
    message_handlers = [Mock(), Mock()]
    exception_handlers = [Mock(), Mock()]

    return {
        "event_handlers": event_handlers,
        "message_handlers": message_handlers,
        "exception_handlers": exception_handlers,
    }
