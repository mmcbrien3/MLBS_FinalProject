from src.ml.neuro_evolution_controller import NeuroEvolutionController
from src.ml.neat_controller import  NEATController
import src.ml.match
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
        elif config['genetic_algorithm'] == 'NEAT':
            self.evolution_controller = NEATController(config, config['neat_config_file'])
        else:
            raise ValueError("Unrecognized type of genetic algorithm from config.")

        self.max_generations = config['max_generations']
        self.max_frames = config['max_frames']
        self.max_score = config['max_score']
        self.max_games_per_generation = config['max_games_per_generation']

        self.solo_generations = config['generation_match_types']['solo_generations']
        self.passing_generations_max = config['generation_match_types']['passing_generations'] + self.solo_generations

        if self.passing_generations_max > self.max_generations:
            raise ValueError("Too many solo and passing generations when compared to max generations in config file.")
        self.current_neural_nets = None
        self.current_generation_matchups = None
        self.neural_net_score_mapping = {}
        self.current_match_type = None
        self.update_current_match_type()

    def update_current_match_type(self):
        if self.evolution_controller.cur_gen < self.solo_generations:
            self.current_match_type = src.ml.match.Match.SOLO_PRACTICE
        elif self.evolution_controller.cur_gen < self.passing_generations_max:
            self.current_match_type = src.ml.match.Match.PASSING
        else:
            self.current_match_type = src.ml.match.Match.FULL
        print("Next generation has match type {}".format(self.current_match_type))

    def run_for_max_generations(self):
        if type(self.evolution_controller) is NEATController:
            self.run_neat_generations()
            return
        for i in range(self.max_generations):
            self.current_neural_nets = self.evolution_controller.increment_gen()
            for nn in self.current_neural_nets:
                self.neural_net_score_mapping[nn] = {"games_won": 0, "games_played": 0, "score": 0}
            self.execute_generation()
            self.update_current_match_type()
        self.evolution_controller.save_best_score()

    def run_neat_generations(self):
        self.evolution_controller.run_for_max_generations()

    def execute_generation(self, genomes=None, config=None):
        st = time.time()
        self.create_matchups()
        self.play_all_matchups()
        self.calculate_and_submit_scores()
        self.neural_net_score_mapping = {}
        print('Generation of {} matchups took {} seconds'.format(len(self.current_generation_matchups), time.time()-st))

    @staticmethod
    def _score_function(score, games_played):
        try:
            return score / games_played
        except ZeroDivisionError:
            return 0

    def calculate_and_submit_scores(self):
        for nn in self.neural_net_score_mapping:
            score = self.neural_net_score_mapping[nn]["score"]
            games_played = self.neural_net_score_mapping[nn]["games_played"]
            self.evolution_controller.submit_network_and_score(nn, self._score_function(score, games_played))

    def play_all_matchups(self):
        pass

    def create_matchups(self):
        all_combinations = itertools.combinations(self.current_neural_nets, 2)

        self.current_generation_matchups = np.asarray(list(all_combinations))
        if len(self.current_generation_matchups) < self.max_games_per_generation:
            for nn in self.neural_net_score_mapping.keys():
                self.neural_net_score_mapping[nn]['games_played'] = len(self.neural_net_score_mapping) - 1
            return
        else:
            games = 0
            games_per_neural_net = {}
            random_games = []
            for nn in self.current_neural_nets:
                games_per_neural_net.update({nn: 0})
            while games < self.max_games_per_generation:
                for nn in self.current_neural_nets:
                    selection = self.current_generation_matchups[
                                np.random.choice(self.current_generation_matchups.shape[0]), :]
                    while nn not in selection:
                        selection = self.current_generation_matchups[
                                    np.random.choice(self.current_generation_matchups.shape[0]), :]
                    random_games.append(selection)
                    games += 1
                    if games >= self.max_games_per_generation:
                        break
            self.current_generation_matchups = random_games
            for m in self.current_generation_matchups:
                games_per_neural_net[m[0]] += 1
                games_per_neural_net[m[1]] += 1
            for nn, games in games_per_neural_net.items():
                self.neural_net_score_mapping[nn]['games_played'] += 1
                print("{} has {} games this generation".format(nn, games))

    def _play_game(self, neural_net_left, neural_net_right):
        match = src.ml.match.Match(self.max_frames, self.max_score, self.current_match_type)
        match.add_players(neural_net_left, neural_net_right)
        match.execute_match()
        return match.get_performances()
