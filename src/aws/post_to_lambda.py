import boto3
import asyncio
from typing import Dict, List
import numpy as np
import time
from concurrent.futures import ThreadPoolExecutor
import json

api_url = "https://g9sjqvnoql.execute-api.us-east-1.amazonaws.com/Prod/execute_match/"

def create_lambda_event(left_network, right_network,
                        left_uuid, right_uuid,
                        stream_name, match_type,
                        max_frames=60*2.5, max_score=1, network_type='ne'):
    lambda_event = {"max_frames": max_frames, "max_score": max_score}

    lambda_event.update({'player_one': left_network})
    lambda_event.update({'player_two': right_network})
    lambda_event.update({'left_uuid': left_uuid})
    lambda_event.update({'right_uuid': right_uuid})
    lambda_event.update({'stream_name': stream_name})
    lambda_event.update({'match_type': match_type})
    lambda_event.update({'network_type': network_type})
    return json.dumps(lambda_event)


async def get_data_asynchronous(matches):

    num_workers = np.min((int(len(matches) / 2), 200))
    num_workers = num_workers if num_workers > 0 else 1
    batches_of_matches = []
    size_of_batch = int(np.ceil(len(matches) / num_workers))
    for i in range(0, len(matches), size_of_batch):
        batches_of_matches.append(matches[i:i+size_of_batch])
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        lambda_client = boto3.client('lambda')

        # Initialize the event loop
        loop = asyncio.get_event_loop()

        tasks = [loop.run_in_executor(executor, post_to_lambda, *(lambda_client,
                                                                  batch))
                 for batch in batches_of_matches]

        for response in await asyncio.gather(*tasks):
            pass


def post_to_lambda(lambda_client, batch):

    lambda_client.invoke(FunctionName="execute-match-ExecuteMatchFunction-42K2YE95E4RX",
                         InvocationType='Event',
                         Payload=json.dumps(batch).encode())


def pull_results_from_kinesis(kinesis_manager, number_of_matches):

    return kinesis_manager.read_next_n_records(number_of_matches)


def run_generation(list_of_matches: List[Dict], kinesis_manager):

    print('Submitting Lambda Events...')
    st = time.time()
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_data_asynchronous(list_of_matches))
    loop.run_until_complete(future)
    print('Took {} seconds to submit all events'.format(time.time() - st))

    print('Waiting on results from Kinesis...')
    return pull_results_from_kinesis(kinesis_manager, len(list_of_matches))

if __name__ == "__main__":
    events = list(range(4))
    lc = boto3.client('lambda')
    st = time.time()
    for event in events:
        lc.invoke(FunctionName="execute-match-ExecuteMatchFunction-42K2YE95E4RX",
                                 InvocationType='Event',
                                 Payload=json.dumps(str(event)))
    print("Took {} seconds".format(time.time() - st))


