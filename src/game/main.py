import os
import pickle

import neat
import pygame as pg

import src.ml.match
from src.game.ball import Ball
from src.game.controller import Controller
from src.game.paddle import Paddle
from src.ml.neat_network import NEATNetwork
from src.ml.network import Network


def get_computer_player(computer_gen, play_against_neat):
    neural_net_folder = os.path.join(os.getcwd(), os.pardir, "ml", "neural_nets")
    neat_net_folder = os.path.join(os.getcwd(), os.pardir, 'ml', 'neat_nets')
    files = sorted(os.listdir(neural_net_folder), key=lambda s: int(s[s.index("_")+1:]))

    if play_against_neat:
        net_path = os.path.join(neat_net_folder, "neat_gen_{}".format(computer_gen))
    else:
        net_path = os.path.join(neural_net_folder, "Gen_{}".format(computer_gen))
    with open(net_path, "rb") as file:
        return pickle.load(file)


if __name__ == "__main__":
    play_against_computer = True
    play_against_neat = True
    computer_gen = 278

    if play_against_computer:
        network_dict = get_computer_player(computer_gen, play_against_neat)

        if play_against_neat:
            neat_config = os.path.join(os.getcwd(), os.pardir, 'ml', 'neat_config.config')
            config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                 neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                 neat_config)
            computer_network = NEATNetwork()
            computer_network.network = neat.nn.FeedForwardNetwork.create(network_dict, config)
        else:
            computer_network = Network()
            computer_network.set_save(network_dict)

    computer_gen = 250

    if play_against_computer:
        network_dict = get_computer_player(computer_gen, play_against_neat)

        if play_against_neat:
            neat_config = os.path.join(os.getcwd(), os.pardir, 'ml', 'neat_config.config')
            config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                 neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                 neat_config)
            computer_network_2 = NEATNetwork()
            computer_network_2.network = neat.nn.FeedForwardNetwork.create(network_dict, config)
        else:
            computer_network_2 = Network()
            computer_network_2.set_save(network_dict)


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

    controller.right_computer_player = computer_network_2
    controller.left_computer_player = computer_network

    controller.score_keeper.match_type = src.ml.match.Match.SOLO_PRACTICE
    controller.start_game()
