# generic imports
import csv
import os
from flask import jsonify, Blueprint, request

# routes imports
from routes.config import configuration

get_csv_data_bp = Blueprint('get_csv_data', __name__)

@get_csv_data_bp.route('/get_csv_data', methods=['POST'])
def get_csv_data():
    output_path = configuration.OUTPUT_PATH

    csv_path = f'{output_path}\\wallet_sleuth_output.csv'

    if not os.path.exists(csv_path):
        return jsonify({'data': []})

    data = []

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append({
                'Type': row.get('Type', ''),
                'Currency': row.get('Currency', ''),
                'Address/Transaction': row.get('Address/Transaction', ''),
                'Wallet': row.get('Wallet', ''),
                'Path': row.get('Path', '')
            })
            
    return jsonify({'data': data})

@get_csv_data_bp.route('/csv_ready', methods=['GET'])
def csv_ready():
    output_dir = request.args.get('output_dir', configuration.OUTPUT_PATH)
    csv_path = os.path.join(output_dir, 'wallet_sleuth_output.csv')
    exists = os.path.isfile(csv_path)

    return jsonify({'ready': exists})