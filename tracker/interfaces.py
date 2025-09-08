from abc import ABC, abstractmethod

from .blah import TrackerEvent, TrackerException, TrackerMessage


class ISetMixin(ABC):
    @abstractmethod
    def set_tags(self, tags): ...

    @abstractmethod
    def set_contexts(self, contexts): ...


class ITrackerHandlerException(ISetMixin, ABC):
    @abstractmethod
    def capture_exception(self, tracker_exception: TrackerException): ...


class ITrackerHandlerMessage(ISetMixin, ABC):
    @abstractmethod
    def capture_message(self, tracker_message: TrackerMessage): ...


class ITrackerHandlerEvent(ISetMixin, ABC):
    @abstractmethod
    def capture_event(self, tracker_event: TrackerEvent): ...
