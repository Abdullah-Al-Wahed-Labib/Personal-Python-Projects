"""A class to model and manage the bullets shoot by the ship."""

import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """A class to manage the bullets fired from the ship."""

    def __init__(self, game):
        """Create a bullet object at the ship's current position"""

        # Initialize the super class and the attributes needed to simulate a bullet
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        # self.color = game.settings.bullet_color

        # Create a bullet rect at (0, 0) and then set current position.
        self.bullet_image = pygame.image.load("images/bullet.bmp")
        self.rect = self.bullet_image.get_rect()
        self.rect.midtop = game.ship.rect.midtop

        # Store the bullet's position as float
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet up the screen"""

        # Update the exact position of the bullet
        self.y -= self.settings.bullet_speed

        # Update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet onto the screen"""
        self.screen.blit(self.bullet_image, self.rect)
