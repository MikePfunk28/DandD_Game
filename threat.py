# threat.py
from dataclasses import dataclass
from typing import TYPE_CHECKING
import random  # This was missing
# This needs to be outside TYPE_CHECKING
from security_measures import SecurityStrategy

if TYPE_CHECKING:
    from vpc_defender import VPCDefender


@dataclass
class Threat:
    name: str
    attack_type: str
    power: int
    persistence: int
    adaptability: int

    def calculate_damage(self, defender: 'VPCDefender') -> int:
        """
        Calculates the damage inflicted by the threat on the defender.
        """
        base_damage = random.randint(self.power - 5, self.power + 5)
        # Apply defender's defensive measures
        for measure in defender.active_measures:
            if measure.strategy == SecurityStrategy.DEFENSIVE:
                base_damage = max(0, base_damage - measure.effectiveness)
        # Apply defender's stats for further damage reduction
        damage_reduction = (defender.stats.fault_tolerance +
                            defender.stats.resilience) / 100
        final_damage = int(base_damage * (1 - damage_reduction))
        return final_damage
