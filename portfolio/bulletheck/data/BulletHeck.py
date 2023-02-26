import pygame
import sys
from pygame.sprite import Group
from pygame.joystick import Joystick
from settings import Settings
import game_functions as gf
from entities import Ship
from stats import Stats
from preloader import Sounds, Images
from hud import HUD, SplashScreen


def run_game():
    # Initialize Pygame
    pygame.mixer.pre_init(frequency=44100)
    pygame.init()
    # Initialize settings, preload assets, and create a clock
    settings = Settings()
    sounds = Sounds(settings)
    images = Images()
    clock = pygame.time.Clock()
    # Set up the window
    pygame.display.set_icon(images.icon)
    screen = pygame.display.set_mode((settings.screen_width,
                                      settings.screen_height))
    pygame.display.set_caption("Bullet Heck!")
    # Try to create a joystick object
    try:
        gamepad = Joystick(settings.gamepad_id)
        gamepad.init()
        settings.gamepad_connected = True
    except pygame.error:
        gamepad = None
        settings.gamepad_connected = False
    # Initialize the stats, HUD, and splash screen
    stats = Stats(settings)
    hud = HUD(settings, screen, stats, images)
    splash = SplashScreen(settings, images, screen)
    # Create the ship and groups for everything else
    ship = Ship(settings, screen, stats, images)
    stars = Group()
    bullets = Group()
    enemies = Group()
    enemy_bullets = Group()
    explosions = Group()
    pickups = Group()
    if not settings.mute_music:
        pygame.mixer.music.play(loops=-1)
    # Pause the music by default
    pygame.mixer.music.pause()
    # Main loop
    while stats.done is False:
        gf.check_events(settings, screen, ship, gamepad, bullets, stats,
                        sounds, enemies, images, enemy_bullets, splash, hud)
        gf.update_stars(settings, screen, stars, images)
        gf.manage_game_level(settings, stats)
        if stats.game_active:
            ship.update(settings, images)
            gf.spawn_enemies(settings, screen, enemies, images, id, stats)
            gf.update_bullets(settings, screen, ship, bullets, enemies, sounds,
                              enemy_bullets, images, stats, hud, explosions,
                              pickups, splash)
            gf.update_enemy_stuff(settings, screen, ship, enemies, sounds,
                                  stats, explosions, images, pickups, hud,
                                  bullets, enemy_bullets, splash)
        # Update the explosions even if the game is paused.
        gf.update_explosions(explosions)
        gf.update_screen(settings, screen, stars, ship, bullets, enemies,
                         explosions, pickups, hud, stats, enemy_bullets,
                         splash)
        clock.tick(settings.fps_limit)
        if settings.show_fps:
            stats.fps = clock.get_fps()


run_game()
# Stop Pygame (necessary if ran from IDLE)
pygame.quit()
# Stop the process (necessary if launcher was skipped)
sys.exit()
