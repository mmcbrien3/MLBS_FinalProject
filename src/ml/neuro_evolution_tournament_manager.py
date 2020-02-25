from src.ml.neuro_evolution_controller import NeuroEvolutionController
from src.ml.match import Match
from src.game.score_keeper import ScoreKeeper
import pygame as pg
import numpy as np
import itertools

class NeuroEvolutionTournamentManager(object):

    MAX_FRAMES = 1200
    MAX_SCORE = 2

    def __init__(self):
        self.ne_controller = NeuroEvolutionController()
        self.current_neural_nets = None
        self.max_generations = 10
        self.current_generation_matchups = None
        self.neural_net_score_mapping = {}

    def run_for_max_generations(self):
        for i in range(self.max_generations):
            self.current_neural_nets = self.ne_controller.increment_gen()
            for nn in self.current_neural_nets:
                self.neural_net_score_mapping[nn] = {"games_won": 0, "games_played": 0}
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
            score = self._score_function(
                self.neural_net_score_mapping[nn]["games_played"],
                self.neural_net_score_mapping[nn]["games_won"]
            )
            self.ne_controller.network_score(nn, score)

    def play_all_matchups(self):
        for matchup in self.current_generation_matchups:
            self.neural_net_score_mapping[matchup[0]]["games_played"] += 1
            self.neural_net_score_mapping[matchup[1]]["games_played"] += 1

            winner = self._play_game(matchup[0], matchup[1])

            if winner == ScoreKeeper.LEFT_WINNER_DECLARATION:
                self.neural_net_score_mapping[matchup[0]]["games_won"] += 1
            elif winner == ScoreKeeper.LEFT_WINNER_DECLARATION:
                self.neural_net_score_mapping[matchup[1]]["games_won"] += 1

    def create_matchups(self):
        all_combinations = itertools.combinations(self.current_neural_nets, 2)

        self.current_generation_matchups = all_combinations

    def _play_game(self, neural_net_left, neural_net_right):
        match = Match()
        match.add_players(neural_net_left, neural_net_right)
        match.execute_match()
        return match.get_winner()

if __name__ == "__main__":
    tourney = NeuroEvolutionTournamentManager()
    tourney.run_for_max_generations()
