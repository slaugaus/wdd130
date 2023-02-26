import pygame
import random
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, settings, screen, stats, images):
        """Initialize the ship and set its starting position."""
        # Call the init function of pygame.sprite.Sprite
        super().__init__()
        self.screen = screen
        self.settings = settings
        self.stats = stats
        # Load the animation frames and get the rect of frame 1.
        self.index = 0
        self.animdir = 1
        self.respawn_countdown = 0
        self.images = images.ship
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.hitbox = images.hitbox
        self.hbrect = self.hitbox.get_rect()
        self.speed = settings.ship_speed
        # Place the ship in the vertical middle with some padding.
        self.rect.centery = self.screen_rect.centery
        self.rect.right = self.screen_rect.left
        self.hbrect.center = self.rect.center
        self.ready = False
        # Store the ship's center as decimals.
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)
        # Flag for being in Dodge Mode
        self.dodge_mode = False
        # Flags for digital movement
        self.moving_right = False
        self.moving_left = False
        self.moving_down = False
        self.moving_up = False
        # Flags for analog movement
        self.an_up, self.an_down = 0, 0
        self.an_right, self.an_left = 0, 0
        # Collision info
        self.radius = 3.5

    def reset_pos(self):
        """Reset the ship's position."""
        self.ready = False
        self.respawn_countdown = 59
        self.stats.ship_inv = True
        self.stats.ship_inv_timer = -1
        self.centery = self.screen_rect.centery
        # same as setting self.rect.right to self.screen_rect.left
        # (not the above because update() doesn't expect it)
        self.centerx = self.screen_rect.left - (self.rect.right - self.centerx)

    def update(self, settings, images):
        """Update the ship's position and various timers."""
        if not self.ready and self.respawn_countdown == 0:
            if self.centerx < settings.screen_width / 10:
                self.centerx += settings.ship_speed
            else:
                self.ready = True
                self.stats.ship_health = settings.ship_health
                self.stats.ship_inv_timer = settings.ship_mercy_inv
        self.animate()
        if self.dodge_mode:
            self.speed = settings.ship_speed * 1.5
        else:
            self.speed = settings.ship_speed
        if settings.gamepad_connected:
            self.move_analog(settings)
        self.move_digital(settings, images)
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery
        self.hbrect.center = self.rect.center
        if self.ready:
            self.stay_on_screen()
        self.rect.center = self.hbrect.center
        if self.respawn_countdown is not 0:
            self.respawn_countdown -= 1
        if self.stats.ship_inv_timer > 0:
            self.stats.ship_inv = True
            self.stats.ship_inv_timer -= 1
        elif self.stats.ship_inv_timer == 0:
            self.stats.ship_inv = False
        if self.stats.ship_inv:
            self.hitbox = images.hitbox_inv
        else:
            self.hitbox = images.hitbox

    def move_digital(self, settings, images):
        """Move the ship if the flags say to."""
        # The ship should be moving the same speed when moving diagonally.
        if (self.moving_up and self.moving_left or
                self.moving_up and self.moving_right or
                self.moving_down and self.moving_left or
                self.moving_down and self.moving_right):
            self.speed *= settings.diag_factor
        # If it's been animated in, allow movement.
        if self.ready:
            if self.moving_right and self.hbrect.right < settings.screen_width:
                self.centerx += self.speed
            if self.moving_left and self.hbrect.left > 0:
                self.centerx -= self.speed
            if self.moving_down and (self.hbrect.bottom <
                                     settings.screen_height):
                self.centery += self.speed
                self.animdir = -1
            if self.moving_up and self.hbrect.top > 0:
                self.centery -= self.speed
                self.animdir = 1

    def move_analog(self, settings):
        """Move the ship based on analog stick movement."""
        if self.ready:
            if self.an_right > 0 and self.hbrect.right < settings.screen_width:
                self.centerx += self.an_right * self.speed
                self.cancel_digital()
            if self.an_left < 0 and self.hbrect.left > 0:
                self.centerx += self.an_left * self.speed
                self.cancel_digital()
            if self.an_up < 0 and self.hbrect.top > 0:
                self.centery += self.an_up * self.speed
                self.animdir = 1
                self.cancel_digital()
            if self.an_down > 0 and (self.hbrect.bottom <
                                     settings.screen_height):
                self.centery += self.an_down * self.speed
                self.animdir = -1
                self.cancel_digital()

    def cancel_digital(self):
        """Prevent "boosting" with multiple input methods."""
        self.moving_right = False
        self.moving_left = False
        self.moving_down = False
        self.moving_up = False

    def stay_on_screen(self):
        """Make sure that the ship's hitbox is always on the screen."""
        if self.hbrect.right > self.settings.screen_width:
            self.hbrect.right = self.settings.screen_width
        if self.hbrect.left < 0:
            self.hbrect.left = 0
        if self.hbrect.bottom > self.settings.screen_height:
            self.hbrect.bottom = self.settings.screen_height
        if self.hbrect.top < 0:
            self.hbrect.top = 0

    def animate(self):
        """Animate the ship."""
        self.index += self.animdir
        # <> are there in case the index ever goes past 30 or 0.
        if self.animdir == 1 and self.index >= len(self.images):
            self.index = 0
        if self.animdir == -1 and self.index <= 0:
            self.index = len(self.images) - 1
        self.image = self.images[self.index]

    def blitme(self):
        """Draw the ship and its hitbox."""
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.hitbox, self.hbrect)


