import logging

from tracker.blah import TrackerException
from tracker.providers.logger import LoggerExceptionHandler


def test_logger_exception_handler_capture(logger_core, caplog):
    exception_handler = LoggerExceptionHandler(logger_core)

    exception_handler.set_tags({"global_tag": "global_value"})
    exception_handler.set_contexts({"global_context": "global_value"})

    with caplog.at_level(logging.ERROR):
        try:
            _ = 1 / 0
        except ZeroDivisionError as e:
            exception_handler.capture_exception(TrackerException(exception=e))

    assert len(caplog.records) == 1

    log_record = caplog.records[0]
    assert log_record.levelname == "ERROR"
    assert log_record.message == "ZeroDivisionError"
    assert log_record.exc_info is not None
    assert log_record.exc_info[2] is not None
    assert log_record.tags == {"global_tag": "global_value"}
    assert log_record.contexts == {"global_context": "global_value"}


def test_logger_exception_handler_capture_with_local_tags_and_contexts(
    logger_core,
    caplog,
):
    exception_handler = LoggerExceptionHandler(logger_core)

    exception_handler.set_tags({"global_tag": "global_value"})
    exception_handler.set_contexts({"global_context": "global_value"})

    with caplog.at_level(logging.ERROR):
        try:
            _ = 1 / 0
        except ZeroDivisionError as e:
            exception_handler.capture_exception(
                TrackerException(
                    exception=e,
                    tags={"local_tag": "local_value"},
                    contexts={"local_context": {"local_value": 123}},
                )
            )

    assert len(caplog.records) == 1

    log_record = caplog.records[0]
    assert log_record.levelname == "ERROR"
    assert log_record.message == "ZeroDivisionError"
    assert log_record.tags == {
        "global_tag": "global_value",
        "local_tag": "local_value",
    }
    assert log_record.contexts == {
        "global_context": "global_value",
        "local_context": {"local_value": 123},
    }
