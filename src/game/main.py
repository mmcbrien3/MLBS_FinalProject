from src.game.controller import Controller
from src.game.paddle import Paddle
from src.game.ball import Ball
import pygame as pg

if __name__ == "__main__":
    paddleOne = Paddle()
    paddleTwo = Paddle()
    paddleTwo.key_to_move_map = {pg.K_i: paddleTwo._move_up,
                                pg.K_j: paddleTwo._move_left,
                                pg.K_k: paddleTwo._move_down,
                                pg.K_l: paddleTwo._move_right}
    paddleTwo.set_starting_position((800, 200))

    ball = Ball()
    controller = Controller()
    controller.add_game_objects(paddleOne, paddleTwo, ball)
    controller.start_game()
