import json
import logging
import re
import time
from unittest.mock import Mock, call, patch

import pytest

from tracker.core import Tracker, TrackerException


def test_tracker_emit_without_handlers(
    tracker_message, tracker_exception, tracker_event
):
    tracker = Tracker()
    tracker.emit_event(tracker_event)
    tracker.emit_message(tracker_message)
    tracker.emit_exception(tracker_exception)


def test_tracker_set_tags_without_handlers():
    tracker = Tracker()
    tracker.set_tags({"key": "value"})


def test_tracker_set_contexts_without_handlers():
    tracker = Tracker()
    tracker.set_contexts({"context": {"detail": "info"}})


def test_tracker_emit_message(tracker_message, handlers_mocks):
    message_handler_one = handlers_mocks["message_handlers"][0]
    message_handler_two = handlers_mocks["message_handlers"][1]
    exception_handler = handlers_mocks["exception_handlers"][0]
    event_handler = handlers_mocks["event_handlers"][0]

    tracker = Tracker(
        message_handlers=[message_handler_one, message_handler_two],
        exception_handlers=[exception_handler],
        event_handlers=[event_handler],
    )

    tracker.emit_message(tracker_message)

    message_handler_one.capture_message.assert_called_once_with(tracker_message)
    message_handler_two.capture_message.assert_called_once_with(tracker_message)
    exception_handler.capture_exception.assert_not_called()
    event_handler.capture_event.assert_not_called()


def test_tracker_emit_exception(tracker_exception, handlers_mocks):
    exception_handler_one = handlers_mocks["exception_handlers"][0]
    exception_handler_two = handlers_mocks["exception_handlers"][1]
    event_handler = handlers_mocks["event_handlers"][0]
    message_handler = handlers_mocks["message_handlers"][0]

    tracker = Tracker(
        message_handlers=[message_handler],
        event_handlers=[event_handler],
        exception_handlers=[exception_handler_one, exception_handler_two],
    )

    tracker.emit_exception(tracker_exception)

    exception_handler_one.capture_exception.assert_called_once_with(tracker_exception)
    exception_handler_two.capture_exception.assert_called_once_with(tracker_exception)
    event_handler.capture_event.assert_not_called()
    message_handler.capture_message.assert_not_called()


def test_tracker_emit_event(tracker_event, handlers_mocks):
    event_handler_one = handlers_mocks["event_handlers"][0]
    event_handler_two = handlers_mocks["event_handlers"][1]
    message_handler = handlers_mocks["message_handlers"][0]
    exception_handler = handlers_mocks["exception_handlers"][0]

    tracker = Tracker(
        event_handlers=[event_handler_one, event_handler_two],
        message_handlers=[message_handler],
        exception_handlers=[exception_handler],
    )

    tracker.emit_event(tracker_event)

    event_handler_one.capture_event.assert_called_once_with(tracker_event)
    event_handler_two.capture_event.assert_called_once_with(tracker_event)
    message_handler.capture_message.assert_not_called()
    exception_handler.capture_exception.assert_not_called()


def test_tracker_emit_message_when_handler_raises(
    tracker_message, handlers_mocks, caplog
):
    message_handler_one = handlers_mocks["message_handlers"][0]
    message_handler_two = handlers_mocks["message_handlers"][1]
    message_handler_one.capture_message.side_effect = Exception("Handler Error")

    tracker = Tracker(message_handlers=[message_handler_one, message_handler_two])

    with caplog.at_level(logging.ERROR):
        tracker.emit_message(tracker_message)

    message_handler_one.capture_message.assert_called_once_with(tracker_message)
    message_handler_two.capture_message.assert_called_once_with(tracker_message)

    log_record = caplog.records[0]
    assert (
        log_record.message
        == f"Error emitting message for handler {message_handler_one}: Handler Error"
    )


