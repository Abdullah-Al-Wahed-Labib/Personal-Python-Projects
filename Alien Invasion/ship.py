"""The class to model the spaceship for the Alien Invasion game."""

import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """A class to model the spaceship of the game."""

    def __init__(self, game):
        """Initialize the ship and set its starting position."""
        super().__init__()

        # Initialize the attributes needed to display a ship
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()

        # Load settings for a ship
        self.settings = game.settings

        # Load the ship image and get its rectangle.
        self.image = pygame.image.load("images/ship.bmp")
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a float for the ship's exact horizontal position
        self.x = float(self.rect.x)

        # Movement flag for the right side movement; start with a ship that's not moving
        self.moving_right = False

        # Movement flag for the left side movement; start with a ship that's not moving
        self.moving_left = False

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Update the ship's position based on the movement flags. Stops moving when reached edge"""

        # Update the ship's x value, not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # Update the rect object from self.x
        self.rect.x = self.x

    def center_ship(self):
        """Center the ship on the screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
