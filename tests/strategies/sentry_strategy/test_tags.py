from unittest.mock import call


def test_set_tags(sentry_strategy, set_tag_mock):
    sentry_strategy.set_tags({"user": "john.doe", "blah": 123})

    assert call("user", "john.doe") in set_tag_mock.call_args_list
    assert call("blah", 123) in set_tag_mock.call_args_list
