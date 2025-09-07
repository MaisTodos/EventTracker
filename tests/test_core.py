from unittest.mock import Mock

from event_tracker.core import EventTracker
from event_tracker.messages import DefaultEvent


def create_mock_strategy(name: str) -> Mock:
    mock = Mock()
    mock.name = name
    return mock


def test_event_tracker_init_with_no_strategy_messages():
    tracker = EventTracker(
        [],
        strategies_by_message={
            "some_event": ["nonexistent_provider"],
            "another_event": ["another_nonexistent_provider"],
            "bad_event": [],
        },
    )
    event_message = DefaultEvent(message="Test event")

    # This should not raise any exceptions
    tracker.emit(event_message)


def test_event_tracker_emit_without_providers():
    tracker = EventTracker([])
    event_message = DefaultEvent(message="Test event")

    # This should not raise any exceptions
    tracker.emit(event_message)


def test_event_tracker_emit_when_one_provider():
    message = "test event"
    tags = {"key1": "value1", "key2": 123}
    contexts = {"context1": {"detail": "info", "blah": 123}}

    mock_strategy = create_mock_strategy("mock_strategy")

    tracker = EventTracker([mock_strategy])
    event_message = DefaultEvent(
        message=message,
        tags=tags,
        contexts=contexts,
    )
    tracker.emit(event_message)

    mock_strategy.track.assert_called_once_with(
        event=message,
        tags=tags,
        contexts=contexts,
    )


def test_event_tracker_emit_when_multiple_providers():
    message = "test event"
    tags = {"key1": "value1", "key2": 123}
    contexts = {"context1": {"detail": "info", "blah": 123}}

    mock_strategy_one = create_mock_strategy("mock_strategy_one")
    mock_strategy_two = create_mock_strategy("mock_strategy_two")

    tracker = EventTracker([mock_strategy_one, mock_strategy_two])
    event_message = DefaultEvent(
        message=message,
        tags=tags,
        contexts=contexts,
    )
    tracker.emit(event_message)

    mock_strategy_one.track.assert_called_once_with(
        event=message,
        tags=tags,
        contexts=contexts,
    )

    mock_strategy_two.track.assert_called_once_with(
        event=message,
        tags=tags,
        contexts=contexts,
    )


def test_event_tracker_emit_when_strategy_raises_exception():
    message = "test event"
    tags = {"key1": "value1", "key2": 123}
    contexts = {"context1": {"detail": "info", "blah": 123}}

    mock_strategy_one = create_mock_strategy("mock_strategy_one")
    mock_strategy_two = create_mock_strategy("mock_strategy_two")
    mock_strategy_two.track.side_effect = Exception("Strategy error")

    tracker = EventTracker([mock_strategy_one, mock_strategy_two])
    event_message = DefaultEvent(
        message=message,
        tags=tags,
        contexts=contexts,
    )

    # This should not raise any exceptions despite one strategy failing
    tracker.emit(event_message)

    mock_strategy_one.track.assert_called_once_with(
        event=message,
        tags=tags,
        contexts=contexts,
    )

    mock_strategy_two.track.assert_called_once_with(
        event=message,
        tags=tags,
        contexts=contexts,
    )


def test_event_tracker_emit_with_providers_names():
    message = "test event"

    mock_strategy_one = create_mock_strategy("mock_strategy_one")
    mock_strategy_two = create_mock_strategy("mock_strategy_two")

    tracker = EventTracker([mock_strategy_one, mock_strategy_two])
    event_message = DefaultEvent(
        message=message,
    )
    tracker.emit(event_message, strategies_names=["fake", mock_strategy_one.name])

    mock_strategy_one.track.assert_called_once_with(
        event=message,
        tags=None,
        contexts=None,
    )

    mock_strategy_two.track.assert_not_called()


def test_event_tracker_emit_for_all_providers_when_nonexistent_provider_name():
    message = "test event"

    mock_strategy_one = create_mock_strategy("mock_strategy_one")
    mock_strategy_two = create_mock_strategy("mock_strategy_two")

    tracker = EventTracker([mock_strategy_one, mock_strategy_two])
    event_message = DefaultEvent(
        message=message,
    )
    tracker.emit(event_message, strategies_names=["nonexistent_provider"])

    mock_strategy_one.track.assert_called_once_with(
        event=message,
        tags=None,
        contexts=None,
    )
    mock_strategy_two.track.assert_called_once_with(
        event=message,
        tags=None,
        contexts=None,
    )


