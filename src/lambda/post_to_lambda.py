import requests
import pickle
import os
import sys
import json

api_url = "https://g9sjqvnoql.execute-api.us-east-1.amazonaws.com/Prod/execute_match/"
lambda_event = {"max_frames": 60 * 2.5, "max_score": 1}

with open(os.path.join(os.pardir, 'ml', 'neural_nets', 'Gen_8'), 'rb') as f:
    lambda_event.update({'player_one': pickle.load(f)})

with open(os.path.join(os.pardir, 'ml', 'neural_nets', 'Gen_9'), 'rb') as f:
    lambda_event.update({'player_two': pickle.load(f)})

print("Sending the following data to lambda: {}".format(json.dumps(lambda_event)))
print(requests.post(api_url, json=lambda_event).json())