def test_tracker_emit_exception_when_handler_raises(
    tracker_exception, handlers_mocks, caplog
):
    exception_handler_one = handlers_mocks["exception_handlers"][0]
    exception_handler_two = handlers_mocks["exception_handlers"][1]
    exception_handler_one.capture_exception.side_effect = Exception("Handler Error")

    tracker = Tracker(exception_handlers=[exception_handler_one, exception_handler_two])

    with caplog.at_level(logging.ERROR):
        tracker.emit_exception(tracker_exception)

    exception_handler_one.capture_exception.assert_called_once_with(tracker_exception)
    exception_handler_two.capture_exception.assert_called_once_with(tracker_exception)

    log_record = caplog.records[0]
    assert (
        log_record.message
        == f"Error emitting exception for handler {exception_handler_one}: Handler Error"
    )


def test_tracker_emit_event_when_handler_raises(tracker_event, handlers_mocks, caplog):
    event_handler_one = handlers_mocks["event_handlers"][0]
    event_handler_two = handlers_mocks["event_handlers"][1]
    event_handler_one.capture_event.side_effect = Exception("Handler Error")

    tracker = Tracker(event_handlers=[event_handler_one, event_handler_two])

    with caplog.at_level(logging.ERROR):
        tracker.emit_event(tracker_event)

    event_handler_one.capture_event.assert_called_once_with(tracker_event)
    event_handler_two.capture_event.assert_called_once_with(tracker_event)

    log_record = caplog.records[0]
    assert (
        log_record.message
        == f"Error emitting event for handler {event_handler_one}: Handler Error"
    )


def test_tracker_set_tags(handlers_mocks):
    message_handler = handlers_mocks["message_handlers"][0]
    exception_handler = handlers_mocks["exception_handlers"][0]
    event_handler = handlers_mocks["event_handlers"][0]

    tracker = Tracker(
        message_handlers=[message_handler],
        exception_handlers=[exception_handler],
        event_handlers=[event_handler],
    )

    tags = {"key": "value"}
    tracker.set_tags(tags)

    message_handler.set_tags.assert_called_once_with(tags)
    exception_handler.set_tags.assert_called_once_with(tags)
    event_handler.set_tags.assert_called_once_with(tags)


def test_tracker_set_tags_when_handler_raises(handlers_mocks, caplog):
    message_handler = handlers_mocks["message_handlers"][0]
    exception_handler = handlers_mocks["exception_handlers"][0]
    event_handler = handlers_mocks["event_handlers"][0]
    message_handler.set_tags.side_effect = Exception("Handler Error")

    tracker = Tracker(
        message_handlers=[message_handler],
        exception_handlers=[exception_handler],
        event_handlers=[event_handler],
    )

    tags = {"key": "value"}

    with caplog.at_level(logging.ERROR):
        tracker.set_tags(tags)

    message_handler.set_tags.assert_called_once_with(tags)
    exception_handler.set_tags.assert_called_once_with(tags)
    event_handler.set_tags.assert_called_once_with(tags)

    log_record = caplog.records[0]
    assert (
        log_record.message
        == f"Error setting tags for handler {message_handler}: Handler Error"
    )


def test_tracker_set_contexts(handlers_mocks):
    message_handler = handlers_mocks["message_handlers"][0]
    exception_handler = handlers_mocks["exception_handlers"][0]
    event_handler = handlers_mocks["event_handlers"][0]

    tracker = Tracker(
        message_handlers=[message_handler],
        exception_handlers=[exception_handler],
        event_handlers=[event_handler],
    )

    contexts = {"context": {"detail": "info"}}
    tracker.set_contexts(contexts)

    message_handler.set_contexts.assert_called_once_with(contexts)
    exception_handler.set_contexts.assert_called_once_with(contexts)
    event_handler.set_contexts.assert_called_once_with(contexts)


