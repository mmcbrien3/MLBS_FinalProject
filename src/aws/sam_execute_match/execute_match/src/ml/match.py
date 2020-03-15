import src.game.controller
from src.game.paddle import Paddle
from src.game.ball import Ball
import pygame as pg
import random

class Match(object):

    SOLO_PRACTICE = "Solo Practice"
    PASSING = "Passing"
    FULL = "Full"

    def __init__(self, max_frames, max_score, match_type):
        self.max_frames = max_frames
        self.max_score = max_score
        self.left_neural_net = None
        self.right_neural_net = None
        self.winner = None
        self.game_controller = src.game.controller.Controller()
        self.game_controller.frame_rate = 9999
        self.match_type = match_type
        self._set_up_controller()
        self.both_performances = [0, 0]

    def _set_up_controller(self, play_left_side=True):
        paddle_one = Paddle()
        paddle_two = Paddle()
        paddle_two.key_to_move_map = {pg.K_i: paddle_two._move_up,
                                     pg.K_l: paddle_two._move_left,
                                     pg.K_k: paddle_two._move_down,
                                     pg.K_j: paddle_two._move_right}
        paddle_two.set_starting_position((800, 200))

        self.game_controller.score_keeper.set_match_type(self.match_type)
        if self.match_type == self.FULL or self.match_type == self.PASSING:
            ball = Ball()
            self.game_controller.add_game_objects(paddle_one, paddle_two, ball)
        else:
            random_y_speeds = [-10, -9, -8, -7, -6, -5, 5, 6, 7, 8, 9, 10]
            if play_left_side:
                ball = Ball([random.randint(-2, 0), random_y_speeds[random.randint(0, len(random_y_speeds)-1)]])
                self.game_controller.add_game_objects(paddle_one, ball)
            else:
                ball = Ball([random.randint(0, 5), random_y_speeds[random.randint(0, len(random_y_speeds)-1)]])
                self.game_controller.add_game_objects(paddle_two, ball)
        self.game_controller.max_frames = self.max_frames
        self.game_controller.set_max_score(self.max_score)
        self.game_controller.do_not_draw = True

    def add_players(self, left_player, right_player):
        self.left_neural_net = left_player
        self.right_neural_net = right_player

        if self.match_type != self.SOLO_PRACTICE:
            self.game_controller.left_computer_player = self.left_neural_net
            self.game_controller.right_computer_player = self.right_neural_net

    def execute_match(self):
        if self.match_type == self.SOLO_PRACTICE:
            self.game_controller = src.game.controller.Controller()
            self._set_up_controller(play_left_side=True)
            self.game_controller.left_computer_player = self.left_neural_net
            self.game_controller.start_game()
            self.both_performances[0] += self.game_controller.get_performances()[0]
            self.game_controller = src.game.controller.Controller()
            self._set_up_controller(play_left_side=False)
            self.game_controller.right_computer_player = self.right_neural_net
            self.game_controller.start_game()
            self.both_performances[1] += self.game_controller.get_performances()[1]
        else:
            self.game_controller.start_game()

    def get_performances(self):
        if self.match_type != self.SOLO_PRACTICE:
            return self.game_controller.get_performances()
        else:
            return self.both_performances
