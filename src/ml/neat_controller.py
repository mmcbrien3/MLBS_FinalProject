import itertools
import pickle
import os

import neat
import numpy as np

import src.ml.base_controller
from src.aws import post_to_lambda
from src.ml.neat_network import NEATNetwork
from src.aws.kinesis_manager import KinesisManager


class NEATController(src.ml.base_controller.BaseController):

    def __init__(self, ml_config, neat_config):
        super().__init__()
        self.config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                  neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                  neat_config)

        self.population = neat.Population(self.config)
        self.genomes = None
        self.neural_net_score_mapping = {}
        self.current_match_type = src.ml.match.Match.SOLO_PRACTICE
        self.stream_name = "execute_match_stream"
        self.kinesis_manager = KinesisManager()
        self.kinesis_manager.create_stream(self.stream_name, shard_count=1)
        self.max_frames = ml_config['max_frames']
        self.max_score = ml_config['max_score']
        self.play_in_cloud = ml_config['run_in_cloud']
        self.solo_generations = ml_config['generation_match_types']['solo_generations']
        self.passing_generations_max = ml_config['generation_match_types']['passing_generations']

    def run_for_max_generations(self):
        winner = self.population.run(self.evaluate_genomes, 100)

    def evaluate_genomes(self, genomes, config):
        self.cur_gen += 1
        self.genomes = genomes
        for g in self.genomes:
            net = NEATNetwork()
            net.network = neat.nn.FeedForwardNetwork.create(g[1], self.config)
            net.genome = g[1]
            self.neural_net_score_mapping[net] = {"score": 0}
        self.execute_generation()
        self.update_current_match_type()
        self.save_best_genome()

    def save_best_genome(self):
        max_fitness = -1
        max_g = None
        for g in self.genomes:
            if g[1].fitness > max_fitness:
                max_fitness = g[1].fitness
                max_g = g[1]

        with open(os.path.join('neat_nets', 'neat_gen_{}'.format(self.cur_gen)), 'wb') as f:
            pickle.dump(max_g, f)

    def execute_generation(self):
        self.create_matchups()
        self.play_all_matchups()
        self.calculate_and_submit_scores()
        self.neural_net_score_mapping = {}

    def calculate_and_submit_scores(self):
        for nn in self.neural_net_score_mapping:
            score = self.neural_net_score_mapping[nn]["score"]
            nn.genome.fitness = int(score)

    def play_all_matchups(self):
        if self.play_in_cloud:
            self.play_all_matchups_in_cloud()
        else:
            self.play_all_matchups_locally()

    def play_all_matchups_in_cloud(self):
        lambda_matches = []
        output_dict = {}
        for matchup in self.current_generation_matchups:
            lambda_matches.append(post_to_lambda.create_lambda_event(matchup[0].get_save(),
                                                                     matchup[1].get_save(),
                                                                     matchup[0].uuid,
                                                                     matchup[1].uuid,
                                                                     self.kinesis_manager.stream_name,
                                                                     self.current_match_type,
                                                                     max_frames=self.max_frames,
                                                                     max_score=self.max_score,
                                                                     network_type='neat'))

        output_dict = post_to_lambda.run_generation(lambda_matches, self.kinesis_manager)
        for uuid, score in output_dict.items():

            for nn in self.neural_net_score_mapping.keys():
                if nn.uuid == uuid:
                    self.neural_net_score_mapping[nn]["score"] += score
                    break

        print(self.neural_net_score_mapping)

    def play_all_matchups_locally(self):

        for matchup in self.current_generation_matchups:

            performances = self._play_game(matchup[0][1], matchup[1][1])

            self.neural_net_score_mapping[matchup[0]]["score"] += performances[0]
            self.neural_net_score_mapping[matchup[1]]["score"] += performances[1]

    def create_matchups(self):
        all_combinations = itertools.combinations(list(self.neural_net_score_mapping.keys()), 2)

        self.current_generation_matchups = list(all_combinations)

    def update_current_match_type(self):
        if self.cur_gen < self.solo_generations:
            self.current_match_type = src.ml.match.Match.SOLO_PRACTICE
        elif self.cur_gen < self.passing_generations_max:
            self.current_match_type = src.ml.match.Match.PASSING
        else:
            self.current_match_type = src.ml.match.Match.FULL
        print("Next generation has match type {}".format(self.current_match_type))

    def _play_game(self, neural_net_left, neural_net_right):
        match = src.ml.match.Match(self.max_frames, self.max_score, self.current_match_type)

        match.add_players(neural_net_left, neural_net_right)
        match.execute_match()
        return match.get_performances()