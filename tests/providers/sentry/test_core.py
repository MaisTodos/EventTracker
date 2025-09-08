from tracker.providers.sentry import SentryCore


def test_sentry_core_with_tracing_enabled(mock_init):
    SentryCore(
        SentryCore.SentryConfig(
            dsn="http://example.com",
            environment="testing",
            traces_sample_rate=1.0,
        )
    )

    sentry_logging_integration = mock_init.call_args[1]["integrations"][0]

    mock_init.assert_called_once_with(
        dsn="http://example.com",
        environment="testing",
        integrations=[sentry_logging_integration],
        traces_sample_rate=1.0,
        enable_tracing=True,
    )


def test_sentry_core_with_tracing_disabled(mock_init):
    SentryCore(
        SentryCore.SentryConfig(
            dsn="http://example.com",
            environment="testing",
            traces_sample_rate=0.0,
        )
    )

    sentry_logging_integration = mock_init.call_args[1]["integrations"][0]
    mock_init.assert_called_once_with(
        dsn="http://example.com",
        environment="testing",
        integrations=[sentry_logging_integration],
        traces_sample_rate=0.0,
        enable_tracing=False,
    )


def test_sentry_core_capture_message(capture_message_mock):
    core = SentryCore(
        SentryCore.SentryConfig(
            dsn="http://example.com",
            environment="testing",
        )
    )

    core.capture_message("Test message")
    capture_message_mock.assert_called_once_with("Test message")


def test_sentry_core_capture_exception(capture_exception_mock):
    core = SentryCore(
        SentryCore.SentryConfig(
            dsn="http://example.com",
            environment="testing",
        )
    )

    exception = Exception("Test exception")

    core.capture_exception(exception)

    capture_exception_mock.assert_called_once_with(exception)


def test_sentry_core_set_tags(set_tag_mock):
    core = SentryCore(
        SentryCore.SentryConfig(
            dsn="http://example.com",
            environment="testing",
        )
    )

    core.set_tags({"key1": "value1", "key2": "value2"})
    core.set_tags({"key3": "value3"})

    set_tag_mock.assert_any_call("key1", "value1")
    set_tag_mock.assert_any_call("key2", "value2")
    set_tag_mock.assert_any_call("key3", "value3")
    assert set_tag_mock.call_count == 3


def test_sentry_core_set_contexts(set_context_mock):
    core = SentryCore(
        SentryCore.SentryConfig(
            dsn="http://example.com",
            environment="testing",
        )
    )

    core.set_contexts(
        {
            "context1": {"field1": "value1", "field2": 2},
            "context2": {"fieldA": True},
        }
    )
    core.set_contexts(
        {
            "context3": {"fieldX": [1, 2, 3]},
        }
    )

    set_context_mock.assert_any_call("context1", {"field1": "value1", "field2": 2})
    set_context_mock.assert_any_call("context2", {"fieldA": True})
    set_context_mock.assert_any_call("context3", {"fieldX": [1, 2, 3]})
    assert set_context_mock.call_count == 3
