import os
import shutil


def clear_old_code():
    lambda_function_folder = os.path.join(os.path.dirname(__file__), 'sam_execute_match', 'execute_match')
    if os.path.isdir(lambda_function_folder):
        shutil.rmtree(lambda_function_folder)
    os.mkdir(lambda_function_folder)


def get_latest_code():
    game_required_files = None
    asset_required_files = None
    ml_required_files = ['match.py', 'network.py', 'neat_network.py', 'layer.py', 'neuron.py']

    sam_folder = os.path.join(os.path.dirname(__file__), 'sam_execute_match', 'execute_match')
    src_folder = os.path.join(os.path.dirname(__file__), os.pardir)
    game_folder = os.path.join(src_folder, 'game')
    ml_folder = os.path.join(src_folder, 'ml')
    asset_folder = os.path.join(src_folder, os.pardir, 'assets')

    code_files = []
    code_files.extend(get_code_from_folder(ml_folder, ml_required_files))
    code_files.extend(get_code_from_folder(asset_folder, asset_required_files))

    os.mkdir(os.path.join(sam_folder, 'src'))

    sam_game_folder = os.path.join(sam_folder, 'src', 'game')
    os.mkdir(sam_game_folder)
    for file in get_code_from_folder(game_folder, game_required_files):
        shutil.copy(file, sam_game_folder)

    sam_ml_folder = os.path.join(sam_folder, 'src', 'ml')
    os.mkdir(sam_ml_folder)
    for file in get_code_from_folder(ml_folder, ml_required_files):
        shutil.copy(file, sam_ml_folder)

    sam_asset_folder = os.path.join(sam_folder, 'assets')
    os.mkdir(sam_asset_folder)
    for file in get_code_from_folder(asset_folder, asset_required_files):
        shutil.copy(file, sam_asset_folder)

    lambda_reqs_file = os.path.join(os.path.dirname(__file__), 'lambda-requirements.txt')
    lambda_function_file = os.path.join(os.path.dirname(__file__), 'lambda_function.py')
    shutil.copy(lambda_reqs_file, os.path.join(sam_folder, 'requirements.txt'))
    shutil.copy(lambda_function_file, os.path.join(sam_folder, 'app.py'))



def get_code_from_folder(folder, required_files):
    code_files = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if required_files is None or file in required_files:
                code_files.append(os.path.join(root, file))
    return code_files

def deploy_with_sam():
    LAMBDA_S3_BUCKET = "execute-match"
    AWS_REGION = "us-east-1"
    BASE_PATH = os.path.join(os.path.dirname(__file__), 'sam_execute_match')
    STACK_NAME = "execute-match"
    BUILD_DIR = os.path.join(BASE_PATH, 'build_artifact')

    if not os.path.exists(BUILD_DIR):
        os.mkdir(BUILD_DIR)

    os.system("cd \"%s\" && sam build --template template.yaml --build-dir \"%s\"" % (BASE_PATH, BUILD_DIR))
    os.system(
        "cd \"%s\" && sam package --template-file \"%s/template.yaml\" --output-template-file packaged.yaml --s3-bucket \"%s\"" % (
        BASE_PATH, BUILD_DIR, LAMBDA_S3_BUCKET))
    os.system(
        "cd \"%s\" && sam deploy  --template-file packaged.yaml --stack-name %s --capabilities CAPABILITY_IAM --region %s" % (
        BASE_PATH, STACK_NAME, AWS_REGION))


if __name__ == "__main__":
    clear_old_code()
    get_latest_code()
    deploy_with_sam()
