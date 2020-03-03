from src.game.controller import Controller
from src.game.paddle import Paddle
from src.game.ball import Ball
import pygame as pg

class Match(object):

    MAX_FRAMES_IN_GAME = 25 * 10
    MAX_SCORE = 1

    def __init__(self):
        self.left_neural_net = None
        self.right_neural_net = None
        self.winner = None
        self.game_controller = Controller()
        self.game_controller.frame_rate = 9999
        self._set_up_controller()

    def _set_up_controller(self):
        paddle_one = Paddle()
        paddle_two = Paddle()
        paddle_two.key_to_move_map = {pg.K_i: paddle_two._move_up,
                                     pg.K_j: paddle_two._move_left,
                                     pg.K_k: paddle_two._move_down,
                                     pg.K_l: paddle_two._move_right}
        paddle_two.set_starting_position((800, 200))

        ball = Ball()
        self.game_controller.add_game_objects(paddle_one, paddle_two, ball)
        self.game_controller.max_frames = self.MAX_FRAMES_IN_GAME
        self.game_controller.set_max_score(self.MAX_SCORE)

    def add_players(self, left_player, right_player):
        self.left_neural_net = left_player
        self.right_neural_net = right_player
        self.game_controller.right_computer_player = self.right_neural_net
        self.game_controller.left_computer_player = self.left_neural_net

    def execute_match(self):
        self.game_controller.start_game()

    def get_performances(self):
        return self.game_controller.get_performances()
