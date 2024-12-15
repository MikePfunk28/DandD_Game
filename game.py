# game.py

# Import necessary modules and classes
from game_board import GameBoard
from player import Player
from vpc_defender import VPCDefender
from threat_generator import generate_threat_for_region
from security_battle import SecurityBattle
from character_stats import CharacterStats
from opening_scene import start_interview
from dataclasses import dataclass
import time  # For tracking time if needed

# Function to run a single game session


def run_game(player: Player, defender: VPCDefender) -> int:
    """
    Runs a single game session and returns the points earned.
    """
    # Initialize game board
    game_board = player.game_board

    # Start of the game session
    session_points = 0  # Points earned in this session
    game_over = False

    while not game_over:
        print("\n=== New Turn ===")

        # Movement phase
        move_choice = input(
            "Do you want to 'roll' the die or 'draw' a card to move? (roll/draw): ").strip().lower()
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

        # Move the player and identify where they landed
        landed_region, landed_az = player.move(steps)

        # Apply regional charges if not in home region
        if landed_region != player.home_region:
            regional_charge = 10  # Example value for charge
            if defender.preparation_points >= regional_charge:
                defender.preparation_points -= regional_charge
                print(f"Operating in {landed_region.name} incurs a charge of {
                      regional_charge} preparation points.")
            else:
                print("Insufficient preparation points to cover regional charges.")

        # Setup phase
        print("\n--- Setup Phase ---")
        print(f"Preparation Points: {defender.preparation_points}")
        print("Available Defensive Measures:")
        for key, measure in defender.defensive_measures.items():
            print(f"- {key}: {measure.description} (Cost: {
                  measure.cost}, Effectiveness: {measure.effectiveness})")
        print("Available Offensive Measures:")
        for key, measure in defender.offensive_measures.items():
            print(f"- {key}: {measure.description} (Cost: {
                  measure.cost}, Effectiveness: {measure.effectiveness})")

        while True:
            setup_action = input(
                "Enter 'measure' to implement a security measure or 'done' to finish setup: ").strip().lower()
            if setup_action == 'measure':
                measure_name = input(
                    "Enter the measure key to implement: ").strip().lower()
                result = defender.implement_security_measure(measure_name)
                print(result)
            elif setup_action == 'done':
                if len(defender.active_measures) == 0:
                    print(
                        "You must implement at least one security measure before proceeding.")
                else:
                    print("Setup phase completed.")
                    break
            else:
                print("Invalid action. Please enter 'measure' or 'done'.")

        # Threat encounter
        print("\n--- Threat Encounter ---")
        threat = generate_threat_for_region(landed_region.name)

        # Generate enemy stats for the threat
        print(f"Threat Details: {threat.name}, Power: {threat.power}, Persistence: {
              threat.persistence}, Adaptability: {threat.adaptability}")

        # Initiate security battle with the defender and threat
        battle = SecurityBattle(defender, threat)
        battle.start_battle()

        # After battle checks
        if not defender.is_alive():
            print("Your defender has been compromised! Game Over.")
            game_over = True
        elif battle.threat_defeated():
            print(f"Successfully defeated the threat: {threat.name}!")
            defender.level_up()
            session_points += 100  # Award points for defeating the threat
        else:
            print("The threat remains active.")

        # Player decision on whether to continue
        continue_choice = input(
            "Do you want to continue to the next turn? (yes/no): ").strip().lower()
        if continue_choice != 'yes':
            print("Ending the current game session.")
            game_over = True

    return session_points  # Return the points earned in this session


# New function: continuous_game_loop
def continuous_game_loop(max_sessions: int = 5, winning_score: int = 500):
    """
    Continuously runs multiple game sessions until a player reaches the winning score or
    the maximum number of sessions is reached.

    Args:
        max_sessions (int): Maximum number of game sessions to play.
        winning_score (int): The score required for a player to win.
    """
    print("=== Welcome to the Cloud Security Battle ===")
    number_of_players = int(input("Enter the number of players: ").strip())

    # Initialize players and defenders
    players = []
    defenders = []
    for i in range(number_of_players):
        player_name = input(f"Enter the name for Player {i + 1}: ").strip()
        game_board = GameBoard()
        player = Player(name=player_name, game_board=game_board)
        player.set_home_region()
        players.append(player)

        # Initialize defender stats
        stats = CharacterStats()
        defender = VPCDefender(name=player.name + "'s Defender", stats=stats)
        player.defender = defender

    # Game loop variables
    # Track player points
    player_points = {player.name: 0 for player in players}
    session_count = 1

    # Run the game until a player wins or max sessions reached
    while session_count <= max_sessions:
        print(f"\n=== Game Session {session_count} ===")
        for idx, player in enumerate(players):
            print(f"\n--- {player.name}'s Turn ---")
            points_earned = run_game(player, defenders[idx])
            player_points[player.name] += points_earned
            print(f"{player.name} earned {points_earned} points this session.")
            print(f"Total Points: {player_points[player.name]}")

            # Reset defender's health and preparation points for the next session
            defenders[idx].current_health = defenders[idx].max_health
            defenders[idx].preparation_points = 100
            defenders[idx].active_measures.clear()

            # Check for winning condition
            if player_points[player.name] >= winning_score:
                print(f"\nCongratulations, {player.name}! You have won the game with {
                      player_points[player.name]} points!")
                return  # End the game once a player wins

        session_count += 1

    # If no player reached the winning score after max sessions, announce the highest scorer
    print("\n=== Game Over ===")
    print("Final Scores:")
    for player_name, points in player_points.items():
        print(f"- {player_name}: {points} points")

    winner = max(player_points, key=player_points.get)
    print(f"\nCongratulations, {winner}! You have won the game with {
          player_points[winner]} points!")


# Run the continuous game loop
if __name__ == "__main__":
    continuous_game_loop()
