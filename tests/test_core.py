from unittest.mock import Mock

from event_tracker.core import EventTracker
from event_tracker.messages import EventTrackerMessage


def test_event_tracker_emit_without_providers():
    tracker = EventTracker([])
    event_message = EventTrackerMessage(message="Test event")

    # This should not raise any exceptions
    tracker.emit(event_message)


def test_event_tracker_emit_when_one_provider_exists():
    message = "test event"
    tags = {"key1": "value1", "key2": 123}
    contexts = {"context1": {"detail": "info"}}

    mock = Mock()

    tracker = EventTracker([mock])
    event_message = EventTrackerMessage(
        message=message,
        tags=tags,
        contexts=contexts,
    )
    tracker.emit(event_message)

    mock.track.assert_called_once_with(
        event=message,
        tags=tags,
        contexts=contexts,
    )


def test_event_tracker_emit_when_multiple_providers_exist():
    message = "test event"
    tags = {"key1": "value1", "key2": 123}
    contexts = {"context1": {"detail": "info"}}

    mock1 = Mock()
    mock2 = Mock()

    tracker = EventTracker([mock1, mock2])
    event_message = EventTrackerMessage(
        message=message,
        tags=tags,
        contexts=contexts,
    )
    tracker.emit(event_message)

    mock1.track.assert_called_once_with(
        event=message,
        tags=tags,
        contexts=contexts,
    )

    mock2.track.assert_called_once_with(
        event=message,
        tags=tags,
        contexts=contexts,
    )
