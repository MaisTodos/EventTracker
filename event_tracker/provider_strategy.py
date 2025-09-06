from abc import ABC, abstractmethod
from typing import Optional, Union

from .messages import Contexts, Tags


class IProviderConfig(ABC): ...


class IProviderStrategy(ABC):
    @abstractmethod
    def __init__(self, config: IProviderConfig): ...

    @abstractmethod
    def track(cls, event: Union[str, Exception], tags: Optional[Tags], contexts: Optional[Contexts]): ...

    @abstractmethod
    def set_tags(cls, tags: Tags): ...

    @abstractmethod
    def set_contexts(cls, contexts: Contexts): ...
