# game_board.py

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class AvailabilityZone:
    """
    Represents an AWS Availability Zone within a region.
    """
    name: str
    bonus: Optional[str] = None  # Optional bonus attribute


@dataclass
class Region:
    """
    Represents an AWS Region containing multiple Availability Zones.
    """
    name: str
    azs: List[AvailabilityZone]
    special_access_required: bool = False  # Indicates if special access is needed


class GameBoard:
    """
    Represents the game board with all regions and their AZs.
    """

    def __init__(self):
        self.regions: List[Region] = self.create_regions()

    def create_regions(self) -> List[Region]:
        """
        Initializes and returns a list of regions with their AZs.
        """
        regions = [
            Region(
                name="US East (N. Virginia)",
                azs=[
                    AvailabilityZone(name="us-east-1a", bonus="Agility"),
                    AvailabilityZone(name="us-east-1b", bonus="Elasticity"),
                    AvailabilityZone(name="us-east-1c"),
                ]
            ),
            Region(
                name="US West (Oregon)",
                azs=[
                    AvailabilityZone(name="us-west-2a", bonus="Resilience"),
                    AvailabilityZone(name="us-west-2b"),
                    AvailabilityZone(name="us-west-2c",
                                     bonus="Fault Tolerance"),
                ]
            ),
            Region(
                name="Special Region",
                azs=[
                    AvailabilityZone(name="special-az-1",
                                     bonus="Availability"),
                ],
                special_access_required=True
            ),
            # Add more regions and AZs as needed
        ]
        return regions
