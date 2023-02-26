import pygame
from entities import Ship


class Statbar():
    def __init__(self, settings, screen, color, stat, statmax, parent=None):
        """A stat bar for use in the HUD."""
        self.screen = screen
        self.settings = settings
        self.stat = stat
        self.statmax = statmax
        self.color = color
        self.parent = parent
        if self.parent is None:
            # Assumes that color is completely red, green, or blue.
            self.dark_color = self.color - pygame.Color(127, 127, 127, 0)
            self.rect = pygame.Rect(0, 0, 500, 6)
            self.top_rect = pygame.Rect(0, 0, 500, 6)
        else:
            # Be a border for the specified parent.
            self.color -= pygame.Color(0, 0, 0, 255)
            self.rect = pygame.Rect(0, 0, 504, 10)
            self.top_rect = pygame.Rect(0, 0, 504, 10)
            self.rect.center = self.parent.rect.center
        self.top_rect.center = self.rect.center

    def update(self, stat):
        """Change the top rect's width to match the given stat, then draw."""
        self.top_rect.left = self.rect.left
        self.top_rect.top = self.rect.top
        self.stat = stat
        if self.stat > self.statmax:
            self.stat = self.statmax
        if self.stat == -1:
            self.stat = self.statmax
        self.top_rect.width = (self.stat / self.statmax) * self.rect.width
        if self.parent is None:
            pygame.draw.rect(self.screen, self.dark_color, self.rect)
        if self.stat > 0 or self.stat == -1:
            pygame.draw.rect(self.screen, self.color, self.top_rect)


class HUD():
    def __init__(self, settings, screen, stats, images):
        """The HUD."""
        self.screen = screen
        self.settings = settings
        self.stats = stats
        self.images = images
        self.text_color = settings.white
        self.font = pygame.font.Font("fonts/unoestado.ttf", 32)
        self.font_small = pygame.font.Font("fonts/unoestado.ttf", 16)
        self.healthbar = Statbar(settings, screen, settings.red,
                                 stats.ship_health, settings.ship_health)
        self.invbar = Statbar(settings, screen, settings.blue,
                              stats.ship_inv_timer, settings.ship_mercy_inv,
                              self.healthbar)
        self.powerbar = Statbar(settings, screen, settings.green,
                                stats.ship_level, settings.max_ship_level)
        self.prep_statbars()
        self.prep_ship()
        self.prep_life_amount()
        self.prep_score()
        self.prep_high_score()
        self.prep_fps()

    def prep_statbars(self):
        self.healthbar.rect.x = 5
        self.healthbar.rect.y = 5
        self.invbar.rect.center = self.healthbar.rect.center
        self.powerbar.rect.x = 5
        self.powerbar.rect.y = self.healthbar.rect.bottom + 2

    def prep_ship(self):
        self.ship = Ship(self.settings, self.screen, self.stats, self.images)
        self.ship.rect.x = 5
        self.ship.rect.y = self.powerbar.rect.bottom + 2

    def prep_life_amount(self):
        lives_left = self.stats.ship_lives
        lives_str = "X " + str(lives_left)
        self.lives_image = self.font.render(lives_str, True, self.text_color)
        self.lives_rect = self.lives_image.get_rect()
        self.lives_rect.left = self.ship.rect.right + 5
        self.lives_rect.centery = self.ship.rect.centery

    def prep_score(self):
        score_str = "Score: " + "{:,}".format(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.left = 0
        self.score_rect.bottom = self.settings.screen_height

    def prep_high_score(self):
        hs_str = "High score: " + "{:,}".format(self.stats.high_score)
        self.hs_image = self.font.render(hs_str, True, self.text_color)
        self.hs_rect = self.hs_image.get_rect()
        self.hs_rect.left = 0
        self.hs_rect.bottom = self.score_rect.top

    def prep_fps(self):
        fps_str = str(int(self.stats.fps)) + " FPS"
        self.fps_image = self.font_small.render(fps_str, True, self.text_color)
        self.fps_rect = self.fps_image.get_rect()
        self.fps_rect.right = self.settings.screen_width
        self.fps_rect.bottom = self.settings.screen_height

    def update(self, stats):
        """Update and draw the HUD."""
        self.ship.animate()
        self.ship.blitme()
        self.screen.blit(self.lives_image, self.lives_rect)
        self.screen.blit(self.score_image, self.score_rect)
        if not stats.game_active:
            self.screen.blit(self.hs_image, self.hs_rect)
        if self.settings.show_fps:
            self.prep_fps()
            self.screen.blit(self.fps_image, self.fps_rect)
        self.invbar.update(stats.ship_inv_timer)
        self.healthbar.update(stats.ship_health)
        self.powerbar.update(stats.ship_level)


class SplashScreen():
    def __init__(self, settings, images, screen):
        """A logo, a "Play" button, and a thing to dim the screen."""
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.settings = settings
        self.msg = "Play"
        self.logo = images.logo
        self.logo_rect = self.logo.get_rect()
        self.button_color = settings.green
        self.text_color = settings.white
        self.font = pygame.font.Font("fonts/unoestado.ttf", 32)
        self.dimmer = pygame.Surface((settings.screen_width,
                                      settings.screen_height))
        self.dimmer.set_alpha(128)
        self.button_rect = pygame.Rect(0, 0, self.logo_rect.width, 41)
        self.prep_msg()
        self.center()

    def prep_msg(self, msg="Play"):
        self.msg = msg
        if self.settings.gamepad_connected:
            self.msg += " (press Start)"
        self.text = self.font.render(self.msg, True, self.text_color)
        self.text_rect = self.text.get_rect()
        self.text_rect.centerx = self.button_rect.centerx
        self.text_rect.centery = self.button_rect.centery - 2

    def center(self):
        self.combined_rect = pygame.Rect(0, 0, self.logo_rect.width,
                                         self.logo_rect.height +
                                         self.button_rect.height)
        self.combined_rect.center = self.screen_rect.center
        self.logo_rect.top = self.combined_rect.top
        self.logo_rect.left = self.combined_rect.left
        self.button_rect.bottom = self.combined_rect.bottom
        self.button_rect.left = self.combined_rect.left
        self.text_rect.centerx = self.button_rect.centerx
        self.text_rect.centery = self.button_rect.centery - 2

    def draw(self):
        self.screen.blit(self.dimmer, (0, 0))
        self.screen.blit(self.logo, self.logo_rect)
        pygame.draw.rect(self.screen, self.button_color, self.button_rect)
        self.screen.blit(self.text, self.text_rect)
