from src.ml.match import Match
from src.ml.network import Network


def lambda_handler(event, context):
    net_one = event['player_one']
    net_two = event['player_two']
    max_frames = event['max_frames']
    max_score = event['max_score']

    p_one = Network()
    p_one.set_save(net_one)

    p_two = Network()
    p_two.set_save(net_two)
    match = Match(max_frames, max_score)
    match.add_players(p_one, p_two)
    match.execute_match()
    return {'performances': match.get_performances()}
