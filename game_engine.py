from game_board import GameBoard
from player import Player
from vpc_defender import VPCDefender
from threat_generator import generate_threat_for_region
from security_battle import SecurityBattle
from character_stats import CharacterStats
from security_measures import SecurityMeasure
from opening_scene import start_interview
import time

class GameEngine:
    """
    The GameEngine class manages the core logic, state, and interactions of the game.
    """

    def __init__(self):
        """
        Initializes the game engine with default settings.
        """
        self.players = []
        self.defenders = []
        self.game_board = GameBoard()
        self.max_sessions = 5
        self.winning_score = 500
        self.session_count = 1
        self.player_points = {}

    def initialize_game(self):
        """
        Initializes the game by setting up players and defenders.
        """
        print("=== Welcome to the Cloud Security Battle ===")
        number_of_players = int(input("Enter the number of players: ").strip())

        for i in range(number_of_players):
            player_name = input(f"Enter the name for Player {i + 1}: ").strip()
            player = Player(name=player_name, game_board=self.game_board)
            player.set_home_region()
            self.players.append(player)

            stats = CharacterStats()
            defender = VPCDefender(name=player.name + "'s Defender", stats=stats)
            player.defender = defender
            self.defenders.append(defender)

            self.player_points[player.name] = 0

    def run_game_session(self, player, defender):
        """
        Runs a single game session for a player and returns the points earned.
        """
        session_points = 0
        game_over = False

        while not game_over:
            print("\n=== New Turn ===")

            move_choice = input("Do you want to 'roll' the die or 'draw' a card to move? (roll/draw): ").strip().lower()
            if move_choice == 'roll':
                steps = player.roll_dice()
                print(f"You rolled a {steps}.")
            elif move_choice == 'draw':
                steps = player.draw_card()
                print(f"You drew a card and move {steps} steps.")
            else:
                print("Invalid choice. Defaulting to rolling the die.")
                steps = player.roll_dice()
                print(f"You rolled a {steps}.")

            landed_region, landed_az = player.move(steps)

            if landed_region != player.home_region:
                regional_charge = 10
                if defender.preparation_points >= regional_charge:
                    defender.preparation_points -= regional_charge
                    print(f"Operating in {landed_region.name} incurs a charge of {regional_charge} preparation points.")
                else:
                    print("Insufficient preparation points to cover regional charges.")

            print("\n--- Setup Phase ---")
            print(f"Preparation Points: {defender.preparation_points}")
            print("Available Defensive Measures:")
            for measure in defender.defensive_measures:
                print(f"- {measure.name}: {measure.description} (Cost: {measure.cost}, Effectiveness: {measure.effectiveness})")


            while True:
                setup_action = input("Enter 'measure' to implement a security measure or 'done' to finish setup: ").strip().lower()
                if setup_action == 'measure':
                    measure_name = input("Enter the measure key to implement: ").strip().lower()
                    result = defender.add_active_measure(measure_name)
                    print(result)
                elif setup_action == 'done':
                    if len(defender.active_measures) == 0:
                        print("You must implement at least one security measure before proceeding.")
                    else:
                        print("Setup phase completed.")
                        break
                else:
                    print("Invalid action. Please enter 'measure' or 'done'.")

            print("\n--- Threat Encounter ---")
            threat = generate_threat_for_region(landed_region.name)

            print(f"Threat Details: {threat.name}, Power: {threat.power}, Persistence: {threat.persistence}, Adaptability: {threat.adaptability}")

            battle = SecurityBattle(defender, threat)
            battle.start_battle()

            if not defender.is_alive():
                print("Your defender has been compromised! Game Over.")
                game_over = True
            elif battle.threat_defeated():
                print(f"Successfully defeated the threat: {threat.name}!")
                defender.level_up()
                session_points += 100
            else:
                print("The threat remains active.")

            continue_choice = input("Do you want to continue to the next turn? (yes/no): ").strip().lower()
            if continue_choice != 'yes':
                print("Ending the current game session.")
                game_over = True

        return session_points

    def continuous_game_loop(self):
        """
        Manages the overall game loop, running multiple sessions until a player wins or the maximum number of sessions is reached.
        """
        self.initialize_game()

        while self.session_count <= self.max_sessions:
            print(f"\n=== Game Session {self.session_count} ===")
            for idx, player in enumerate(self.players):
                print(f"\n--- {player.name}'s Turn ---")
                points_earned = self.run_game_session(player, self.defenders[idx])
                self.player_points[player.name] += points_earned
                print(f"{player.name} earned {points_earned} points this session.")
                print(f"Total Points: {self.player_points[player.name]}")

                self.defenders[idx].current_health = self.defenders[idx].max_health
                self.defenders[idx].preparation_points = 100
                self.defenders[idx].active_measures.clear()

                if self.player_points[player.name] >= self.winning_score:
                    print(f"\nCongratulations, {player.name}! You have won the game with {self.player_points[player.name]} points!")
                    return

            self.session_count += 1

        print("\n=== Game Over ===")
        print("Final Scores:")
        for player_name, points in self.player_points.items():
            print(f"- {player_name}: {points} points")

        winner = max(self.player_points, key=self.player_points.get)
        print(f"\nCongratulations, {winner}! You have won the game with {self.player_points[winner]} points!")

if __name__ == "__main__":
    engine = GameEngine()
    engine.continuous_game_loop()