def test_tracker_set_contexts_when_handler_raises(handlers_mocks, caplog):
    message_handler = handlers_mocks["message_handlers"][0]
    exception_handler = handlers_mocks["exception_handlers"][0]
    event_handler = handlers_mocks["event_handlers"][0]
    message_handler.set_contexts.side_effect = Exception("Handler Error")

    tracker = Tracker(
        message_handlers=[message_handler],
        exception_handlers=[exception_handler],
        event_handlers=[event_handler],
    )

    contexts = {"context": {"detail": "info"}}

    with caplog.at_level(logging.ERROR):
        tracker.set_contexts(contexts)

    message_handler.set_contexts.assert_called_once_with(contexts)
    exception_handler.set_contexts.assert_called_once_with(contexts)
    event_handler.set_contexts.assert_called_once_with(contexts)

    log_record = caplog.records[0]
    assert (
        log_record.message
        == f"Error setting contexts for handler {message_handler}: Handler Error"
    )


def test_persist_dynamo_success(monkeypatch):
    tracker = Tracker()

    mock_client = Mock()
    monkeypatch.setattr("boto3.client", lambda *a, **kw: mock_client)

    tracker._Tracker__persist_dynamo("exception", {"foo": "bar"}, tags={"t": 1})

    mock_client.put_item.assert_called_once()
    call_args = mock_client.put_item.call_args[1]

    assert call_args["TableName"] == "TrackerEvents"
    item = call_args["Item"]

    assert re.match(r"APP#.*", item["pk"]["S"])
    assert re.match(r"EXCEPTION#\d+#\w{6}", item["sk"]["S"])
    assert json.loads(item["payload"]["S"]) == {"foo": "bar"}
    assert json.loads(item["tags"]["S"]) == {"t": 1}


def test_persist_dynamo_logs_when_put_fails(monkeypatch, caplog):
    tracker = Tracker()

    mock_client = Mock()
    mock_client.put_item.side_effect = Exception("boom")
    monkeypatch.setattr("boto3.client", lambda *a, **kw: mock_client)

    with caplog.at_level(logging.WARNING):
        tracker._Tracker__persist_dynamo("event", {"foo": "bar"})

    assert "Failed to persist to DynamoDB" in caplog.text


def test_emit_exception_when_handler_fails(
    tracker_exception, handlers_mocks, caplog, monkeypatch
):
    handler_one = handlers_mocks["exception_handlers"][0]
    handler_two = handlers_mocks["exception_handlers"][1]
    handler_one.capture_exception.side_effect = Exception("Handler Error")

    tracker = Tracker(exception_handlers=[handler_one, handler_two])

    mock_client = Mock()
    monkeypatch.setattr("boto3.client", lambda *a, **kw: mock_client)

    with caplog.at_level(logging.ERROR):
        tracker.emit_exception(tracker_exception)

    handler_one.capture_exception.assert_called_once_with(tracker_exception)
    handler_two.capture_exception.assert_called_once_with(tracker_exception)
    assert (
        f"Error emitting exception for handler {handler_one}: Handler Error"
        in caplog.text
    )


def test_persist_dynamo_builds_correct_item(monkeypatch):
    tracker = Tracker(app_id="myapp")

    mock_client = Mock()
    monkeypatch.setattr("boto3.client", lambda *a, **kw: mock_client)

    tracker._Tracker__persist_dynamo(
        "exception", {"foo": "bar"}, tags={"tag1": "value1"}, contexts={"user": "alice"}
    )

    put_item_call = mock_client.put_item.call_args[1]
    item = put_item_call["Item"]


    assert item["pk"]["S"] == "APP#myapp"

    assert item["type"]["S"] == "exception"

    assert item["timestamp"]["N"].isdigit()

    assert json.loads(item["payload"]["S"]) == {"foo": "bar"}

    assert json.loads(item["tags"]["S"]) == {"tag1": "value1"}

    assert json.loads(item["contexts"]["S"]) == {"user": "alice"}

    assert item["sk"]["S"].startswith("EXCEPTION#")


def test_persist_dynamo_defaults(monkeypatch):
    tracker = Tracker()

    mock_client = Mock()
    monkeypatch.setattr("boto3.client", lambda *a, **kw: mock_client)

    tracker._Tracker__persist_dynamo("event", {"x": 1})

    item = mock_client.put_item.call_args[1]["Item"]

    assert item["pk"]["S"] == "APP#tracker"

    assert json.loads(item["tags"]["S"]) == {}
    assert json.loads(item["contexts"]["S"]) == {}



