# generic imports
from flask import Blueprint, request, jsonify

os_config_bp = Blueprint('os_config', __name__)
directory_path_bp = Blueprint('directory_config', __name__)
output_path_bp = Blueprint('output_config', __name__)

class Config:
    OS_SELECTION = 'windows'
    DIRECTORY_PATH = None
    OUTPUT_PATH = None

configuration = Config()

@os_config_bp.route('/print_os_selection', methods=['POST'])
def print_os_selection():
    data = request.get_json()
    configuration.OS_SELECTION = data.get('os_choice')
    # print(configuration.OS_SELECTION)
    return jsonify({'status': 'ok'})

@directory_path_bp.route('/print_directory_path', methods=['POST'])
def print_directory_path():
    data = request.get_json()
    configuration.DIRECTORY_PATH = data.get('directoryPath')
    # print(configuration.DIRECTORY_PATH)
    return jsonify({'status': 'ok'})

@directory_path_bp.route('/print_output_path', methods=['POST'])
def print_output_path():
    data = request.get_json()
    configuration.OUTPUT_PATH = data.get('outputPath')
    # print(configuration.OUTPUT_PATH)
    return jsonify({'status': 'ok'})