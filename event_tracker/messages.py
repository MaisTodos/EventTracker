from typing import Dict, List, Optional, Union

Primitive = Union[str, int, float, bool, None]
JSONFields = Union[Primitive, List["JSONFields"], Dict[str, "JSONFields"]]
Tags = Dict[str, JSONFields]
Contexts = Dict[str, Dict[str, JSONFields]]


class EventTrackerMessage:
    name: str = "default_event"

    def __init__(
        self,
        message: Union[Exception, str],
        tags: Optional[Tags] = None,
        contexts: Optional[Contexts] = None,
    ):
        self.__message = message
        self.__tags = tags
        self.__contexts = contexts

    @property
    def message(self):
        return self.__message

    @property
    def tags(self) -> Optional[Tags]:
        return self.__tags

    @property
    def contexts(self) -> Optional[Contexts]:
        return self.__contexts
