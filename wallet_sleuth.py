print('''
 ██     ██  █████  ██      ██      ███████ ████████     ███████ ██      ███████ ██    ██ ████████ ██   ██ 
 ██     ██ ██   ██ ██      ██      ██         ██        ██      ██      ██      ██    ██    ██    ██   ██ 
 ██  █  ██ ███████ ██      ██      █████      ██        ███████ ██      █████   ██    ██    ██    ███████ 
 ██ ███ ██ ██   ██ ██      ██      ██         ██             ██ ██      ██      ██    ██    ██    ██   ██ 
  ███ ███  ██   ██ ███████ ███████ ███████    ██        ███████ ███████ ███████  ██████     ██    ██   ██ 
 v2026.XX 
''')
#SET VERSION NUMBER


# generic imports
from flask import Flask, render_template, request
import logging

# ws imports
from model.wallets_list import mac_wallets_list, windows_wallets_list, wallets_folders
from model.wallet_card_loader import load_wallet_metadata

# routes imports
from routes.wallet_selection_processing import wallet_selection_processing_bp
from routes.config import os_config_bp
from routes.config import directory_path_bp
from routes.config import output_path_bp
from routes.csv_data import get_csv_data_bp
from routes.log_data import get_log_data_bp

# this prevents anything but Flask errors and print statements displaying in terminal #
logging.basicConfig(level=logging.ERROR)
logging.getLogger('werkzeug').setLevel(logging.ERROR)
####

wallet_sleuth = Flask(__name__)
wallet_sleuth.register_blueprint(wallet_selection_processing_bp)
wallet_sleuth.register_blueprint(os_config_bp)
wallet_sleuth.register_blueprint(directory_path_bp)
wallet_sleuth.register_blueprint(output_path_bp)
wallet_sleuth.register_blueprint(get_csv_data_bp)
wallet_sleuth.register_blueprint(get_log_data_bp)

@wallet_sleuth.route('/')
def home():
    return render_template('home.html')

@wallet_sleuth.route('/identify')
def identify():
    os_choice = request.args.get('os', 'windows').lower()

    if os_choice == 'mac':
        wallets = mac_wallets_list
        wallets = dict(sorted(wallets.items()))

    else:
        wallets = windows_wallets_list
        wallets = dict(sorted(wallets.items()))

    return render_template('identify.html', wallets=wallets, os_choice=os_choice, wallets_folders=wallets_folders)


@wallet_sleuth.route('/wallet_cards')
def wallet_cards():
    metadata_list = load_wallet_metadata()
    return render_template('wallet_cards.html', metadata_list=metadata_list)

if __name__ == "__main__":
    wallet_sleuth.run(debug=True)
    # wallet_sleuth.run(debug=False)