def test_emit_exception_persists_and_calls_handlers(monkeypatch):
    mock_client = Mock()
    monkeypatch.setattr("boto3.client", lambda *a, **kw: mock_client)

    handler1 = Mock()
    handler2 = Mock()

    tracker = Tracker(exception_handlers=[handler1, handler2])
    exc = TrackerException(ValueError("boom"), tags={"t": 1}, contexts={"c": 2})

    tracker.emit_exception(exc)

    item = mock_client.put_item.call_args[1]["Item"]
    assert json.loads(item["payload"]["S"]) == {"exception": "boom"}
    assert json.loads(item["tags"]["S"]) == {"t": 1}
    assert json.loads(item["contexts"]["S"]) == {"c": 2}

    handler1.capture_exception.assert_called_once_with(exc)
    handler2.capture_exception.assert_called_once_with(exc)


def test_emit_exception_handler_failure(monkeypatch, caplog):
    mock_client = Mock()
    monkeypatch.setattr("boto3.client", lambda *a, **kw: mock_client)

    handler1 = Mock()
    handler1.capture_exception.side_effect = Exception("Handler broken")
    handler2 = Mock()

    tracker = Tracker(exception_handlers=[handler1, handler2])
    exc = TrackerException(ValueError("bad"))

    with caplog.at_level(logging.ERROR):
        tracker.emit_exception(exc)

    assert mock_client.put_item.called

    handler2.capture_exception.assert_called_once_with(exc)


    assert "Error emitting exception for handler" in caplog.text


def test_persist_dynamo_uses_correct_region(monkeypatch):
    """Kill mutation: 'us-east-1' -> 'XXus-east-1XX' or other string mutations"""
    tracker = Tracker()

    mock_boto3_client = Mock()
    monkeypatch.setattr("boto3.client", mock_boto3_client)

    tracker._Tracker__persist_dynamo("event", {"test": "data"})

    mock_boto3_client.assert_called_once_with("dynamodb", region_name="us-east-1")


def test_persist_dynamo_uses_correct_service(monkeypatch):
    """Kill mutation: 'dynamodb' -> 'XXdynamodbXX' or other string mutations"""
    tracker = Tracker()

    mock_boto3_client = Mock()
    monkeypatch.setattr("boto3.client", mock_boto3_client)

    tracker._Tracker__persist_dynamo("event", {"test": "data"})

    mock_boto3_client.assert_called_once_with("dynamodb", region_name="us-east-1")


def test_persist_dynamo_uses_correct_table_name(monkeypatch):
    """Kill mutation: 'TrackerEvents' -> 'XXTrackerEventsXX' or other string mutations"""
    tracker = Tracker()

    mock_client = Mock()
    monkeypatch.setattr("boto3.client", lambda *a, **kw: mock_client)

    tracker._Tracker__persist_dynamo("event", {"test": "data"})

    mock_client.put_item.assert_called_once()
    call_args = mock_client.put_item.call_args[1]
    assert call_args["TableName"] == "TrackerEvents"


def test_persist_dynamo_pk_format(monkeypatch):
    """Kill mutation: 'APP#' -> 'XXAPP#XX' or other prefix mutations"""
    tracker = Tracker(app_id="testapp")

    mock_client = Mock()
    monkeypatch.setattr("boto3.client", lambda *a, **kw: mock_client)

    tracker._Tracker__persist_dynamo("event", {"test": "data"})

    item = mock_client.put_item.call_args[1]["Item"]
    assert item["pk"]["S"] == "APP#testapp"


def test_persist_dynamo_sk_format_with_type_uppercase(monkeypatch):
    """Kill mutation: type_.upper() -> type_.lower() or type_ alone"""
    tracker = Tracker()

    mock_client = Mock()
    monkeypatch.setattr("boto3.client", lambda *a, **kw: mock_client)

    tracker._Tracker__persist_dynamo("event", {"test": "data"})

    item = mock_client.put_item.call_args[1]["Item"]
    assert item["sk"]["S"].startswith("EVENT#")
    assert not item["sk"]["S"].startswith("event#")


