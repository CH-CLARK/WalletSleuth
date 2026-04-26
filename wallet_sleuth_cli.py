# generic imports
import argparse
import os
import csv

#wallet sleuth imports
from wallet_sleuth import title
from utils.user_config import configuration
from utils.pyinstaller_utils import resource_path
from utils.wallet_utils import normalize_type
from model.load_wallets import load_wallet_functions
from wallet_scripts.desktop_wallets.All_Desktop_Wallets import all_desktop_wallets

def main():
    print(title)

    parser = argparse.ArgumentParser(prog='wallet_sleuth_cli.py')

    parser.add_argument('-p',
                         metavar='PROFILE_PATH', 
                         required=True, 
                         help='User profile directory path')
    
    parser.add_argument('-o', 
                        metavar='OUTPUT_PATH', 
                        required=True, 
                        help='Output directory path')
                        
    parser.add_argument('-os', 
                        metavar='OS', 
                        required=True, 
                        choices=['WIN', 'MAC'], 
                        help='Operating system: WIN or MAC')

    parser.add_argument('--desktop_wallets', 
                        action='store_true', 
                        help='Run all desktop wallet scripts')
    
    parser.add_argument('--browser_wallets', 
                        action='store_true', 
                        help='Run all browser wallet scripts')
    
    parser.add_argument('--all_wallets', 
                        action='store_true', 
                        help='Run all wallet scripts')

    args = parser.parse_args()

    profile_path = args.p
    output_path = args.o
    os_selection = 'windows' if args.os == 'WIN' else 'mac'
    desktop_wallets = args.desktop_wallets
    browser_wallets = args.browser_wallets
    all_wallets = args.all_wallets
 
    configuration.DIRECTORY_PATH = profile_path
    configuration.OUTPUT_PATH = output_path
    configuration.OS_SELECTION = os_selection

    print('Wallet Sleuth - Scan Settings')
    print('======================================')
    print(f'User Directory: {configuration.DIRECTORY_PATH}')
    print(f'Output Directory: {configuration.OUTPUT_PATH}')
    print(f'Operating System: {configuration.OS_SELECTION}')
    print('======================================')


    #run wallet_scripts
    func_list = []
    header = 'Type', 'Currency', 'Address/Transaction', 'Wallet', 'Path'

    if desktop_wallets:
        all_desktop_wallets()
        wallet_functions = load_wallet_functions([resource_path('wallet_scripts/desktop_wallets')])
        func_list = [i for i in wallet_functions if i != 'all_desktop_wallets']

    elif browser_wallets:
        print('this will do browser wallets')

    elif(all_wallets):
        print('this will do all wallets')
    
    master_file = os.path.join(output_path, 'wallet_sleuth_output.csv')

    with open(master_file, 'w', newline='', encoding='utf-8') as master_csv:
        writer = csv.DictWriter(master_csv, fieldnames=list(header))
        writer.writeheader()

        for function in func_list:
            file_name = f'{function}_ws_output.csv'
            file_path = os.path.join(output_path, file_name)
            try:
                with open(file_path, 'r', newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        row = {key: row.get(key, '') for key in header}
                        row['Currency'] = normalize_type(row.get('Currency', ''))
                        if not row:
                            continue
                        writer.writerow(row)
            except Exception:
                pass

    print(f'Scan Complete!')


if __name__ == "__main__":
    main()