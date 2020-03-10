import numpy as np
from src.ml.base_tournament_manager import BaseTournamentManager


class LocalTournamentManager(BaseTournamentManager):

    def __init__(self, config):
        super().__init__(config)

    def play_all_matchups(self):
        fraction_of_matchups = 1.0
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

