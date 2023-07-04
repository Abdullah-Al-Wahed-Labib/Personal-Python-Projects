"""A class to model and simulate the aliens fleet"""

import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to model aliens and provide functionality to control it"""

    def __init__(self, game):
        """Initialize the alien and set its starting position"""
        super().__init__()

        # Initialize the screen for the aliens
        self.screen = game.screen

        # Load the alien image and set its rect attribute
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()

        # Start each alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position
        self.x = float(self.rect.x)

        # Initialize settings for aliens
        self.settings = game.settings

    def update(self):
        """Move the alien to the right or left"""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

    def check_edges(self):
        """Return true if alien is at edge of the screen"""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)
