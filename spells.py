# spells.py
from abc import ABC, abstractmethod
from typing import Dict
from security_status import SecurityStatus, StatusType


class ServerlessSpell(ABC):
    def __init__(self, name: str, cost: Dict[str, int]):
        self.name = name
        self.cost = cost

    @abstractmethod
    def cast(self, caster) -> bool:
        pass


class LambdaEdgeSpell(ServerlessSpell):
    def __init__(self):
        super().__init__("Lambda Edge", {"compute": 20, "network": 15})

    def cast(self, caster) -> bool:
        if caster.resources.consume(self.cost):
            caster.status_effects.append(
                SecurityStatus(
                    name="Edge Computing",
                    duration=3,
                    effect_value=15,
                    status_type=StatusType.BUFF,
                    description="Increased computing power at edge locations"
                )
            )
            return True
        return False


class CloudFrontSpell(ServerlessSpell):
    def __init__(self):
        super().__init__("CloudFront Shield", {"compute": 25, "network": 25})

    def cast(self, caster) -> bool:
        if caster.resources.consume(self.cost):
            caster.status_effects.append(
            SecurityStatus(
                name="Edge Computing",
                duration=3,
                effect_value=15,
                status_type=StatusType.BUFF,
                description="Increased computing power at edge locations",
                )
            )
            return True
        return False
