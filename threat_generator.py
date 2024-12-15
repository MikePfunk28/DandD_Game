# threat_generator.py

from threat import Threat
from typing import Dict


def generate_threat_for_region(region: str) -> Threat:
    """
    Generates a threat based on the region.
    """
    region_threats = {
        "US East (N. Virginia)": Threat(
            name="DDoS Attack",
            attack_type="Network Flood",
            power=25,
            persistence=3,
            adaptability=60
        ),
        "US West (Oregon)": Threat(
            name="Data Breach",
            attack_type="Unauthorized Access",
            power=30,
            persistence=4,
            adaptability=70
        ),
        "Special Region": Threat(
            name="Advanced Threat",
            attack_type="Multi-vector Attack",
            power=35,
            persistence=5,
            adaptability=80
        ),
        # Add more regions and corresponding threats
    }
    return region_threats.get(region, Threat(
        name="Generic Threat",
        attack_type="Unknown",
        power=20,
        persistence=2,
        adaptability=50
    ))
