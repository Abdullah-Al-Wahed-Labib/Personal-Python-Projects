"""The main module to manage Alien Invasion game. Run it to start the game."""

# built-in modules
import sys
import json
from time import sleep
from pathlib import Path

# third-party modules, available via pip
import pygame

# private modules, created by the developer
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    """Overall class to manage game assets and behaviours."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()

        # Initialize a storage path to save high-score
        self.path = Path("alien_invasion_data.json")

        # Initialize the settings and set up display, clock and title
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics and create a scoreboard
        self.stats = GameStats(self)
        self.scoreboard = Scoreboard(self)

        # Set the background color.
        self.bg_color = (230, 230, 230)
        self.ship = Ship(self)

        # Define a group to contain the bullets
        self.bullets = pygame.sprite.Group()

        # Define another group to contain all the aliens available
        self.aliens = pygame.sprite.Group()

        # Populate the aliens' group
        self._create_fleet()

        # Define a mixer to produce sound output and initialize it
        self.mixer = pygame.mixer
        self.mixer.init()

        # Set a flag to see if the game is running or not, start in inactive state
        self.game_active = False

        # Make a Play button
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._store_high_score()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                self._check_play_button(mouse_position)

    def _store_high_score(self):
        """Save the high score into storage"""
        high_score = self.stats.high_score
        json_data = json.dumps(high_score)
        self.path.write_text(json_data)

    def _update_bullets(self):
        """Update the position of bullets and get rid of old bullets"""

        # Update bullet positions
        self.bullets.update()

        # get rid of old bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        """Respond to bullet-alien collisions"""
        # Check for any bullets that have hit aliens.
        # If so, remove the bullet and the alien
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.scoreboard.prepare_score()
            self.scoreboard.check_high_score()

        for _ in collisions.keys():
            # Code to produce blast sound
            self.mixer.music.load("sounds/blast.mp3")
            self.mixer.music.set_volume(0.5)
            self.mixer.music.play()

        # Let's check if the fleet is empty, then create a new fleet
        if not self.aliens:
            # Destroy Existing bullets ad create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase the nuber of level
            self.stats.level += 1
            self.scoreboard.prepare_level()

    def _create_fleet(self):
        """Create the fleet of aliens"""

        # Create an alien and keep adding aliens until there is no room left.
        # Spacing between aliens is one alien width and one alien height
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height

        # Now create a fleet of aliens at the top of the screen
        # Let's use an inner loop to fill all the alies in horizontal space
        # and an outer loop to fill all the vertical available space
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 4 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            # Finished filling up a row; reset X value and increment Y value
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the given position"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _update_screen(self):
        """Update images in the screen and flip to the new screen."""

        # Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)

        # Draw the bullets that's already fired
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Make the ship visible
        self.ship.blitme()

        # Draw the group of aliens t make themselves visible to the screen
        self.aliens.draw(self.screen)

        # Draw the score information
        self.scoreboard.show_score()

        # Draw the play button if the game is in the inactive state only
        if not self.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible.
        pygame.display.flip()

    def _update_aliens(self):
        """Check if the fleet is at an edge, then update positions"""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()

    def _check_keydown_events(self, event):
        """This method responds to keypresses. Quits the game using the specific key"""
        if event.key == pygame.K_RIGHT:
            # Move the ship to the right until key is released
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            # Move the ship to the left until key is released
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            # Fire a bullet
            self._fire_bullet()

        # Make sure the game quits when pressed "Q"
        if event.key == pygame.K_q:
            self._store_high_score()
            sys.exit()

    def _check_keyup_events(self, event):
        """This method responds to key release events"""
        if event.key == pygame.K_RIGHT:
            # Stop moving the ship to the right
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            # Stop moving the ship to the left
            self.ship.moving_left = False

    def _check_play_button(self, mouse_position):
        """Start a new game when the player clicks Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_position)
        if button_clicked and not self.game_active:
            # Reset the game settings
            self.settings.initialize_dynamic_settings()

            # Reset the game statistics
            self.stats.reset_stats()
            self.scoreboard.prepare_score()
            self.scoreboard.prepare_level()
            self.scoreboard.prepare_ships()
            self.game_active = True

            # Remove any remaining bullets and aliens
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet of alien and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Hide mouse cursor
            pygame.mouse.set_visible(False)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group. Don't create one if limit exceed"""
        if len(self.bullets) < self.settings.bullets_allowed:
            # Code to produce firing sound
            self.mixer.music.load("sounds/fire.mp3")
            self.mixer.music.set_volume(0.5)
            self.mixer.music.play()
            # Code to create a bullet
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""

        if self.stats.ships_left > 0:
            # Decrement the number of ships left
            self.stats.ships_left -= 1
            self.scoreboard.prepare_ships()

            # Remove all bullets and aliens
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Play a warning sound to make the user aware
            self.mixer.music.load("sounds/warning.mp3")
            self.mixer.music.set_volume(0.5)
            self.mixer.music.play()

            # Pause the game for a moment
            sleep(2)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat it as the ship got hit
                self._ship_hit()
                break


if __name__ == "__main__":
    # Make a game instance, and run the game. Only if it is run from the CMD
    game = AlienInvasion()
    game.run_game()
