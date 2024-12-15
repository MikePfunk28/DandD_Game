# security_status.py
from enum import Enum
from dataclasses import dataclass
from typing import Optional


class StatusType(Enum):
    BUFF = "buff"
    DEBUFF = "debuff"


@dataclass
class SecurityStatus:
    name: str
    duration: int
    effect_value: int
    status_type: StatusType
    description: Optional[str] = None

    def tick(self) -> bool:
        self.duration -= 1
        return self.duration <= 0
