from src.ml.match import Match
from src.ml.network import Network
import boto3
import json

def lambda_handler(event, context):
    net_one = event['player_one']
    net_two = event['player_two']
    max_frames = event['max_frames']
    max_score = event['max_score']
    left_uuid = event['left_uuid']
    right_uuid = event['right_uuid']

    stream_name = event['stream_name']
    kinesis_client = boto3.client('kinesis')

    p_one = Network()
    p_one.set_save(net_one)

    p_two = Network()
    p_two.set_save(net_two)
    match = Match(max_frames, max_score)
    match.add_players(p_one, p_two)
    match.execute_match()

    match_result = {
        'performances': match.get_performances(),
        'left_uuid': left_uuid,
        'right_uuid': right_uuid
    }

    put_record_result = kinesis_client.put_record(StreamName=stream_name,
                                                  Data=json.dumps(match_result).encode(),
                                                  PartitionKey='0')
    print(put_record_result)
    return {
        'Status': 'Success',
        'StatusCode': 200
    }
