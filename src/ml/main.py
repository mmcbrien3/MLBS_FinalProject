import json
import os
from src.ml.cloud_tournment_manager import CloudTournamentManager
from src.ml.local_tournament_manager import LocalTournamentManager

ML_CONFIG_FILE_LOCATION = os.path.join(os.path.dirname(__file__), 'ml_config.json')


if __name__ == "__main__":
    with open(ML_CONFIG_FILE_LOCATION, 'r') as json_file:
        config = json.load(json_file)

    tm = None
    if config['run_in_cloud']:
        tm = CloudTournamentManager(config)
    else:
        tm = LocalTournamentManager(config)

    tm.run_for_max_generations()
