import pygame as pg
from ball import Ball
from score_keeper import Score_Keeper

class Controller(object):

    BACKGROUND_COLOR = (0, 0, 0)
    CAPTION = "PING"
    ACCEPTABLE_KEYS = [pg.K_w, pg.K_a, pg.K_s, pg.K_d, pg.K_i, pg.K_j, pg.K_k, pg.K_l]

    def __init__(self, dimensions=[1000, 600]):
        self.clock = pg.time.Clock()
        self.game_objects = []
        self.window = None
        self.dimensions = dimensions
        self.score_keeper = Score_Keeper()
        self.quit_game_flag = False

    def add_game_objects(self, *objects: pg.sprite.Sprite):
        self.game_objects.extend(objects)
        for o in objects:
            if type(o) is Ball:
                self.score_keeper.ball = o

    def _should_game_continue(self):
        return not self.score_keeper.is_max_score_reached() and not self.quit_game_flag

    @staticmethod
    def _check_for_window_close(event):
        return event.type == pg.QUIT

    def _do_updates(self):
        [o.update() for o in self.game_objects]
        if self.score_keeper.check_for_goal():
            [o.reset_to_starting_position() for o in self.game_objects]

    def _do_draws(self):
        self.score_keeper.draw(self.window)
        [self.window.blit(o.image, (o.rect.x, o.rect.y)) for o in self.game_objects]
        pg.display.update()

    def _create_window(self):
        self.window = pg.display.set_mode((self.dimensions[0], self.dimensions[1]))
        pg.display.set_caption(self.CAPTION)
        pg.display.update()

    def _handle_key_input(self, keys):
        pressed_keys = [k for k in self.ACCEPTABLE_KEYS if keys[k]]
        [o.handle_keyboard_input(pressed_keys) for o in self.game_objects]

    def _check_for_collisions(self):
        balls = [o for o in self.game_objects if type(o) is Ball]
        not_balls = [o for o in self.game_objects if type(o) is not Ball]

        [ball.check_for_bounces(not_balls) for ball in balls]

    def start_game(self):
        pg.init()

        self._create_window()

        while self._should_game_continue():

            for event in pg.event.get():
                if self._check_for_window_close(event):
                    self.quit_game_flag = True
                    break

            self._handle_key_input(pg.key.get_pressed())
            self._check_for_collisions()
            self.window.fill(self.BACKGROUND_COLOR)

            self._do_updates()
            self._do_draws()
            self.clock.tick(60)

        pg.quit()

