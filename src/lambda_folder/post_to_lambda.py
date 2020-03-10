import requests
import pickle
import os
from uuid import uuid4
import asyncio
from typing import Dict, List
from concurrent.futures import ThreadPoolExecutor

api_url = "https://g9sjqvnoql.execute-api.us-east-1.amazonaws.com/Prod/execute_match/"

def create_lambda_event(left_network, right_network, left_uuid, right_uuid, max_frames=60*2.5, max_score=1):
    lambda_event = {"max_frames": max_frames, "max_score": max_score}

    lambda_event.update({'player_one': left_network})
    lambda_event.update({'player_two': right_network})
    lambda_event.update({'left_uuid': left_uuid})
    lambda_event.update({'right_uuid': right_uuid})
    return lambda_event


async def get_data_asynchronous(matches, output_dict):

    with ThreadPoolExecutor(max_workers=5000) as executor:
        with requests.Session() as session:

            # Initialize the event loop
            loop = asyncio.get_event_loop()

            tasks = [loop.run_in_executor(executor, post_to_lambda, *(session,
                                                                      match,
                                                                      output_dict))
                     for match in matches]

            for response in await asyncio.gather(*tasks):
                pass
    return output_dict


def post_to_lambda(session, event, output_dict):
    resp = session.post(api_url, json=event).json()

    output_dict[event['left_uuid']] += resp['performances'][0]
    output_dict[event['right_uuid']] += resp['performances'][1]


def run_generation(list_of_matches: List[Dict], output_dict):

    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_data_asynchronous(list_of_matches, output_dict))
    loop.run_until_complete(future)

    return output_dict