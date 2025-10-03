# generic imports
from flask import Blueprint, request, jsonify
import os
import csv
import datetime
import inspect
import re

# routes imports
from routes.config import configuration

# model imports
from model.load_wallets import load_wallet_functions

# utils imports
from utils.wallet_utils import currency_types, normalize_type
from utils.pyinstaller_utils import resource_path

wallet_selection_processing_bp = Blueprint('selection', __name__)

@wallet_selection_processing_bp.route('/process_selection', methods=['POST'])
def process_selection():
    
    # print('Wallet Sleuth - Processing...')
    data = request.get_json()
    wallets = data.get('wallets', [])
    browsers = data.get('browsers', {})

    selected_wallets = []

    for wallet in wallets:
        # print('-------------------')
        # print('wallet_selection_processing.py')
        # print(wallets)
        selected_browsers = browsers.get(wallet, [])
        
        if selected_browsers:
            for browser in selected_browsers:
                selected = f"{wallet.lower().replace(' ', '_').replace('-browser_wallets','')}_{browser.lower()}"
                selected_wallets.append(selected)
        else:
            selected = wallet.lower().replace(' ', '_').replace('-desktop_wallets','').replace('-browser_wallets','')
            selected_wallets.append(selected)
    

    # print('------------------------------------------------')
    # print('wallet_selection_prcessing.py - Selected OS:', configuration.OS_SELECTION)
    # print('wallet_selection_prcessing.py - Typed Directory:', configuration.DIRECTORY_PATH)
    # print('wallet_selection_prcessing.py - Typed Output:', configuration.OUTPUT_PATH)
    # print('wallet_selection_processing.py - User selections:', selected_wallets)
    # print('------------------------------------------------')
    
    output_path = configuration.OUTPUT_PATH
    log_file_master = os.path.join(output_path, 'wallet_sleuth_logging.txt')
    formatted_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  
    with open(log_file_master, 'w') as log_file:
        log_file.write('Wallet Sleuth - Process Log\n')
        log_file.write(f'{formatted_datetime}\n')
        log_file.write('------------------------------------------------')
        log_file.write('\n--SETTINGS--')       
        log_file.write(f'\nOPERATING SYSTEM: {configuration.OS_SELECTION.capitalize()}')
        log_file.write(f'\nDIRECTORY PATH: {configuration.DIRECTORY_PATH}')
        log_file.write(f'\nOUTPUT PATH: {configuration.OUTPUT_PATH}')
        log_file.write('\n------------------------------------------------')
        log_file.write('\n--PROCESSES--')

    wallet_functions = load_wallet_functions([
        resource_path('wallet_scripts/browser_wallets'),
        resource_path('wallet_scripts/desktop_wallets'),
    ])

    desktop_wallet_functions = load_wallet_functions([
        resource_path('wallet_scripts/desktop_wallets')
    ])

    browser_wallet_functions = load_wallet_functions([
        resource_path('wallet_scripts/browser_wallets')
    ])

    if 'all_desktop_wallets' in selected_wallets and 'all_browser_wallets' in selected_wallets:
        remove_list = []
        for items in wallet_functions:
            remove_list.append(items)

        remove_list.remove('all_desktop_wallets')
        remove_list.remove('all_browser_wallets')

        selected_wallets = [item for item in selected_wallets if item not in remove_list]

    elif 'all_desktop_wallets' in selected_wallets and 'all_browser_wallets' not in selected_wallets:
        remove_list = []
        for items in desktop_wallet_functions:
            remove_list.append(items)

        remove_list.remove('all_desktop_wallets')

        selected_wallets = [item for item in selected_wallets if item not in remove_list]

    elif 'all_browser_wallets' in selected_wallets and 'all_desktop_wallets' not in selected_wallets:
        remove_list = []

        for items in browser_wallet_functions:
            remove_list.append(items)

        remove_list.remove('all_browser_wallets')
        
        selected_wallets = [item for item in selected_wallets if item not in remove_list]

    run_funtions_list = []

    for wallet_key in selected_wallets:
        func = wallet_functions.get(wallet_key)
        if func:
            try:
                func()
                run_funtions_list.append(wallet_key)
            except Exception as e:
                pass

    # print('------------------------------------------------')
    # print(f'wallet_selection_processing.py: {run_funtions_list}')
    # print('------------------------------------------------')
 
    master_file = os.path.join(output_path, 'wallet_sleuth_output.csv')
    header = 'Type', 'Currency', 'Address/Transaction', 'Wallet', 'Path'

    if set(selected_wallets) == {'all_browser_wallets', 'all_desktop_wallets'}:

        wallet_functions = load_wallet_functions([
            'wallet_scripts/browser_wallets',
            'wallet_scripts/desktop_wallets'
        ])

        combined_list = []
        func_list = []

        for items in wallet_functions:
            func_list.append(items)
        
        combined_list = func_list + selected_wallets
        filtered_list = [x for x  in combined_list if x != 'all_browser_wallets']
        filtered_list_two = [x for x  in filtered_list if x != 'all_desktop_wallets']

        with open(master_file, 'w', newline='', encoding='utf-8') as master_csv:
            writer = csv.DictWriter(master_csv,fieldnames=list(header))
            writer.writeheader()
            
            for functions in filtered_list_two:
                file_name = f'{functions}_ws_output.csv'
                file_path = os.path.join(output_path, file_name)

                try:
                    with open(file_path, 'r', newline='', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            row = {key: row.get(key, '') for key in header}
                            row['Currency'] = normalize_type(row.get('Currency', ''))

                            if not row:
                                continue

                            if row == list(header):
                                continue
                                
                            writer.writerow(row)

                except Exception as e:
                    pass # this is a very lazy way to deal with functions that do not produce an output csv and it will have to do for now. i cant imagine a situation this would be a real issue though so perhaps it will stay...

    elif 'all_desktop_wallets' in selected_wallets and 'all_browser_wallets' not in selected_wallets:

        wallet_functions = load_wallet_functions([
            'wallet_scripts/desktop_wallets'
        ])

        combined_list = []
        func_list = []
        
        for items in wallet_functions:
            func_list.append(items)
        
        combined_list = func_list + selected_wallets
        filtered_list = [x for x  in combined_list if x != 'all_desktop_wallets']

        with open(master_file, 'w', newline='', encoding='utf-8') as master_csv:
            writer = csv.DictWriter(master_csv,fieldnames=list(header))
            writer.writeheader()
            
            for functions in filtered_list:
                file_name = f'{functions}_ws_output.csv'
                file_path = os.path.join(output_path, file_name)

                try:
                    with open(file_path, 'r', newline='', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            row = {key: row.get(key, '') for key in header}
                            row['Currency'] = normalize_type(row.get('Currency', ''))

                            if not row:
                                continue

                            if row == list(header):
                                continue
                                
                            writer.writerow(row)

                except Exception as e:
                    pass

    elif 'all_browser_wallets' in selected_wallets and 'all_desktop_wallets' not in selected_wallets:

        wallet_functions = load_wallet_functions([
            'wallet_scripts/browser_wallets'
        ])

        combined_list = []
        func_list = []

        for items in wallet_functions:
            func_list.append(items)
        
        combined_list = func_list + selected_wallets
        filtered_list = [x for x  in combined_list if x != 'all_browser_wallets']

        with open(master_file, 'w', newline='', encoding='utf-8') as master_csv:
            writer = csv.DictWriter(master_csv,fieldnames=list(header))
            writer.writeheader()
            
            for functions in filtered_list:
                file_name = f'{functions}_ws_output.csv'
                file_path = os.path.join(output_path, file_name)

                try:
                    with open(file_path, 'r', newline='', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            row = {key: row.get(key, '') for key in header}
                            row['Currency'] = normalize_type(row.get('Currency', ''))

                            if not row:
                                continue

                            if row == list(header):
                                continue
                                
                            writer.writerow(row)

                except Exception as e:
                    pass

    elif 'all_desktop_wallets' not in selected_wallets or 'all_browser_wallets' not in selected_wallets:

        with open(master_file, 'w', newline='', encoding='utf-8') as master_csv:
            writer = csv.DictWriter(master_csv,fieldnames=list(header))
            writer.writeheader()
            
            for functions in run_funtions_list:
                file_name = f'{functions}_ws_output.csv'
                file_path = os.path.join(output_path, file_name)

                try:
                    with open(file_path, 'r', newline='', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            row = {key: row.get(key, '') for key in header}
                            row['Currency'] = normalize_type(row.get('Currency', ''))

                            if not row:
                                continue

                            if row == list(header):
                                continue
                                
                            writer.writerow(row)

                except Exception as e:
                    pass
    
    return jsonify({'status': 'executed'})