def test_event_tracker_emit_when_strategy_by_message():
    message = "test event"

    mock_strategy = create_mock_strategy("mock_strategy")
    mock_strategy_message = create_mock_strategy("mock_strategy_message")

    tracker = EventTracker(
        [mock_strategy, mock_strategy_message],
        strategies_by_message={
            "not_value_event": ["not_used_provider"],
            "default_event": [mock_strategy_message.name],
        },
    )

    event_message = DefaultEvent(message=message)
    tracker.emit(event_message)

    mock_strategy.track.assert_not_called()
    mock_strategy_message.track.assert_called_once_with(
        event=message,
        tags=None,
        contexts=None,
    )


def test_event_tracker_emit_when_strategy_by_message_and_names():
    message = "test event"

    mock_strategy_one = create_mock_strategy("mock_strategy_one")
    mock_strategy_two = create_mock_strategy("mock_strategy_two")
    mock_strategy_message = create_mock_strategy("mock_strategy_message")

    tracker = EventTracker(
        [mock_strategy_one, mock_strategy_two, mock_strategy_message],
        strategies_by_message={"default_event": [mock_strategy_message.name]},
    )

    event_message = DefaultEvent(message=message)
    tracker.emit(event_message, strategies_names=[mock_strategy_one.name])

    mock_strategy_one.track.assert_called_once_with(
        event=message,
        tags=None,
        contexts=None,
    )
    mock_strategy_two.track.assert_not_called()
    mock_strategy_message.track.assert_called_once_with(
        event=message,
        tags=None,
        contexts=None,
    )


def test_event_tracker_set_tags():
    tags = {"key1": "value1", "key2": 123}

    mock_strategy_one = create_mock_strategy("mock_strategy_one")
    mock_strategy_two = create_mock_strategy("mock_strategy_two")

    tracker = EventTracker([mock_strategy_one, mock_strategy_two])
    tracker.set_tags(tags)

    mock_strategy_one.set_tags.assert_called_once_with(tags)
    mock_strategy_two.set_tags.assert_called_once_with(tags)


def test_event_tracker_set_tags_with_strategies_names():
    tags = {"key1": "value1", "key2": 123}

    mock_strategy_one = create_mock_strategy("mock_strategy_one")
    mock_strategy_two = create_mock_strategy("mock_strategy_two")

    tracker = EventTracker([mock_strategy_one, mock_strategy_two])
    tracker.set_tags(tags, strategies_names=[mock_strategy_one.name])

    mock_strategy_one.set_tags.assert_called_once_with(tags)
    mock_strategy_two.set_tags.assert_not_called()


def test_event_tracker_set_tags_when_strategy_raises_exception():
    tags = {"key1": "value1", "key2": 123}

    mock_strategy_one = create_mock_strategy("mock_strategy_one")
    mock_strategy_two = create_mock_strategy("mock_strategy_two")
    mock_strategy_two.set_tags.side_effect = Exception("Strategy error")

    tracker = EventTracker([mock_strategy_one, mock_strategy_two])

    # This should not raise any exceptions despite one strategy failing
    tracker.set_tags(tags)

    mock_strategy_one.set_tags.assert_called_once_with(tags)
    mock_strategy_two.set_tags.assert_called_once_with(tags)


def test_event_tracker_set_contexts():
    contexts = {"context1": {"detail": "info", "number": 42}}

    mock_strategy_one = create_mock_strategy("mock_strategy_one")
    mock_strategy_two = create_mock_strategy("mock_strategy_two")

    tracker = EventTracker([mock_strategy_one, mock_strategy_two])
    tracker.set_contexts(contexts)

    mock_strategy_one.set_contexts.assert_called_once_with(contexts)
    mock_strategy_two.set_contexts.assert_called_once_with(contexts)


def test_event_tracker_set_contexts_with_strategies_names():
    contexts = {"context1": {"detail": "info", "blah": 123}}

    mock_strategy_one = create_mock_strategy("mock_strategy_one")
    mock_strategy_two = create_mock_strategy("mock_strategy_two")

    tracker = EventTracker([mock_strategy_one, mock_strategy_two])
    tracker.set_contexts(contexts, strategies_names=[mock_strategy_one.name])

    mock_strategy_one.set_contexts.assert_called_once_with(contexts)
    mock_strategy_two.set_contexts.assert_not_called()


def test_event_tracker_set_contexts_when_strategy_raises_exception():
    contexts = {"context1": {"detail": "info", "blah": 123}}

    mock_strategy_one = create_mock_strategy("mock_strategy_one")
    mock_strategy_two = create_mock_strategy("mock_strategy_two")
    mock_strategy_two.set_contexts.side_effect = Exception("Strategy error")

    tracker = EventTracker([mock_strategy_one, mock_strategy_two])

    # This should not raise any exceptions despite one strategy failing
    tracker.set_contexts(contexts)

    mock_strategy_one.set_contexts.assert_called_once_with(contexts)
    mock_strategy_two.set_contexts.assert_called_once_with(contexts)
