from event_tracker.providers.logger_provider import _logger_contexts


def test_logger_set_contexts(logger_provider):
    logger_provider.set_contexts(
        {"user": "john.doe", "blah": {"bleh": "123", "bluh": 456}}
    )

    logger_contexts = _logger_contexts.get()
    assert logger_contexts == {"user": "john.doe", "blah": {"bleh": "123", "bluh": 456}}


def test_logger_set_contexts_multiple_times(logger_provider):
    logger_provider.set_contexts({"endpoint": "/api/test"})
    logger_provider.set_contexts({"payload": {"item": "book", "price": 9.99}})

    logger_contexts = _logger_contexts.get()
    assert logger_contexts == {
        "endpoint": "/api/test",
        "payload": {"item": "book", "price": 9.99},
    }
