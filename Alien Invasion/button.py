"""A class to create a button for any application as needed"""

import pygame.font


class Button:
    """A class to build a button for the game"""

    def __init__(self, game, message):
        """Initialize button attributes"""

        # Let's initialize the screen and rect objects
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button
        self.width, self.height = 400, 150
        self.button_color = (0, 135, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # The button message needs to be prepared once
        self._prep_msg(message)

    def _prep_msg(self, message):
        """Turn message into an image and center text on the bottom"""
        self.message_image = self.font.render(message, True, self.text_color, self.button_color)
        self.message_image_rect = self.message_image.get_rect()
        self.message_image_rect.center = self.rect.center

    def draw_button(self):
        """Draw blank button and then draw the image"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.message_image, self.message_image_rect)
