from src.ml.neuro_evolution_controller import NeuroEvolutionController
from src.ml.match import Match
from src.game.score_keeper import ScoreKeeper
import pygame as pg
import numpy as np
import itertools


class TournamentManager(object):

    def __init__(self):
        self.evolution_controller = NeuroEvolutionController()
        self.current_neural_nets = None
        self.max_generations = 100
        self.current_generation_matchups = None
        self.neural_net_score_mapping = {}
        self.max_frames = 60 * 2.5
        self.max_score = 1

    def run_for_max_generations(self):
        for i in range(self.max_generations):
            self.current_neural_nets = self.evolution_controller.increment_gen()
            for nn in self.current_neural_nets:
                self.neural_net_score_mapping[nn] = {"games_won": 0, "games_played": 0, "score": 0}
            self.execute_generation()

    def execute_generation(self):
        self.create_matchups()
        self.play_all_matchups()
        self.calculate_and_submit_scores()

    @staticmethod
    def _score_function(games_played, games_won):
        try:
            return games_played / games_won
        except ZeroDivisionError:
            return 0

    def calculate_and_submit_scores(self):
        for nn in self.neural_net_score_mapping:
            score = self.neural_net_score_mapping[nn]["score"]
            # self._score_function(
            #     self.neural_net_score_mapping[nn]["games_played"],
            #     self.neural_net_score_mapping[nn]["games_won"]
            # )
            self.evolution_controller.submit_network_and_score(nn, score)

    def play_all_matchups(self):
        fraction_of_matchups = 1 / 2
        matchup_indexes = np.random.choice(self.current_generation_matchups.shape[0],
                                            round(self.current_generation_matchups.shape[0] //
                                                  (1 / fraction_of_matchups)))
        for idx in matchup_indexes:
            matchup = self.current_generation_matchups[idx]
            self.neural_net_score_mapping[matchup[0]]["games_played"] += 1
            self.neural_net_score_mapping[matchup[1]]["games_played"] += 1

            performances = self._play_game(matchup[0], matchup[1])

            self.neural_net_score_mapping[matchup[0]]["score"] += performances[0]
            self.neural_net_score_mapping[matchup[1]]["score"] += performances[1]

    def create_matchups(self):
        all_combinations = itertools.combinations(self.current_neural_nets, 2)

        self.current_generation_matchups = np.asarray(list(all_combinations))

    def _play_game(self, neural_net_left, neural_net_right):
        match = Match(self.max_frames, self.max_score)
        match.add_players(neural_net_left, neural_net_right)
        match.execute_match()
        return match.get_performances()


if __name__ == "__main__":
    tourney = TournamentManager()
    tourney.run_for_max_generations()
