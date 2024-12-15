# security_measures.py
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict


class SecurityStrategy(Enum):
    DEFENSIVE = "defensive"
    OFFENSIVE = "offensive"
    HYBRID = "hybrid"


@dataclass
class SecurityMeasure:
    name: str
    cost: Dict[str, int]
    effectiveness: int
    strategy: SecurityStrategy


class SecurityMeasures:
    @staticmethod
    def get_offensive_measures() -> List[SecurityMeasure]:
        return [
            SecurityMeasure(
                name="Firewall Rule",
                cost={"compute": 10, "network": 5},
                effectiveness=15,
                strategy=SecurityStrategy.OFFENSIVE
            ),
            SecurityMeasure(
                name="IDS Alert",
                cost={"compute": 15, "network": 10},
                effectiveness=20,
                strategy=SecurityStrategy.OFFENSIVE
            )
        ]

    @staticmethod
    def get_defensive_measures() -> List[SecurityMeasure]:
        return [
            SecurityMeasure(
                name="Encryption",
                cost={"compute": 20, "network": 5},
                effectiveness=25,
                strategy=SecurityStrategy.DEFENSIVE
            ),
            SecurityMeasure(
                name="Backup",
                cost={"compute": 10, "storage": 20},
                effectiveness=30,
                strategy=SecurityStrategy.DEFENSIVE
            )
        ]
