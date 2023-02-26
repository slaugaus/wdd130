import pickle


class Stats():
    """Tracks statistics."""

    def __init__(self, settings):
        """Initialize stats and load the high score."""
        try:
            self.file = open("../highscore.pickle", mode="r+b")
            self.high_score = pickle.load(self.file)
            self.file = open("../highscore.pickle", mode="w+b")
        except (FileNotFoundError, EOFError):
            self.file = open("../highscore.pickle", mode="w+b")
            self.high_score = 0
        self.settings = settings
        self.game_active = False
        self.done = False
        self.fps = 0
        self.reset_stats()

    def reset_stats(self):
        """Reset the stats that will change."""
        self.score = 0
        self.bullet_cooldown = 0
        self.ship_health = self.settings.ship_health
        self.ship_lives = self.settings.ship_lives
        self.ship_level = 0
        self.ship_inv = False
        self.ship_inv_timer = 1
        self.game_level = 1
        self.next_score = 0
        self.next_score_increment = 1000
        self.enemy_timer = self.settings.enemy_timer
        self.next_timer = 120

    def update_high_score(self, hud):
        """Update the high score if it's beaten."""
        if self.score > self.high_score:
            self.high_score = self.score
            hud.prep_high_score()

    def save_high_score(self, hud):
        """Save the high score to a file."""
        self.update_high_score(hud)
        pickle.dump(self.high_score, self.file)