def test_persist_dynamo_default_app_id_string(monkeypatch):
    """Kill mutation: 'tracker' -> 'XXtrackerXX' in default app_id"""
    tracker = Tracker()

    mock_client = Mock()
    monkeypatch.setattr("boto3.client", lambda *a, **kw: mock_client)

    tracker._Tracker__persist_dynamo("event", {"test": "data"})

    item = mock_client.put_item.call_args[1]["Item"]
    assert item["pk"]["S"] == "APP#tracker"


def test_persist_dynamo_while_loop_breaks_on_success(monkeypatch):
    """Kill mutation: break -> continue or removal of break statement"""
    tracker = Tracker()

    mock_client = Mock()
    monkeypatch.setattr("boto3.client", lambda *a, **kw: mock_client)

    mock_client.put_item.return_value = {}

    tracker._Tracker__persist_dynamo("event", {"test": "data"})

    mock_client.put_item.assert_called_once()


def test_persist_dynamo_while_loop_breaks_on_exception(monkeypatch, caplog):
    """Kill mutation: break -> continue in exception handler"""
    tracker = Tracker()

    mock_client = Mock()
    mock_client.put_item.side_effect = Exception("DynamoDB error")
    monkeypatch.setattr("boto3.client", lambda *a, **kw: mock_client)

    import logging

    with caplog.at_level(logging.WARNING):
        tracker._Tracker__persist_dynamo("event", {"test": "data"})

    mock_client.put_item.assert_called_once()
    assert "Failed to persist to DynamoDB" in caplog.text


def test_persist_dynamo_json_dumps_payload(monkeypatch):
    """Kill mutation: json.dumps() calls or removal"""
    tracker = Tracker()

    mock_client = Mock()
    monkeypatch.setattr("boto3.client", lambda *a, **kw: mock_client)

    payload = {"complex": {"nested": "data"}}
    tracker._Tracker__persist_dynamo("event", payload)

    item = mock_client.put_item.call_args[1]["Item"]
    assert isinstance(item["payload"]["S"], str)
    assert json.loads(item["payload"]["S"]) == payload


def test_persist_dynamo_json_dumps_tags(monkeypatch):
    """Kill mutation: json.dumps() for tags"""
    tracker = Tracker()

    mock_client = Mock()
    monkeypatch.setattr("boto3.client", lambda *a, **kw: mock_client)

    tags = {"tag1": "value1"}
    tracker._Tracker__persist_dynamo("event", {"test": "data"}, tags=tags)

    item = mock_client.put_item.call_args[1]["Item"]
    assert isinstance(item["tags"]["S"], str)
    assert json.loads(item["tags"]["S"]) == tags


def test_persist_dynamo_json_dumps_contexts(monkeypatch):
    """Kill mutation: json.dumps() for contexts"""
    tracker = Tracker()

    mock_client = Mock()
    monkeypatch.setattr("boto3.client", lambda *a, **kw: mock_client)

    contexts = {"user": "alice"}
    tracker._Tracker__persist_dynamo("event", {"test": "data"}, contexts=contexts)

    item = mock_client.put_item.call_args[1]["Item"]
    assert isinstance(item["contexts"]["S"], str)
    assert json.loads(item["contexts"]["S"]) == contexts


def test_persist_dynamo_tags_or_empty_dict(monkeypatch):
    """Kill mutation: tags or {} -> tags or None or other mutations"""
    tracker = Tracker()

    mock_client = Mock()
    monkeypatch.setattr("boto3.client", lambda *a, **kw: mock_client)

    tracker._Tracker__persist_dynamo("event", {"test": "data"}, tags=None)

    item = mock_client.put_item.call_args[1]["Item"]
    assert json.loads(item["tags"]["S"]) == {}


