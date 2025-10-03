# generic imports
import os
from flask import jsonify, Blueprint, request

# routes imports
from routes.config import configuration

get_log_data_bp = Blueprint('get_log_data', __name__)

@get_log_data_bp.route('/get_log_data', methods=['POST'])
def get_log_data():
    output_path = configuration.OUTPUT_PATH
    log_path = os.path.join(output_path, 'wallet_sleuth_logging.txt')

    if not os.path.exists(log_path):
        return jsonify({'data': 'Log file not found.'})

    with open(log_path, 'r', encoding='utf-8') as logfile:
        contents = logfile.read()

    return jsonify({'data': contents})

@get_log_data_bp.route('/log_ready', methods=['GET'])
def log_ready():
    output_dir = request.args.get('output_dir', configuration.OUTPUT_PATH)
    log_path = os.path.join(output_dir, 'wallet_sleuth_logging.txt')

    exists = os.path.isfile(log_path)

    return jsonify({'ready': exists})