import logging


def test_track_when_string_event(caplog, logger_provider):
    with caplog.at_level(logging.INFO):
        logger_provider.track("test_message")

    event_record = caplog.records[0]
    assert event_record.levelname == "INFO"
    assert event_record.msg == "test_message"
    assert event_record.tags == {}
    assert event_record.contexts == {}


def test_track_when_exception_event(caplog, logger_provider):
    with caplog.at_level(logging.INFO):

        try:
            _ = 1 / 0
        except Exception as e:
            logger_provider.track(e)

    event_record = caplog.records[0]
    assert event_record.levelname == "ERROR"
    assert event_record.msg == "ZeroDivisionError('division by zero')"
    assert event_record.tags == {}
    assert event_record.contexts == {}
    assert event_record.exc_info is not None
    assert event_record.exc_info[2] is not None


def test_track_when_all_infos(caplog, logger_provider):
    with caplog.at_level(logging.INFO):
        logger_provider.track(
            "test_message",
            tags={"user": "john.doe"},
            contexts={"session": {"id": "abcd"}},
        )

    event_record = caplog.records[0]
    assert event_record.levelname == "INFO"
    assert event_record.msg == "test_message"
    assert event_record.tags == {"user": "john.doe"}
    assert event_record.contexts == {"session": {"id": "abcd"}}


def test_track_when_already_infos_set_and_new_infos(caplog, logger_provider):
    logger_provider.set_contexts({"session": {"id": "abcd"}})
    logger_provider.set_tags({"user": "jane.doe"})

    with caplog.at_level(logging.INFO):
        logger_provider.track(
            "test_message",
            tags={"new": "tag"},
            contexts={"new": {"info": "value"}},
        )

    event_record = caplog.records[0]
    assert event_record.levelname == "INFO"
    assert event_record.msg == "test_message"
    assert event_record.tags == {"user": "jane.doe", "new": "tag"}
    assert event_record.contexts == {
        "session": {"id": "abcd"},
        "new": {"info": "value"},
    }
