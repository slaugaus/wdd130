import pygame
import zipfile
import io


class Sounds():
    """Handles the sound mixer."""

    def __init__(self, settings):
        """Edit mixer settings, then load all of the audio and set volumes."""
        pygame.mixer.set_num_channels(32)
        self.null = pygame.mixer.Sound("audio/null.ogg")
        if not settings.mute_sound:
            self.pew = pygame.mixer.Sound("audio/pew.ogg")
            self.boom_med = pygame.mixer.Sound("audio/boom_med.ogg")
            self.boom_small = pygame.mixer.Sound("audio/boom_small.ogg")
            self.enemy_hit = pygame.mixer.Sound("audio/enemy_hit.ogg")
            self.ship_hit = pygame.mixer.Sound("audio/ship_hit.ogg")
            self.levelup = pygame.mixer.Sound("audio/levelup.ogg")
            self.leveldown = pygame.mixer.Sound("audio/leveldown.ogg")
        else:
            self.pew = self.null
            self.boom_med = self.null
            self.boom_small = self.null
            self.enemy_hit = self.null
            self.ship_hit = self.null
            self.levelup = self.null
            self.leveldown = self.null
        if not settings.mute_music:
            pygame.mixer.music.load("audio/bgm.ogg")
            pygame.mixer.music.set_volume(0.3)
        self.pew.set_volume(0.2)
        self.boom_med.set_volume(0.3)
        self.boom_small.set_volume(0.7)
        self.enemy_hit.set_volume(0.05)
        self.ship_hit.set_volume(0.5)
        self.levelup.set_volume(0.5)


class Images():
    """Handles all of the sprites."""

    def __init__(self):
        """Load each of the sprites and sprite lists."""
        # I know these could all be done with gfxdraw,
        # but they wouldn't look as good.
        self.hitbox = pygame.image.load("images/hitbox.png")
        self.hitbox_inv = pygame.image.load("images/hitbox_inv.png")
        self.star = pygame.image.load("images/star.png")
        self.enemy_bullet = pygame.image.load("images/enemy_bullet.png")
        # Loading icon_16 screws it up for some reason.
        self.icon = pygame.image.load("images/icon/icon_16_2x.png")
        self.logo = pygame.image.load("images/logo.png")
        # Pretty dumb trick [CODERS HATE HIM]
        self.enemy = [0, 1, 2, 3, 4, 5]
        for id in self.enemy:
            self.enemy[id] = self.load_anim("enemy" + str(id + 1))
        self.ship = self.load_anim("ship")
        self.explosion = self.load_anim("explosion")
        self.explosion_large = self.load_anim("explosion_large")
        self.powerup = self.load_anim("powerup")
        self.health = self.load_anim("health")

    def load_anim(self, filepath):
        target = []
        zip = zipfile.ZipFile("anims/" + filepath + ".zip")
        list = zip.namelist()
        for filename in list:
            file = io.BytesIO(zip.read(filename))
            image = pygame.image.load(file)
            target.append(image)
        zip.close()
        return target
