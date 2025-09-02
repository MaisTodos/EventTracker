from unittest.mock import call

from event_tracker import EventTracker
from event_tracker.enums import EventTrackerTags


def test_set_tags(set_tag_mock):
    EventTracker.set_tags(
        {
            "user": "john.doe",
            "blah": 123,
            EventTrackerTags.STATUS_CODE: 500,
        }
    )

    assert call("user", "john.doe") in set_tag_mock.call_args_list
    assert call("blah", 123) in set_tag_mock.call_args_list
    assert call("STATUS_CODE", 500) in set_tag_mock.call_args_list


def test_set_tags_when_not_allowed_type_tag(set_tag_mock):
    EventTracker.set_tags(
        {
            "user": "john.doe",
            Exception: Exception("Test"),
        }
    )

    assert call("user", "john.doe") in set_tag_mock.call_args_list
    assert call(Exception, Exception("Test")) not in set_tag_mock.call_args_list
