from src.ml.neuro_evolution_controller import NeuroEvolutionController
from src.ml.match import Match
import numpy as np
import time
import itertools


class BaseTournamentManager(object):

    def __init__(self, config):

        if config['genetic_algorithm'] == 'NeuroEvolution':
            self.evolution_controller = NeuroEvolutionController(
                config['num_per_gen'], config['num_children'], config['elite_percentage'],
                config['mutation_rate'], config['mutation_range'], config['completely_new_rate'],
                config['network_layers']
            )
        else:
            raise ValueError("Unrecognized type of genetic algorithm from config.")

        self.max_generations = config['max_generations']
        self.max_frames = config['max_frames']
        self.max_score = config['max_score']

        self.current_neural_nets = None
        self.current_generation_matchups = None
        self.neural_net_score_mapping = {}

    def run_for_max_generations(self):
        for i in range(self.max_generations):
            self.current_neural_nets = self.evolution_controller.increment_gen()
            for nn in self.current_neural_nets:
                self.neural_net_score_mapping[nn] = {"games_won": 0, "games_played": 0, "score": 0}
            self.execute_generation()

    def execute_generation(self):
        st = time.time()
        self.create_matchups()
        self.play_all_matchups()
        self.calculate_and_submit_scores()
        print('Generation of {} matchups took {} seconds'.format(len(self.current_generation_matchups), time.time()-st))

    @staticmethod
    def _score_function(games_played, games_won):
        try:
            return games_played / games_won
        except ZeroDivisionError:
            return 0

    def calculate_and_submit_scores(self):
        for nn in self.neural_net_score_mapping:
            score = self.neural_net_score_mapping[nn]["score"]
            self.evolution_controller.submit_network_and_score(nn, score)

    def play_all_matchups(self):
        pass

    def create_matchups(self):
        all_combinations = itertools.combinations(self.current_neural_nets, 2)

        self.current_generation_matchups = np.asarray(list(all_combinations))

    def _play_game(self, neural_net_left, neural_net_right):
        match = Match(self.max_frames, self.max_score)
        match.add_players(neural_net_left, neural_net_right)
        match.execute_match()
        return match.get_performances()
