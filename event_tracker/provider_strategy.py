from abc import ABC, abstractmethod


class IProviderConfig(ABC): ...


class IProviderStrategy(ABC):
    @abstractmethod
    def __init__(self, config): ...

    @abstractmethod
    def track(cls, event, tags, context): ...

    @abstractmethod
    def set_tags(cls, tags): ...

    @abstractmethod
    def set_contexts(cls, context): ...
