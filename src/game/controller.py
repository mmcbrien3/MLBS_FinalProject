import pygame as pg
import numpy as np
from src.game.ball import Ball
from src.game.paddle import Paddle
import src.ml.match
import src.game.score_keeper

class Controller(object):

    BACKGROUND_COLOR = (0, 0, 0)
    CAPTION = "PING"
    ACCEPTABLE_KEYS = [pg.K_w, pg.K_a, pg.K_s, pg.K_d, pg.K_i, pg.K_j, pg.K_k, pg.K_l]

    def __init__(self, dimensions=[1000, 600]):
        self.game_objects = []
        self.num_paddles = 0
        self.window = None
        self.dimensions = dimensions
        self.score_keeper = src.game.score_keeper.ScoreKeeper()
        self.quit_game_flag = False
        self.max_frames = None
        self.max_score = None
        self.frame_rate = 60
        self.frames_expired = 0
        self.left_computer_player = None
        self.right_computer_player = None
        self.do_not_draw = False

    def add_game_objects(self, *objects: pg.sprite.Sprite):
        self.game_objects.extend(objects)
        for o in objects:
            if type(o) is Ball:
                self.score_keeper.ball = o
            if type(o) is Paddle:
                self.num_paddles += 1

    def set_max_score(self, score):
        self.score_keeper.max_score = score

    def _should_game_continue(self):
        return not self.score_keeper.is_max_score_reached() and \
               not self.quit_game_flag and \
               (self.max_frames is None or self.max_frames > self.frames_expired)


    @staticmethod
    def _check_for_window_close(event):
        return event.type == pg.QUIT

    def _do_updates(self):
        balls = [o for o in self.game_objects if type(o) is Ball]
        cur_ball_pos = balls[0].rect.x

        [o.update() for o in self.game_objects]
        if self.score_keeper.check_for_goal(self.num_paddles):

            if self.score_keeper.match_type != src.ml.match.Match.PASSING and \
                    self.score_keeper.match_type != src.ml.match.Match.SOLO_PRACTICE:
                [o.reset_to_starting_position() for o in self.game_objects]
            else:
                self.score_keeper.scores = [0, 0]

        for o in balls:
            if o.rect.x > 500 and cur_ball_pos < 500:
                self.score_keeper.passes[0] += 1
                print(self.score_keeper.passes)
            if o.rect.x < 500 and cur_ball_pos > 500:
                self.score_keeper.passes[1] += 1
                print(self.score_keeper.passes)

    def _do_draws(self):
        self.window.fill(self.BACKGROUND_COLOR)
        self.score_keeper.draw(self.window)
        [self.window.blit(o.image, (o.rect.x, o.rect.y)) for o in self.game_objects]
        pg.display.update()

    def _create_window(self):
        self.window = pg.display.set_mode((self.dimensions[0], self.dimensions[1]))
        pg.display.set_caption(self.CAPTION)
        pg.display.update()

    def _handle_key_input(self, keys):

        pressed_keys = [k for k in self.ACCEPTABLE_KEYS if k < len(keys) and keys[k]]
        [o.handle_keyboard_input(pressed_keys) for o in self.game_objects]

        if self.left_computer_player is not None:
            output = self.left_computer_player.compute(self.get_neural_net_stimuli(src.game.score_keeper.ScoreKeeper.LEFT_WINNER_DECLARATION))
            pressed_keys = [self.left_computer_player.convert_output_to_keyboard_input(
                output, self.score_keeper.LEFT_WINNER_DECLARATION)]
            [o.handle_keyboard_input(pressed_keys) for o in self.game_objects]

        if self.right_computer_player is not None:
            output = self.right_computer_player.compute(self.get_neural_net_stimuli(src.game.score_keeper.ScoreKeeper.RIGHT_WINNER_DECLARATION))
            pressed_keys = [self.right_computer_player.convert_output_to_keyboard_input(
                output, self.score_keeper.RIGHT_WINNER_DECLARATION)]

            [o.handle_keyboard_input(pressed_keys) for o in self.game_objects]

    def _check_for_collisions(self):
        balls = [o for o in self.game_objects if type(o) is Ball]
        not_balls = [o for o in self.game_objects if type(o) is not Ball]

        paddles_hit = [ball.check_for_bounces(not_balls) for ball in balls][0]
        for p in paddles_hit:
            if p.starting_position[0] < 500:
                self.score_keeper.paddle_hits[0] += 1
            elif p.starting_position[1] > 500:
                self.score_keeper.paddle_hits[1] += 1

    def get_winner(self):
        return self.score_keeper.get_winner()

    def get_performances(self):
        return self.score_keeper.get_player_performances()

    def get_neural_net_stimuli(self, side):
        right_paddle_position = None
        left_paddle_position = None
        left_paddle = [o for o in self.game_objects if o.starting_position[0] < 500 and type(o) is Paddle]
        if len(left_paddle) > 0:
            left_paddle = left_paddle[0]
            left_paddle_position = [left_paddle.rect.x / self.dimensions[0], left_paddle.rect.y / self.dimensions[1]]

        right_paddle = [o for o in self.game_objects if o.starting_position[0] > 500 and type(o) is Paddle]
        if len(right_paddle) > 0:
            right_paddle = right_paddle[0]
            right_paddle_position = [(1000 - right_paddle.rect.x) / self.dimensions[0], right_paddle.rect.y / self.dimensions[1]]

        ball = [o for o in self.game_objects if type(o) is Ball][0]
        if side == src.game.score_keeper.ScoreKeeper.LEFT_WINNER_DECLARATION:
            ball_position = (ball.rect.x / self.dimensions[0], ball.rect.y / self.dimensions[1])
            ball_velocity = np.asarray(ball.velocity) / 8

        else:
            x_ball = 1000 - ball.rect.x
            ball_position = (x_ball / self.dimensions[0], ball.rect.y / self.dimensions[1])
            ball_velocity = np.asarray(ball.velocity) / 8
            ball_velocity[0] *= -1

        if side == src.game.score_keeper.ScoreKeeper.LEFT_WINNER_DECLARATION and left_paddle_position is not None:
            return [*left_paddle_position, *ball_position, *right_paddle_position, *ball_velocity]
        elif side == src.game.score_keeper.ScoreKeeper.RIGHT_WINNER_DECLARATION and right_paddle_position is not None:
            return [*right_paddle_position, *ball_position, *left_paddle_position, *ball_velocity]

    def _should_draw(self):
        return True #not self.do_not_draw and (self.left_computer_player is None or self.right_computer_player is None)

    def start_game(self):
        if self._should_draw():
            pg.init()
            self._create_window()

        while self._should_game_continue():
            if self._should_draw():
                for event in pg.event.get():
                    if self._check_for_window_close(event):
                        self.quit_game_flag = True
                        break

            keys = []
            if self._should_draw():
                keys = pg.key.get_pressed()
            self._handle_key_input(keys)
            self._check_for_collisions()

            self._do_updates()
            if self._should_draw():
                self._do_draws()
            if self._should_draw():
                pg.time.Clock().tick(60)
            self.frames_expired += 1
            if self.frames_expired % 60 == 0:
                 pass # print(self.frames_expired)


        if self._should_draw():
            pg.quit()

