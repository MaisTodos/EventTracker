import json
import logging
import time
import uuid
from typing import List, Optional

import boto3

from .dtos import TrackerEvent, TrackerException, TrackerMessage
from .interfaces import (
    ITrackerHandlerEvent,
    ITrackerHandlerException,
    ITrackerHandlerMessage,
)
from .types import Contexts, Tags

logger = logging.getLogger(__name__)


class Tracker:
    def __init__(
        self,
        message_handlers: Optional[List[ITrackerHandlerMessage]] = None,
        exception_handlers: Optional[List[ITrackerHandlerException]] = None,
        event_handlers: Optional[List[ITrackerHandlerEvent]] = None,
        app_id: Optional[str] = None,
    ):
        self.__message_handlers = message_handlers or []
        self.__exception_handlers = exception_handlers or []
        self.__event_handlers = event_handlers or []
        self.__app_id = app_id

    def __persist_dynamo(self, type_: str, payload: dict, tags=None, contexts=None):
        timestamp = int(time.time() * 1000)
        dynamo_client = boto3.client("dynamodb", region_name="us-east-1")
        table = "TrackerEvents"
        item = {
            "pk": {"S": f"APP#{self.__app_id or 'tracker'}"},
            "sk": {"S": f"{type_.upper()}#{timestamp}#{uuid.uuid4().hex[:6]}"},
            "type": {"S": type_},
            "timestamp": {"N": str(timestamp)},
            "payload": {"S": json.dumps(payload)},
            "tags": {"S": json.dumps(tags or {})},
            "contexts": {"S": json.dumps(contexts or {})},
        }

        try:
            dynamo_client.put_item(TableName=table, Item=item)
        except Exception as e:
            logger.warning(f"Failed to persist to DynamoDB: {e}")

    def set_tags(self, tags: Tags):
        handlers = (
            self.__event_handlers + self.__exception_handlers + self.__message_handlers
        )

        for handler in handlers:
            try:
                handler.set_tags(tags)
            except Exception as e:
                logger.error(f"Error setting tags for handler {handler}: {e}")

    def set_contexts(self, contexts: Contexts):
        handlers = (
            self.__event_handlers + self.__exception_handlers + self.__message_handlers
        )

        for handler in handlers:
            try:
                handler.set_contexts(contexts)
            except Exception as e:
                logger.error(f"Error setting contexts for handler {handler}: {e}")

    def emit_exception(self, tracker_exception: TrackerException):
        self.__persist_dynamo(
            "exception",
            {"exception": str(tracker_exception.exception)},
            tracker_exception.tags,
            tracker_exception.contexts,
        )

        for handler in self.__exception_handlers:
            try:
                handler.capture_exception(tracker_exception)
            except Exception as e:
                logger.error(f"Error emitting exception for handler {handler}: {e}")

    def emit_message(self, tracker_message: TrackerMessage):
        for handler in self.__message_handlers:
            try:
                handler.capture_message(tracker_message)
            except Exception as e:
                logger.error(f"Error emitting message for handler {handler}: {e}")

    def emit_event(self, tracker_event: TrackerEvent):
        for handler in self.__event_handlers:
            try:
                handler.capture_event(tracker_event)
            except Exception as e:
                logger.error(f"Error emitting event for handler {handler}: {e}")
