from src.ml.match import Match


def lambda_handler(event, context):
    p_one = event['player_one']
    p_two = event['player_two']
    max_frames = event['max_frames']
    max_score = event['max_score']
    match = Match(max_frames, max_score)
    match.add_players(p_one, p_two)
    match.execute_match()
    return match.get_performances()