def test_persist_dynamo_contexts_or_empty_dict(monkeypatch):
    """Kill mutation: contexts or {} -> contexts or None or other mutations"""
    tracker = Tracker()

    mock_client = Mock()
    monkeypatch.setattr("boto3.client", lambda *a, **kw: mock_client)

    tracker._Tracker__persist_dynamo("event", {"test": "data"}, contexts=None)

    item = mock_client.put_item.call_args[1]["Item"]
    assert json.loads(item["contexts"]["S"]) == {}


def test_emit_exception_str_conversion(monkeypatch):
    """Kill mutation: str(tracker_exception.exception) -> tracker_exception.exception"""
    tracker = Tracker()

    mock_client = Mock()
    monkeypatch.setattr("boto3.client", lambda *a, **kw: mock_client)

    exc = TrackerException(ValueError("test error"))
    tracker.emit_exception(exc)

    item = mock_client.put_item.call_args[1]["Item"]
    payload = json.loads(item["payload"]["S"])
    assert payload["exception"] == "test error"
    assert isinstance(payload["exception"], str)


def test_emit_exception_payload_key_name(monkeypatch):
    """Kill mutation: 'exception' key -> 'XXexceptionXX' or other mutations"""
    tracker = Tracker()

    mock_client = Mock()
    monkeypatch.setattr("boto3.client", lambda *a, **kw: mock_client)

    exc = TrackerException(ValueError("test"))
    tracker.emit_exception(exc)

    item = mock_client.put_item.call_args[1]["Item"]
    payload = json.loads(item["payload"]["S"])
    assert "exception" in payload
    assert payload["exception"] == "test"


def test_emit_exception_type_string(monkeypatch):
    """Kill mutation: 'exception' type string -> 'XXexceptionXX'"""
    tracker = Tracker()

    mock_client = Mock()
    monkeypatch.setattr("boto3.client", lambda *a, **kw: mock_client)

    exc = TrackerException(ValueError("test"))
    tracker.emit_exception(exc)

    item = mock_client.put_item.call_args[1]["Item"]
    assert item["type"]["S"] == "exception"


def test_persist_dynamo_timestamp_multiplication(monkeypatch):
    """Kill mutation: time.time() * 1000 -> time.time() * 999 or time.time() + 1000"""
    tracker = Tracker()

    mock_client = Mock()
    monkeypatch.setattr("boto3.client", lambda *a, **kw: mock_client)

    
    with patch("time.time", return_value=1609459200.123):
        tracker._Tracker__persist_dynamo("event", {"test": "data"})

    item = mock_client.put_item.call_args[1]["Item"]
    timestamp = int(item["timestamp"]["N"])

    expected = int(1609459200.123 * 1000)
    assert timestamp == expected
    assert timestamp == 1609459200123


def test_persist_dynamo_timestamp_int_conversion(monkeypatch):
    """Kill mutation: int(time.time() * 1000) -> time.time() * 1000 (no int conversion)"""
    tracker = Tracker()

    mock_client = Mock()
    monkeypatch.setattr("boto3.client", lambda *a, **kw: mock_client)

    tracker._Tracker__persist_dynamo("event", {"test": "data"})

    item = mock_client.put_item.call_args[1]["Item"]
    assert isinstance(item["timestamp"]["N"], str)
    timestamp_value = int(item["timestamp"]["N"])
    assert str(timestamp_value) == item["timestamp"]["N"]


def test_persist_dynamo_uuid_hex_slice(monkeypatch):
    """Kill mutation: uuid.uuid4().hex[:6] -> uuid.uuid4().hex[:5] or [:7]"""
    tracker = Tracker()

    mock_client = Mock()
    monkeypatch.setattr("boto3.client", lambda *a, **kw: mock_client)

    tracker._Tracker__persist_dynamo("event", {"test": "data"})

    item = mock_client.put_item.call_args[1]["Item"]
    sk_parts = item["sk"]["S"].split("#")
    uuid_part = sk_parts[2]

    assert len(uuid_part) == 6
    assert all(c in "0123456789abcdef" for c in uuid_part)


