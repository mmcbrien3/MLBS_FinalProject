from src.game.controller import Controller
from src.game.paddle import Paddle
from src.game.ball import Ball
import pygame as pg
import os
import pickle
import src.ml.match
from src.ml.network import Network


def get_computer_player():
    neural_net_folder = os.path.join(os.getcwd(), os.pardir, "ml", "neural_nets")
    files = sorted(os.listdir(neural_net_folder), key=lambda s: int(s[s.index("_")+1:]))
    with open(os.path.join(neural_net_folder, "Gen_357"), "rb") as file:
        return pickle.load(file)


if __name__ == "__main__":
    play_against_computer = True

    paddleOne = Paddle()
    paddleTwo = Paddle()
    paddleTwo.key_to_move_map = {pg.K_i: paddleTwo._move_up,
                                pg.K_j: paddleTwo._move_left,
                                pg.K_k: paddleTwo._move_down,
                                pg.K_l: paddleTwo._move_right}
    paddleTwo.set_starting_position((800, 200))

    ball = Ball([-4, 5])
    controller = Controller()
    controller.add_game_objects(paddleOne, paddleTwo, ball)

    if play_against_computer:
        network_dict = get_computer_player()
        computer_network = Network()
        computer_network.set_save(network_dict)
        controller.right_computer_player = computer_network
        controller.score_keeper.match_type = src.ml.match.Match.SOLO_PRACTICE
    controller.start_game()
