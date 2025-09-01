from event_tracker import EventTracker


def test_track_when_string_event(
    set_capture_message_mock,
    set_capture_exception_mock,
    set_tag_mock,
    set_context_mock,
):
    EventTracker.track("test_event")

    set_capture_message_mock.assert_called_once_with("test_event", level=None)
    set_capture_exception_mock.assert_not_called()
    set_tag_mock.assert_not_called()
    set_context_mock.assert_not_called()


def test_track_when_exception_event(
    set_capture_message_mock,
    set_capture_exception_mock,
    set_tag_mock,
    set_context_mock,
):
    test_exception = Exception("Test")

    EventTracker.track(test_exception)

    set_capture_message_mock.assert_not_called()
    set_capture_exception_mock.assert_called_once_with(test_exception)
    set_tag_mock.assert_not_called()
    set_context_mock.assert_not_called()
