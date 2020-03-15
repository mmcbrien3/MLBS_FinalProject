import numpy as np
from src.ml.base_tournament_manager import BaseTournamentManager


class LocalTournamentManager(BaseTournamentManager):

    def __init__(self, config):
        super().__init__(config)

    def play_all_matchups(self):

        for matchup in self.current_generation_matchups:
            self.neural_net_score_mapping[matchup[0]]["games_played"] += 1
            self.neural_net_score_mapping[matchup[1]]["games_played"] += 1

            performances = self._play_game(matchup[0], matchup[1])

            self.neural_net_score_mapping[matchup[0]]["score"] += performances[0]
            self.neural_net_score_mapping[matchup[1]]["score"] += performances[1]

