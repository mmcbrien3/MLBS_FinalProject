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
                        stream_name, max_frames=60*2.5, max_score=1):
    lambda_event = {"max_frames": max_frames, "max_score": max_score}

    lambda_event.update({'player_one': left_network})
    lambda_event.update({'player_two': right_network})
    lambda_event.update({'left_uuid': left_uuid})
    lambda_event.update({'right_uuid': right_uuid})
    lambda_event.update({'stream_name': stream_name})
    return json.dumps(lambda_event).encode()


async def get_data_asynchronous(matches):

    num_workers = int(len(matches) / 10)
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

    for event in batch:
        lambda_client.invoke(FunctionName="execute-match-ExecuteMatchFunction-42K2YE95E4RX",
                             InvocationType='Event',
                             Payload=event)


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