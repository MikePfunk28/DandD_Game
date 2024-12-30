# player.py

import random
from typing import Optional
from game_board import GameBoard, Region, AvailabilityZone


class Player:
    """
    Represents a player in the game.
    """

    def __init__(self, name: str, game_board: GameBoard):
        self.name = name
        self.game_board = game_board
        self.current_position: int = 0  # Index in the game board's regions list
        self.home_region: Optional[Region] = None
        self.home_az: Optional[AvailabilityZone] = None

    def set_home_region(self):
        """
        Sets the player's home region and AZ at the start of the game.
        """
        self.home_region = self.game_board.regions[0]  # For example, first region as home
        self.home_az = self.home_region.azs[0]        # First AZ in home region
        print(f"{self.name}'s home region is {
              self.home_region.name} - {self.home_az.name}.")

    def roll_dice(self) -> int:
        """
        Simulates rolling a six-sided die to determine movement steps.
        """
        return random.randint(1, 6)

    def draw_card(self) -> int:
        """
        Simulates drawing a card that determines movement steps (1-6).
        """
        return random.randint(1, 6)  # Replace with card logic if needed

    def move(self, steps: int):
        total_regions = len(self.game_board.regions)
        self.current_position = (self.current_position + steps) % total_regions
        landed_region = self.game_board.regions[self.current_position]
        # Randomly select an AZ within the region
        landed_az = random.choice(landed_region.azs)
        print(f"{self.name} landed on {
              landed_region.name} - {landed_az.name}.")
        return landed_region, landed_az


myplayer = Player("Mike", GameBoard())
myplayer.set_home_region()
steps = myplayer.roll_dice()
landed_region, landed_az = myplayer.move(steps)
print(f"{myplayer.name} rolled {steps} and moved to {
      landed_region.name} - {landed_az.name}.")
