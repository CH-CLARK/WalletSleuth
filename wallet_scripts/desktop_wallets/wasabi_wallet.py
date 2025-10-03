SUPPORTED_OPERATING_SYSTEMS = ['Windows', 'Mac']
SUPPORTED_BROWSERS = None
DEPENDENCIES = None
WALLET_METADATA = {
    'name': 'Wasabi Wallet',
    'description': 'Wasabi Wallet is a privacy focused non-custodial desktop wallet for the Bitcoin cryptocurrency. Users are able to easily send and recieve cryptocurrency using the platform.',
    'websites': ['wasabiwallet.io'],
    'ext_id': None,
    'author': ['CH-CLARK'],
    'plugin-iteration': '1',
    'plugin-last-update':'2025-09-29'
}

def wasabi_wallet():
    try:
        from routes.config import configuration

        import inspect
        import os
        import json
        import csv
    
    except ImportError as e:
        import_catch = f'ERROR: Wasabi Wallet - {e} identified! Execution aborted!'
        pass

    # user set varibless
    operating_system = configuration.OS_SELECTION
    directory_path = configuration.DIRECTORY_PATH
    output_path = configuration.OUTPUT_PATH

    logging_output = os.path.join(output_path, 'wallet_sleuth_logging.txt')

    try:
        if import_catch:
            with open(logging_output, 'a') as log_file:
                log_file.write(f'\n{import_catch}')
            return
    except:
        pass

    if operating_system == 'windows':
        user_data_subdir = "/AppData"
        directory_path = directory_path + user_data_subdir
        data_location = "/Roaming/WalletWasabi/Client/Wallets"

    if operating_system == 'mac':
        user_data_subdir = "/Library"
        directory_path = directory_path + user_data_subdir
        data_location = "/Application Support/WalletWasabi/Client/Wallets"

    function_name = inspect.currentframe().f_code.co_name

    result = []
    identified_paths = []

    if os.path.exists(directory_path + data_location):
        identified_paths.append(directory_path + data_location)

        for files in os.listdir(directory_path + data_location):
            all_locations = directory_path + data_location + '/' + files

            with open(all_locations, 'r') as f:
                read_files = f.read()
                strip_first = read_files.lstrip(read_files[0:3])
                json_obj = json.loads(strip_first)
                data_obj = json_obj['ExtPubKey']

                address_output = 'Extended Public Key (XPUB)', 'Bitcoin', data_obj, 'Wasabi Wallet', all_locations.replace("\\","/")

                result.append(address_output)

    if not identified_paths:
        with open(logging_output, 'a') as log_file:
            log_file.write(f'\nERROR: Wasabi Wallet - Wallet not found!')

    if result:
        header = 'Type', 'Currency', 'Address/Transaction', 'Wallet', 'Path'
        output_file = f'{function_name}_ws_output.csv'
        wallet_output_path = os.path.join(output_path, output_file)
    
        with open(wallet_output_path, 'w', newline='') as result_output:
            write = csv.writer(result_output, escapechar='*')
            write.writerow(header)
            write.writerows(result)

        with open(logging_output, 'a') as log_file:
            log_file.write(f"\nACTION: {WALLET_METADATA.get('name')} - Addresses identified.")

    if identified_paths and not result:
        with open(logging_output, 'a') as log_file:
            log_file.write(f"\nACTION: {WALLET_METADATA.get('name')} - No addresses identified.")