"""A module to provide access to the settings of Alien Invasion game."""


class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""

        # Setting dynamic values to None
        self.alien_points = None
        self.ship_speed = None
        self.bullet_speed = None
        self.alien_speed = None
        self.fleet_direction = None
        self.fleet_drop_speed = None

        # Screen Settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Settings for ship
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 15
        self.bullet_height = 20
        self.bullet_color = (0, 0, 0)
        self.bullets_allowed = 6

        # How quickly the game speeds up
        self.speedup_rate = 1.3

        # How quickly the alien point values increase
        self.score_scale = 2

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize the settings that change throughout the game"""
        self.ship_speed = 12
        self.bullet_speed = 6
        self.alien_speed = 5
        self.fleet_drop_speed = 15

        # fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

        # Scoring settings
        self.alien_points = 50

    def increase_speed(self):
        """Increase dynamic settings"""
        self.ship_speed *= self.speedup_rate
        self.bullet_speed *= self.speedup_rate
        self.alien_speed *= self.speedup_rate

        # Increase the alien points for upper levels
        self.alien_points = int(self.alien_points * self.score_scale)
