from dataclasses import dataclass
from enum import Enum
from typing import Optional

from .types import Contexts, Tags


@dataclass
class TrackerException:
    exception: Exception
    tags: Optional[Tags] = None
    contexts: Optional[Contexts] = None


@dataclass
class TrackerEvent:
    event: Enum
    tags: Optional[Tags] = None
    contexts: Optional[Contexts] = None


@dataclass
class TrackerMessage:
    message: Enum
    tags: Optional[Tags] = None
    contexts: Optional[Contexts] = None
