from src.ml.match import Match
from src.ml.network import Network
from src.ml.neat_network import NEATNetwork
import boto3
import json

GAMES_TO_RUN_LOCALLY = 4
def lambda_handler(event, context):

    if type(event) == list and len(event) > GAMES_TO_RUN_LOCALLY:
        lambda_client = boto3.client('lambda')
        for i in range(GAMES_TO_RUN_LOCALLY, len(event), GAMES_TO_RUN_LOCALLY):
            lambda_client.invoke(FunctionName="execute-match-ExecuteMatchFunction-42K2YE95E4RX",
                                 InvocationType='Event',
                                 Payload=json.dumps(event[i:i+2]).encode())
        event = event[:GAMES_TO_RUN_LOCALLY]
    elif type(event) == dict:
        event = [event]

    for current_event in event:
        if type(current_event) == str:
            current_event = json.loads(current_event)
        net_one = current_event['player_one']
        net_two = current_event['player_two']
        max_frames = current_event['max_frames']
        max_score = current_event['max_score']
        match_type = current_event['match_type']
        left_uuid = current_event['left_uuid']
        right_uuid = current_event['right_uuid']

        stream_name = current_event['stream_name']
        kinesis_client = boto3.client('kinesis')

        p_one = None
        p_two = None
        if current_event['network_type'] == 'neat':
            p_one = NEATNetwork()
            p_two = NEATNetwork()
        else:
            p_one = Network()
            p_two = Network()

        p_one.set_save(net_one)

        p_two.set_save(net_two)
        match = Match(max_frames, max_score, match_type)
        match.add_players(p_one, p_two)
        match.execute_match()

        match_result = {
            'performances': match.get_performances(),
            'left_uuid': left_uuid,
            'right_uuid': right_uuid,
        }

        put_record_result = kinesis_client.put_record(StreamName=stream_name,
                                                      Data=json.dumps(match_result).encode(),
                                                      PartitionKey='0')
        print(put_record_result)
    return {
        'Status': 'Success',
        'StatusCode': 200
    }
