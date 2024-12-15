# character_stats.py
from typing import List, Dict
from resources import Resources


class CharacterStats:
    def __init__(self):
        # Core attributes that map to system properties
        self.elasticity: int = 70      # Maps to strength
        self.agility: int = 75         # Maps to dexterity
        self.fault_tolerance: int = 65  # Maps to defense
        self.availability: int = 85     # Maps to awareness
        self.resilience: int = 80      # Maps to wisdom
        self.intelligence: int = 10     # Technical knowledge
        self.adaptability: int = 10     # Maps to charisma

        # Derived stats
        self.start_health = 100
        self.current_health = self.start_health
        self.security_status = "Safe"
        self.inventory = []
        self.level = 1
        self.max_health = self.calculate_max_health()
        self.preparation_points = 100

        # Resource management (assuming proper Resource class definition)
        self.resources = Resources(
            compute_points=100,
            network_bandwidth=50,
            storage_capacity=20,
            memory_capacity=128,
            latency_measure=5,
            security_level=10,
            data_integrity=95
        )

    def calculate_max_health(self) -> int:
        return self.elasticity * 10 + self.fault_tolerance * 5

    def take_damage(self, amount):
        self.current_health = max(0, self.current_health - amount)
        self.update_security_status()

    def heal(self, amount):
        self.current_health = min(
            self.start_health, self.current_health + amount)
        self.update_security_status()

    def update_security_status(self):
        if self.current_health >= 75:
            self.security_status = "Safe"
        elif self.current_health >= 40:
            self.security_status = "Caution"
        else:
            self.security_status = "Danger"

    def add_to_inventory(self, item):
        self.inventory.append(item)

    def remove_from_inventory(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False

    def get_stats(self):
        return {
            "health": f"{self.current_health}/{self.start_health}",
            "status": self.security_status,
            "inventory": self.inventory
        }


# Create a new character
player = CharacterStats()

# Check initial stats
print(player.get_stats())  # Full health, Safe status, empty inventory

# Add items to inventory
player.add_to_inventory("Health Potion")
player.add_to_inventory("Sword")

# Take some damage
# Health will be 70/100, status will change to "Caution"
player.take_damage(30)

# Use a healing item
player.heal(20)  # Health will be 90/100, status will return to "Safe"

print(player.intelligence)