class Enemy(Sprite):
    """One enemy."""

    def __init__(self, settings, screen, images, id):
        """Figure out what enemy this is, then initialize it.
           IDs: 1 - Small tri-torus
                2 - Big tri-torus
                3 - Evil ship
                4 - Spinning theta
                5 - Spinning plus
                6 - Spinning star"""
        super().__init__()
        self.settings = settings
        self.screen = screen
        self.id = id
        self.health = settings.enemy_health[self.id-1]
        self.index = 0
        self.fire_cooldown = (settings.enemy_fire_cooldown[self.id-1] +
                              random.randint(-10, 10))
        self.images = images.enemy[self.id-1]
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.point_value = settings.enemy_points[self.id-1]
        # Collision info
        if self.id == 2:
            self.radius = 40
        elif self.id is not 3:
            self.radius = 20

    def animate(self):
        self.index += 1
        if self.index == len(self.images):
            self.index = 0

    def update(self):
        self.animate()
        self.image = self.images[self.index]
        self.rect.x -= self.settings.enemy_speed[self.id-1]

    def blitme(self):
        """Draw the enemy."""
        self.screen.blit(self.image, self.rect)


class EnemyBullet(Sprite):
    """Manages enemy bullets."""

    def __init__(self, settings, screen, images, start, angle=0,
                 offset=0, speed=9):
        """Create an enemy bullet at the specified location (start).
           The offset is relative to the angle."""
        super().__init__()
        self.screen = screen
        self.start = start
        self.speed = speed
        self.angle = angle
        self.offset = pygame.math.Vector2(offset, 0)
        self.offset.rotate_ip(self.angle)
        [self.x_offset, self.y_offset] = self.offset
        self.vector = pygame.math.Vector2(0, 0)
        self.vector.from_polar((self.speed, self.angle))
        [self.xspeed, self.yspeed] = self.vector
        self.image = images.enemy_bullet
        self.rect = self.image.get_rect()
        self.rect.center = self.start
        self.rect.centerx += self.x_offset
        self.rect.centery -= self.y_offset
        self.radius = 5

    def update(self):
        self.rect.centerx += self.xspeed
        self.rect.centery -= self.yspeed  # since pygame y is flipped

    def blitme(self):
        self.screen.blit(self.image, self.rect)


class Bullet(Sprite):
    """Manages the ship's bullets."""

    def __init__(self, settings, screen, ship, y_offset=0, height=2, width=15,
                 damage=1, speed=20):
        """Make a bullet at the ship's position."""
        super().__init__()
        self.screen = screen
        self.y_offset = y_offset
        self.speed = speed
        self.damage = damage
        self.color = settings.red
        # Create a bullet rect at (0, 0) and set its real position.
        self.rect = pygame.Rect(0, 0, width, height)
        # If told to, offset the bullet from the usual value.
        self.rect.centery = ship.rect.centery + self.y_offset
        self.rect.right = ship.rect.right

    def update(self):
        """Move the bullet right."""
        self.rect.x += self.speed

    def draw_bullet(self):
        """Draw the bullet."""
        pygame.draw.rect(self.screen, self.color, self.rect)


class Star(Sprite):
    """Manages the starry background."""

    def __init__(self, settings, screen, images):
        """Put a star somewhere on the screen."""
        super().__init__()
        self.screen = screen
        self.image = images.star
        self.rect = self.image.get_rect()
        self.rect.right = settings.screen_width
        self.rect.bottom = random.randint(0, settings.screen_height)
        self.speed_factor = settings.star_speed
        self.x = float(self.rect.x)

    def update(self):
        """Move the star left."""
        self.x -= self.speed_factor
        self.speed_factor += 0.5
        self.rect.x = self.x

    def blitme(self):
        """Draw the star."""
        self.screen.blit(self.image, self.rect)


class Explosion(Sprite):
    """Boom!"""

    def __init__(self, settings, screen, images, pos, size="s"):
        """Place the explosion at the given coordinates."""
        super().__init__()
        self.settings = settings
        self.screen = screen
        self.index = 0
        if size == "s":
            self.images = images.explosion
        elif size == "l":
            self.images = images.explosion_large
        self.countdown = len(self.images) - 1
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self):
        self.index += 1
        self.countdown -= 1
        self.image = self.images[self.index]

    def blitme(self):
        self.screen.blit(self.image, self.rect)


class Pickup(Sprite):
    """A pickup for the ship to collect.
       Types: powerup (p), health (h)"""

    def __init__(self, images, screen, pos, type):
        super().__init__()
        self.screen = screen
        self.index = 0
        self.type = type
        if self.type == "p":
            self.images = images.powerup
        elif self.type == "h":
            self.images = images.health
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.center = self.rect.center
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.speed = random.randint(2, 5)
        self.angle = random.randint(0, 359)
        self.vector = pygame.math.Vector2(0, 0)
        self.vector.from_polar((self.speed, self.angle))
        [self.xspeed, self.yspeed] = self.vector

    def update(self):
        self.index += 1
        if self.index == len(self.images):
            self.index = 0
        self.image = self.images[self.index]
        self.x += self.xspeed
        self.y -= self.yspeed
        self.rect.centerx = self.x
        self.rect.centery = self.y

    def blitme(self):
        self.screen.blit(self.image, self.rect)
