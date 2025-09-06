from event_tracker.providers.logger_provider import _logger_tags


def test_logger_set_tags(logger_provider):
    logger_provider.set_tags({"user": "john.doe", "blah": 123})

    logger_tags = _logger_tags.get()
    assert logger_tags == {"user": "john.doe", "blah": 123}


def test_logger_set_tags_multiple_times(logger_provider):
    logger_provider.set_tags({"user": "john.dae", "bleh": 444})
    logger_provider.set_tags({"endpoint": "/api/test"})

    logger_tags = _logger_tags.get()
    assert logger_tags == {"user": "john.dae", "bleh": 444, "endpoint": "/api/test"}
