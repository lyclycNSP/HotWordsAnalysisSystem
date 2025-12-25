from dataclasses import dataclass
from enum import Enum

class EventType(Enum):
    DATA = 1
    QUERY = 2

@dataclass
class Event:
    timestamp: int
    content: str | int
    event_type: EventType