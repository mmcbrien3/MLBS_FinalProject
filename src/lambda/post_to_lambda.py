import requests
import pickle
import os

api_url = "https://61u7b2milg.execute-api.us-east-1.amazonaws.com/execute_match"
lambda_event = {"max_frames": 60 * 2.5, "max_score": 1}

with open(os.path.join(os.pardir, 'ml', 'neural_nets', 'Gen_1'), 'rb') as f:
    lambda_event.update({'player_one': pickle.load(f)})

with open(os.path.join(os.pardir, 'ml', 'neural_nets', 'Gen_2'), 'rb') as f:
    lambda_event.update({'player_two': pickle.load(f)})

print(requests.post(api_url, data=lambda_event))