def test_persist_dynamo_app_id_or_logic(monkeypatch):
    """Kill mutation: self.__app_id or 'tracker' -> self.__app_id and 'tracker' or other logic"""
    tracker_none = Tracker(app_id=None)
    mock_client = Mock()
    monkeypatch.setattr("boto3.client", lambda *a, **kw: mock_client)

    tracker_none._Tracker__persist_dynamo("event", {"test": "data"})
    item = mock_client.put_item.call_args[1]["Item"]
    assert item["pk"]["S"] == "APP#tracker"

    mock_client.reset_mock()
    tracker_empty = Tracker(app_id="")
    tracker_empty._Tracker__persist_dynamo("event", {"test": "data"})
    item = mock_client.put_item.call_args[1]["Item"]
    assert item["pk"]["S"] == "APP#tracker"

    mock_client.reset_mock()
    tracker_valid = Tracker(app_id="myapp")
    tracker_valid._Tracker__persist_dynamo("event", {"test": "data"})
    item = mock_client.put_item.call_args[1]["Item"]
    assert item["pk"]["S"] == "APP#myapp"


def test_emit_exception_continues_after_handler_exception():
    """Kill mutation: continue -> break in exception handling loop"""
    handler1 = Mock()
    handler1.capture_exception.side_effect = Exception("First handler fails")
    handler2 = Mock()
    handler3 = Mock()

    tracker = Tracker(exception_handlers=[handler1, handler2, handler3])
    exc = TrackerException(ValueError("test"))

    tracker.emit_exception(exc)

    handler1.capture_exception.assert_called_once_with(exc)
    handler2.capture_exception.assert_called_once_with(
        exc
    ) 
    handler3.capture_exception.assert_called_once_with(exc) 


def test_persist_dynamo_string_type_attribute():
    """Kill mutation: 'S' type -> 'N' or other DynamoDB types"""
    tracker = Tracker()

    mock_client = Mock()
    with patch("boto3.client", return_value=mock_client):
        tracker._Tracker__persist_dynamo("event", {"test": "data"})

    item = mock_client.put_item.call_args[1]["Item"]

    # All string fields should use 'S' type
    assert "S" in item["pk"]
    assert "S" in item["sk"]
    assert "S" in item["type"]
    assert "S" in item["payload"]
    assert "S" in item["tags"]
    assert "S" in item["contexts"]

    # Timestamp should use 'N' type
    assert "N" in item["timestamp"]


def test_persist_dynamo_warning_log_message(monkeypatch, caplog):
    """Kill mutation: 'Failed to persist to DynamoDB' message"""
    tracker = Tracker()

    mock_client = Mock()
    mock_client.put_item.side_effect = Exception("Connection error")
    monkeypatch.setattr("boto3.client", lambda *a, **kw: mock_client)

    import logging

    with caplog.at_level(logging.WARNING):
        tracker._Tracker__persist_dynamo("event", {"test": "data"})

    # Check exact log message
    assert any(
        "Failed to persist to DynamoDB" in record.message for record in caplog.records
    )





def test_persist_dynamo_exception_path_logs_then_breaks(monkeypatch, caplog):
    """
    Ensure that in exception path, we log first THEN break
    This kills mutations that might reorder or remove the break
    """
    tracker = Tracker()

    mock_client = Mock()
    mock_client.put_item.side_effect = Exception("Test exception")
    monkeypatch.setattr("boto3.client", lambda *a, **kw: mock_client)

    import logging

    with caplog.at_level(logging.WARNING):
        tracker._Tracker__persist_dynamo("event", {"test": "data"})

    assert len(caplog.records) == 1
    assert "Failed to persist to DynamoDB: Test exception" in caplog.records[0].message

    assert mock_client.put_item.call_count == 1






