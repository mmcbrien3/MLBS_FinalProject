from neuro_evolution_controller import NeuroEvolutionController
import pygame as pg
import numpy as np


class NeuroEvolutionTournamentManager(object):

    MAX_FRAMES = 1200
    MAX_SCORE = 2
    LEFT_INPUTS = [pg.K_w, pg.K_a, pg.K_s, pg.K_d]
    RIGHT_INPUTS = [pg.K_i, pg.K_j, pg.K_k, pg.K_l]

    def __init__(self):
        ne_controller = NeuroEvolutionController()
        ne_controller.increment_gen()

    def create_matchups(self):
        pass

    def play_game(self, neural_net_left, neural_net_right):
        pass

    def convert_output_to_keyboard_input(self, nn_output, side):
        if side == "LEFT":
            return self.LEFT_INPUTS[np.argmax(nn_output)]
        else:
            return self.RIGHT_INPUTS[np.argmax(nn_output)]
