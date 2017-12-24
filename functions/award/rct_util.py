"""
Rollercoaster Tycoon utility functions
"""
import random

AWARDS = [
    'Best Value Park Award',
    'Tidiest Park Award',
    'Most Beautiful Park Award',
    'Safest Park Award',
    'Park With The Best Roller Coasters Award',
    'Best Park Food Award',
    'Best Bathroom Facilities Award',
    'Best Staff Award',
    'Park With The Best Water Rides Award',
    'Best Gentle Rides Award',
    'Best Custom-Designed Rides Award',
    'Most Dazzling Ride Color Schemes Award',
    'Cleanest Footpaths in the Country Award',
    'Worst Value Park Award',
    'Untidiest Park Award',
    'Most Disappointing Park Award',
    'Worst Park Food Award',
    'Worst Scenery Award',
    'Most Confusing Park Layout Award',
]


def random_award():
    return random.choice(AWARDS)