def test_persist_dynamo_method_completes_after_success(monkeypatch):
    """
    Kill mutation: break -> return in success path
    Tests that the method fully completes and doesn't return early
    """
    tracker = Tracker(app_id="test_app")

    mock_time = Mock(return_value=1234567890.123)
    mock_uuid4 = Mock()
    mock_uuid4.hex = "abcdef123456"
    mock_uuid = Mock()
    mock_uuid.uuid4.return_value = mock_uuid4
    mock_json = Mock()
    mock_json.dumps.side_effect = lambda x: f"JSON({x})"

    mock_client = Mock()
    mock_client.put_item.return_value = {}
    mock_boto3_client = Mock(return_value=mock_client)

    monkeypatch.setattr("time.time", mock_time)
    monkeypatch.setattr("uuid.uuid4", mock_uuid.uuid4)
    monkeypatch.setattr("json.dumps", mock_json.dumps)
    monkeypatch.setattr("boto3.client", mock_boto3_client)

    tracker._Tracker__persist_dynamo("event", {"key": "value"}, {"tag": 1}, {"ctx": 2})

    mock_time.assert_called_once()
    mock_boto3_client.assert_called_once_with("dynamodb", region_name="us-east-1")
    mock_uuid.uuid4.assert_called_once()

    assert mock_json.dumps.call_count == 3
    expected_calls = [
        call({"key": "value"}),
        call({"tag": 1}),
        call({"ctx": 2}), 
    ]
    mock_json.dumps.assert_has_calls(expected_calls, any_order=True)

    mock_client.put_item.assert_called_once()
    call_args = mock_client.put_item.call_args[1]
    assert call_args["TableName"] == "TrackerEvents"

    item = call_args["Item"]
    assert item["pk"]["S"] == "APP#test_app"
    assert item["type"]["S"] == "event"
    assert "EVENT#" in item["sk"]["S"]


def test_persist_dynamo_method_completes_after_exception(monkeypatch, caplog):
    """
    Kill mutation: break -> return in exception path
    Tests that the method fully completes and doesn't return early
    """
    tracker = Tracker(app_id="test_app")

    mock_time = Mock(return_value=1234567890.123)
    mock_uuid4 = Mock()
    mock_uuid4.hex = "abcdef123456"
    mock_uuid = Mock()
    mock_uuid.uuid4.return_value = mock_uuid4
    mock_json = Mock()
    mock_json.dumps.side_effect = lambda x: f"JSON({x})"

    mock_client = Mock()
    mock_client.put_item.side_effect = Exception("DynamoDB error")
    mock_boto3_client = Mock(return_value=mock_client)

    monkeypatch.setattr("time.time", mock_time)
    monkeypatch.setattr("uuid.uuid4", mock_uuid.uuid4)
    monkeypatch.setattr("json.dumps", mock_json.dumps)
    monkeypatch.setattr("boto3.client", mock_boto3_client)

    import logging

    with caplog.at_level(logging.WARNING):
        tracker._Tracker__persist_dynamo(
            "message", {"msg": "test"}, {"tag": 1}, {"ctx": 2}
        )

    mock_boto3_client.assert_called_once_with("dynamodb", region_name="us-east-1")
    mock_uuid.uuid4.assert_called_once()

    assert mock_json.dumps.call_count == 3

    mock_client.put_item.assert_called_once()

    assert len(caplog.records) == 1
    assert "Failed to persist to DynamoDB" in caplog.records[0].message


def test_persist_dynamo_no_infinite_loop_on_success(monkeypatch):
    """
    Test to ensure single call on success (catches break -> continue mutation)
    """
    tracker = Tracker()

    mock_client = Mock()
    mock_client.put_item.return_value = {"success": True}
    monkeypatch.setattr("boto3.client", lambda *a, **kw: mock_client)

    tracker._Tracker__persist_dynamo("event", {"test": "data"})

    assert mock_client.put_item.call_count == 1


def test_persist_dynamo_no_infinite_loop_on_exception(monkeypatch, caplog):
    """
    Test to ensure single call on exception (catches break -> continue mutation)
    """
    tracker = Tracker()

    mock_client = Mock()
    mock_client.put_item.side_effect = Exception("Always fails")
    monkeypatch.setattr("boto3.client", lambda *a, **kw: mock_client)

    import logging

    with caplog.at_level(logging.WARNING):
        tracker._Tracker__persist_dynamo("event", {"test": "data"})

    assert mock_client.put_item.call_count == 1
    assert len(caplog.records) == 1
