import logging

from tracker.providers.logger import LoggerEventHandler


def test_logger_event_handler_capture(logger_core, tracker_event, caplog):
    event_handler = LoggerEventHandler(logger_core)

    event_handler.set_tags({"global_tag": "global_value"})
    event_handler.set_contexts({"global_context": "global_value"})

    with caplog.at_level(logging.INFO):
        event_handler.capture_event(tracker_event)

    assert len(caplog.records) == 1

    log_record = caplog.records[0]
    assert log_record.levelname == "INFO"
    assert log_record.message == "test_event"
    assert log_record.tags == {"global_tag": "global_value"}
    assert log_record.contexts == {"global_context": "global_value"}


def test_logger_event_handler_capture_with_local_tags_and_contexts(
    logger_core, tracker_event, caplog
):
    event_handler = LoggerEventHandler(logger_core)

    event_handler.set_tags({"global_tag": "global_value"})
    event_handler.set_contexts({"global_context": "global_value"})

    tracker_event.tags = {"local_tag": "local_value"}
    tracker_event.contexts = {"local_context": "local_value"}

    with caplog.at_level(logging.INFO):
        event_handler.capture_event(tracker_event)

    assert len(caplog.records) == 1

    log_record = caplog.records[0]
    assert log_record.levelname == "INFO"
    assert log_record.message == "test_event"
    assert log_record.tags == {
        "global_tag": "global_value",
        "local_tag": "local_value",
    }
    assert log_record.contexts == {
        "global_context": "global_value",
        "local_context": "local_value",
    }
