# security_battle.py
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from vpc_defender import VPCDefender
    from threat import Threat
    from security_measures import SecurityStrategy


class SecurityBattle:
    """
    Manages the battle between the VPC Defender and a Threat.
    """

    def __init__(self, defender: 'VPCDefender', threat: 'Threat'):
        self.defender = defender
        self.threat = threat
        self.round = 1

    def start_battle(self):
        """
        Starts the battle until either the defender or the threat is defeated.
        """
        print(f"\nA threat '{
              self.threat.name}' has emerged! Preparing for battle...")
        print(f"Defender: {self.defender.name}")
        print(f"Level: {self.defender.level}")
        print(
            f"Health: {self.defender.current_health}/{self.defender.max_health}")
        while self.defender.is_alive() and self.threat.persistence > 0:
            print(f"\n--- Round {self.round} ---")
            self.player_turn()
            if not self.threat_defeated():
                self.threat_turn()
            self.round += 1
        if self.defender.is_alive() and self.threat.persistence <= 0:
            print("Threat has been neutralized!")
        elif not self.defender.is_alive():
            print("Defender has been defeated!")

    def player_turn(self):
        """
        Handles the defender's actions during their turn.
        """
        action = input(
            "Do you want to 'attack' or 'cast spell'? ").strip().lower()
        if action == 'attack':
            offensive_power = sum(
                measure.effectiveness for measure in self.defender.active_measures
                if measure.strategy == SecurityStrategy.OFFENSIVE
            )
            counter_damage = int(
                offensive_power * (1 + self.defender.stats.agility / 100))
            self.threat.power -= counter_damage
            self.threat.persistence -= 1  # Reduce threat persistence when attacked
            print(f"Attacked the threat! Dealt {counter_damage} damage.")
        elif action == 'cast spell':
            print("Available Spells:")
            for key, spell in self.defender.spells.items():
                print(f"- {key}: {spell.description}")
            spell_key = input("Enter the spell key to cast: ").strip().lower()
            result = self.defender.cast_spell(spell_key)
            print(result)
        else:
            print("Invalid action. Skipping turn.")

    def threat_turn(self):
        """
        Handles the threat's actions during its turn.
        """
        damage = self.threat.calculate_damage(self.defender)
        self.defender.take_damage(damage)
        print(f"The threat dealt {damage} damage to your defender.")

    def threat_defeated(self) -> bool:
        """
        Checks if the threat has been defeated.
        """
        return self.threat.power <= 0

    def special_attack(self):
        # Implementation of the special attack
        pass
