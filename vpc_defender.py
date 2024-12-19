from typing import List
from character_stats import CharacterStats
from security_measures import SecurityMeasure, SecurityMeasures
from security_common import SecurityStrategy
from resources import Resources

class VPCDefender:
    def __init__(self, name: str, stats: CharacterStats):
        self.name = name
        self.stats = stats
        self.level = 1
        self.max_health = self.calculate_max_health()
        self.current_health = self.max_health
        self.offensive_measures = SecurityMeasures().get_offensive_measures()
        self.defensive_measures = SecurityMeasures().get_defensive_measures()
        self.hybrid_measures = SecurityMeasures().get_hybrid_measures()
        self.active_measures: List[SecurityMeasure] = []
        self.preparation_points = 100
        self.resources = Resources(
            compute_points=100,
            network_bandwidth=50,
            storage_capacity=10
        )

    def calculate_max_health(self) -> int:
        return self.stats.elasticity * 10 + self.stats.fault_tolerance * 5

    def is_alive(self) -> bool:
        return self.current_health > 0

    def level_up(self):
        self.level += 1
        self.max_health = self.calculate_max_health()
        self.current_health = self.max_health
        print(f"{self.name} has leveled up to Level {self.level}!")

    def add_active_measure(self, measure_name: str) -> str:
        measure = next((m for m in self.defensive_measures + self.offensive_measures + self.hybrid_measures if m.name.lower() == measure_name.lower()), None)
        if measure and self.preparation_points >= measure.cost:
            self.active_measures.append(measure)
            self.preparation_points -= measure.cost
            return f"Implemented {measure.name} with effectiveness bonus of {measure.effectiveness}."
        return "Insufficient preparation points or invalid measure."