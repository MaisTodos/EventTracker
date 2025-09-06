from unittest.mock import call


def test_set_contexts(sentry_provider, set_context_mock):
    sentry_provider.set_contexts(
        {
            "user": {"value": "john.doe"},
            "blah": {"bleh": 123},
            "bleh": None,
        }
    )

    assert call("user", {"value": "john.doe"}) in set_context_mock.call_args_list
    assert call("blah", {"bleh": 123}) in set_context_mock.call_args_list
    assert call("bleh", None) in set_context_mock.call_args_list
