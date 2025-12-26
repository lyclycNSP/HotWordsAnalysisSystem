from dataclasses import dataclass
from enum import Enum

# 使用枚举，避免魔法数字
class EventType(Enum):
    DATA = 1
    QUERY = 2

# 使用数据类便于传递每一行弹幕数据
@dataclass
class Event:
    timestamp: int
    content: str | int
    event_type: EventType