# vpc_defender.py

from typing import Dict, List
from spells import ServerlessSpell, LambdaEdgeSpell, CloudFrontSpell
from security_measures import SecurityMeasures, SecurityStrategy, SecurityMeasure
from security_status import SecurityStatus
from character_stats import CharacterStats
from resources import Resources


class VPCDefender:
    def __init__(self, name: str, stats: CharacterStats):
        # Initialization of key attributes
        self.name = name
        self.stats = stats
        self.level = 1
        self.max_health = self.calculate_max_health()
        self.current_health = self.max_health
        self.preparation_points = 100

        # Measures (offensive and defensive)
        self.offensive_measures = SecurityMeasures.get_offensive_measures()
        self.defensive_measures = SecurityMeasures.get_defensive_measures()
        self.active_measures: List[SecurityMeasure] = []

        # Resource management
        self.resources = Resources(
            compute_points=100,
            network_bandwidth=50,
            storage_capacity=10,
            memory_capacity=128,      # Added missing required attributes
            latency_measure=5,        # Example values, adjust as needed
            security_level=3,
            data_integrity=95
        )

        # Status effects and inventory
        self.status_effects: List[SecurityStatus] = []
        self.inventory: List[SecurityMeasure] = []

        # Available spells
        self.spells: Dict[str, ServerlessSpell] = {
            "lambda_edge": LambdaEdgeSpell(),
            "cloudfront": CloudFrontSpell(),
        }

    def calculate_max_health(self) -> int:
        """Calculates max health based on character stats and current level."""
        return self.stats.calculate_max_health() + (self.level * 20)

    def cast_spell(self, spell_key: str) -> str:
        """
        Casts a serverless spell if the player has enough resources.
        Args:
            spell_key (str): The key representing the spell in the spellbook.

        Returns:
            str: Outcome message of casting the spell.
        """
        spell = self.spells.get(spell_key)
        if not spell:
            return f"Spell '{spell_key}' not found."
        if spell.cast(self):
            return f"Cast spell: {spell.name}."
        return f"Not enough resources to cast {spell.name}."

    def update_status_effects(self):
        """Updates status effects, removing those that have expired."""
        self.status_effects = [
            effect for effect in self.status_effects
            if not effect.tick()  # Assume 'tick()' returns True if still active, False if expired
        ]

    def take_damage(self, amount: int) -> str:
        """Applies damage to the defender and updates the health status."""
        self.current_health = max(0, self.current_health - amount)
        if self.current_health <= 0:
            return f"{self.name} has been defeated!"
        return f"{self.name} took {amount} damage. Current health: {self.current_health}/{self.max_health}"

    def heal(self, amount: int) -> str:
        """Heals the defender and updates health status."""
        self.current_health = min(
            self.max_health, self.current_health + amount)
        return f"{self.name} healed by {amount}. Current health: {self.current_health}/{self.max_health}"

    def add_active_measure(self, measure: SecurityMeasure) -> str:
        """Adds a security measure to active measures if enough preparation points are available."""
        if measure.cost > self.preparation_points:
            return f"Not enough preparation points to implement {measure.name}."
        self.active_measures.append(measure)
        self.preparation_points -= measure.cost
        return f"Implemented {measure.name}. Preparation points remaining: {self.preparation_points}"

    def level_up(self):
        """Levels up the defender, increasing stats and max health."""
        self.level += 1
        self.max_health += 20
        self.current_health = self.max_health
        return f"{self.name} leveled up! Level: {self.level}, Max Health: {self.max_health}"


# Example usage (testing the integration):
if __name__ == "__main__":
    # Create a new character stats instance
    stats = CharacterStats()

    # Initialize VPC Defender with stats
    defender = VPCDefender(name="CloudGuardian", stats=stats)

    # Cast a spell
    print(defender.cast_spell("lambda_edge"))

    # Apply damage
    print(defender.take_damage(30))

    # Heal the defender
    print(defender.heal(20))

    # Level up the defender
    print(defender.level_up())
