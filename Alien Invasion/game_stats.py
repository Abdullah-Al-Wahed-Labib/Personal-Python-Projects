"""A module to store the statistics of the game"""

import json
from pathlib import Path


class GameStats:
    """Track statistics for the game"""

    def __init__(self, game):
        """Initialize statistics"""
        self.level = None
        self.score = None
        self.ships_left = None
        self.settings = game.settings
        self.path = game.path
        self.reset_stats()

        # High score should never be reset
        if self.path.exists():
            high_score_data = self.path.read_text()
            self.high_score = json.loads(high_score_data)
        else:
            self.high_score = 0

    def reset_stats(self):
        """Initialize statistics that can change during the game runtime"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
