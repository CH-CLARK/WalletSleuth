from wallet_sleuth import title
from routes.config import configuration
from utils.pyinstaller_utils import resource_path
from model.load_wallets import load_wallet_functions
import argparse


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
    
    # parser.add_argument('--browser_wallets', 
    #                     action='store_true', 
    #                     help='Run all browser wallet scripts')
    
    # parser.add_argument('--all_wallets', 
    #                     action='store_true', 
    #                     help='Run all wallet scripts')

    args = parser.parse_args()

    profile_path = args.p
    output_path = args.o
    os_selection = 'windows' if args.os == 'WIN' else 'mac'
    desktop_wallets = args.desktop_wallets

    #for tetsing
    # print(f'Profile Path   : {profile_path}')
    # print(f'Output Path    : {output_path}')
    # print(f'OS Selection   : {os_selection}')
    # print(f'Desktop Wallets: {desktop_wallets}')

    #recereating the config locally in the cli version
    class Config:
        OS_SELECTION = None
        DIRECTORY_PATH = None
        OUTPUT_PATH = None

    configuration = Config()
    configuration.DIRECTORY_PATH = profile_path
    configuration.OUTPUT_PATH = output_path
    configuration.OS_SELECTION = os_selection


    print('config variables')
    print('======================================')
    print(configuration.OS_SELECTION)
    print(configuration.DIRECTORY_PATH)
    print(configuration.OUTPUT_PATH)
    print('======================================')

if __name__ == "__main__":
    main()