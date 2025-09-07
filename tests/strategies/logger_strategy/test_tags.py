from event_tracker.strategies.logger_strategy import _logger_tags


def test_logger_set_tags(logger_strategy):
    logger_strategy.set_tags({"user": "john.doe", "blah": 123})

    logger_tags = _logger_tags.get()
    assert logger_tags == {"user": "john.doe", "blah": 123}


def test_logger_set_tags_multiple_times(logger_strategy):
    logger_strategy.set_tags({"user": "john.dae", "bleh": 444})
    logger_strategy.set_tags({"endpoint": "/api/test"})

    logger_tags = _logger_tags.get()
    assert logger_tags == {"user": "john.dae", "bleh": 444, "endpoint": "/api/test"}
