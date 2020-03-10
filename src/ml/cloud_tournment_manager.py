from src.ml.neuro_evolution_controller import NeuroEvolutionController
from src.ml.match import Match
import numpy as np
import itertools
from src.lambda_folder import post_to_lambda

class CloudTournamentManager(object):

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
        self.play_all_matchups_in_the_cloud()
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

    def play_all_matchups_in_the_cloud(self):
        lambda_matches = []
        output_dict = {}
        for matchup in self.current_generation_matchups:
            lambda_matches.append(post_to_lambda.create_lambda_event(matchup[0].get_save(),
                                                                     matchup[1].get_save(),
                                                                     matchup[0].uuid,
                                                                     matchup[1].uuid,
                                                                     max_frames=self.max_frames,
                                                                     max_score=self.max_score))

        [output_dict.update({nn.uuid: 0}) for nn in self.current_neural_nets]
        output_dict = post_to_lambda.run_generation(lambda_matches, output_dict)
        for uuid, score in output_dict.items():

            for nn in self.neural_net_score_mapping.keys():
                if nn.uuid == uuid:
                    self.neural_net_score_mapping[nn]["score"] = score
                    break

    def create_matchups(self):
        all_combinations = itertools.combinations(self.current_neural_nets, 2)

        self.current_generation_matchups = np.asarray(list(all_combinations))

    def _play_game(self, neural_net_left, neural_net_right):
        match = Match(self.max_frames, self.max_score)
        match.add_players(neural_net_left, neural_net_right)
        match.execute_match()
        return match.get_performances()


if __name__ == "__main__":
    tourney = CloudTournamentManager()
    tourney.run_for_max_generations()
