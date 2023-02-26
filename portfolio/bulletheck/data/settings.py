import pickle
import pygame
import sys


class Settings():
    """Loads and stores settings for Bullet Heck. Also a bunch of constants."""

    def __init__(self):
        """Load settings.pickle and convert the list to variables."""
        # try:
        #     file = open("../settings.pickle", mode="r+b")
        #     vars = pickle.load(file)
        #     [self.gamepad_connected, self.screen_res, self.gamepad_id,
        #      self.deadzone, self.axis_x, self.axis_y, self.hat_id, self.but_A,
        #      self.but_X, self.but_Y, self.but_S, self.show_fps, skip_launcher,
        #      self.autofire, self.mute_music, self.mute_sound] = vars
        # except (FileNotFoundError, EOFError, ValueError):
        #     print("ERROR: Couldn't load from settings.pickle!\n"
        #           "Did you run the launcher?")
        #     input("Press any key to quit...")
        #     sys.exit()

        # Screw that, we're hardcoding these.
        self.gamepad_connected = False
        self.screen_res = "1366 x 768"
        self.gamepad_id = 0
        self.deadzone = 0.2
        self.axis_x = 0
        self.axis_y = 1
        self.hat_id = 0
        self.but_A = 0
        self.but_X = 2
        self.but_Y = 2
        self.but_S = 7
        self.show_fps = True
        skip_launcher = True
        self.autofire = False
        self.mute_music = False
        self.mute_sound = False
        # Split the screen resolution into useful values
        reslist = self.screen_res.split()
        self.screen_width = int(reslist[0])
        self.screen_height = int(reslist[2])
        # Colors
        self.white = pygame.Color(255, 255, 255, 255)
        self.black = pygame.Color(0, 0, 0, 255)
        self.red = pygame.Color(255, 0, 0, 255)
        self.green = pygame.Color(0, 255, 0, 255)
        self.blue = pygame.Color(0, 0, 255, 255)
        # Performance
        self.star_limit = 100
        self.fps_limit = 60
        # Ship
        self.ship_speed = 10  # pixels/frame
        self.ship_health = 3
        self.ship_lives = 3
        self.diag_factor = ((2 ** 0.5) / 2)  # (root2)/2
        self.star_speed = 5
        self.max_ship_level = 8
        self.ship_mercy_inv = 60  # frames
        # Bullets
        self.bullet_limit = 100
        self.bullet_cooldown = 5  # frames
        # Enemies
        self.enemy_speed = [5, 4, 5, 3, 3, 3]
        self.enemy_health = [4, 9, 3, 4, 4, 4]
        self.enemy_fire_cooldown = [-1, -1, 90, 90, 90, 90]
        self.enemy_points = [50, 100, 25, 75, 75, 75]
        self.enemy_timer = 150  # 2.5 seconds before first enemy
        self.enemy_timer_min = 20
        self.pickup_chance = 20  # percent
