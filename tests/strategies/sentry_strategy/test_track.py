def test_track_when_string_event(
    sentry_strategy,
    capture_message_mock,
    capture_exception_mock,
    set_tag_mock,
    set_context_mock,
):
    sentry_strategy.track("test_event")

    capture_message_mock.assert_called_once_with("test_event")
    capture_exception_mock.assert_not_called()
    set_tag_mock.assert_not_called()
    set_context_mock.assert_not_called()


def test_track_when_exception_event(
    sentry_strategy,
    capture_message_mock,
    capture_exception_mock,
    set_tag_mock,
    set_context_mock,
):
    test_exception = Exception("Test")

    sentry_strategy.track(test_exception)

    capture_message_mock.assert_not_called()
    capture_exception_mock.assert_called_once_with(test_exception)
    set_tag_mock.assert_not_called()
    set_context_mock.assert_not_called()


def test_track_when_all_infos(
    sentry_strategy,
    capture_message_mock,
    capture_exception_mock,
    set_tag_mock,
    set_context_mock,
):

    sentry_strategy.track(
        "test_message",
        tags={"user": "john.doe"},
        contexts={"request": {"id": "1234"}},
    )

    capture_message_mock.assert_called_once_with("test_message")
    capture_exception_mock.assert_not_called()
    set_tag_mock.assert_called_once_with("user", "john.doe")
    set_context_mock.assert_called_once_with("request", {"id": "1234"})
