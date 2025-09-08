from dataclasses import dataclass
from enum import Enum
from typing import List, Mapping, Optional, Union

Primitive = Union[str, int, float, bool, None]
JSONFields = Union[Primitive, List["JSONFields"], Mapping[str, "JSONFields"]]
Tags = Mapping[str, Primitive]
Contexts = Mapping[str, Mapping[str, JSONFields]]


@dataclass
class TrackerException:
    exception: Exception
    tags: Optional[Tags] = None
    contexts: Optional[Contexts] = None


@dataclass
class TrackerEvent:
    event: Enum
    tags: Optional[Tags]
    contexts: Optional[Contexts]


@dataclass
class TrackerMessage:
    message: Enum
    tags: Optional[Tags] = None
    contexts: Optional[Contexts] = None
