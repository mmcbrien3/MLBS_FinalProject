from src.aws import post_to_lambda
from src.ml.base_tournament_manager import BaseTournamentManager
from src.aws.kinesis_manager import KinesisManager

class CloudTournamentManager(BaseTournamentManager):

    def __init__(self, config):
        super().__init__(config)

        stream_name = "execute_match_stream"
        print("Setting up kinesis stream: {}".format(stream_name))
        self.kinesis_manager = KinesisManager()
        self.kinesis_manager.create_stream(stream_name, shard_count=1)

    def play_all_matchups(self):
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
                                                                     max_score=self.max_score))

        output_dict = post_to_lambda.run_generation(lambda_matches, self.kinesis_manager, self.current_match_type)
        for uuid, score in output_dict.items():

            for nn in self.neural_net_score_mapping.keys():
                if nn.uuid == uuid:
                    self.neural_net_score_mapping[nn]["score"] = score
                    break

        print(self.neural_net_score_mapping)

    def run_for_max_generations(self):
        super().run_for_max_generations()
        self.kinesis_manager.delete_stream()
