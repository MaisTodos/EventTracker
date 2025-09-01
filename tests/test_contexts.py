from unittest.mock import call
from event_tracker import EventTracker


def test_set_contexts(set_context_mock):
    # TODO: assert key are enum and string

    EventTracker.set_contexts(
        {
            "user": {"value": "john.doe"},
            "blah": {"bleh": 123},
        }
    )

    assert call("user", {"value": "john.doe"}) in set_context_mock.call_args_list
    assert call("blah", {"bleh": 123}) in set_context_mock.call_args_list


def test_set_contexts_when_none(set_context_mock):
    EventTracker.set_contexts(None)
    set_context_mock.assert_not_called()


def test_set_contexts_when_not_allowed_type_context(set_context_mock):
    EventTracker.set_contexts(
        {
            "user": {"value": "john.doe"},
            Exception: {"error": Exception("Test")},
        }
    )

    assert call("user", {"value": "john.doe"}) in set_context_mock.call_args_list
    assert not call(Exception, {"error": Exception("Test")}) in set_context_mock.call_args_list


def test_set_contexts_when_not_allowed_type_context(set_context_mock):
    # Should not raise error, only not call sentry. And call log
    ...
