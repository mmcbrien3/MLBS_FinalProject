from src.aws import post_to_lambda
from src.ml.base_tournament_manager import BaseTournamentManager

class CloudTournamentManager(BaseTournamentManager):

    def __init__(self, config):
        super().__init__(config)

    def play_all_matchups(self):
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
