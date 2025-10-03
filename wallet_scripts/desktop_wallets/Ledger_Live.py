SUPPORTED_OPERATING_SYSTEMS = ['Windows', 'Mac']
SUPPORTED_BROWSERS = None
DEPENDENCIES = None
WALLET_METADATA = {
    'name': 'Ledger Live',
    'description': '''Ledger Live is a non-custodial desktop application for interacting with Ledger hardware wallets. 
                    Ledger supports a variety of cryptocurrencies and tokens, using the Ledger Live platform a user is able to easily send and recieve cryptocurrency.''',
    'websites': ['ledger.com'],
    'ext_id': None,
    'author': ['CH-CLARK'],
    'plugin-iteration': '1',
    'plugin-last-update':'2025-09-29'
}

def ledger_live():
    try:
        from routes.config import configuration

        import inspect
        import os
        import json
        import csv
    
    except ImportError as e:
        import_catch = f'ERROR: Ledger Live - {e} identified! Execution aborted!'
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
        data_location = "/Roaming/Ledger Live/app.json"

    if operating_system == 'mac':
        user_data_subdir = "/Library"
        directory_path = directory_path + user_data_subdir
        data_location = "/Application Support/Ledger Live/app.json"

    function_name = inspect.currentframe().f_code.co_name

    result = []
    identified_paths = []

    if os.path.exists(directory_path + data_location):
        identified_paths.append(data_location)

        with open(directory_path + data_location, 'r') as file:
            read_data = file.read()
            
            json_obj = json.loads(read_data)
            data_obj = json_obj['data']
            accounts_obj = data_obj['accounts']


        for keys in accounts_obj:
            accounts_data_obj = keys['data']

            try:
                bitcoin_resources = accounts_data_obj['bitcoinResources']
                walletAccount_obj = bitcoin_resources['walletAccount']
                params_obj = walletAccount_obj['params']
                xpub_obj = walletAccount_obj['xpub']
                xpub_data_obj = xpub_obj['data']
                address_cache = xpub_data_obj['addressCache']

                xpub_addresses = 'Extended Public Key (XPUB)', params_obj['currency'], params_obj['xpub'], 'Ledger Live', directory_path.replace("\\","/") + data_location.replace("\\","/")
                result.append(xpub_addresses)
                
                for k, v in address_cache.items():
                    other_addresses = 'Address', params_obj['currency'], v, 'Ledger Live', directory_path.replace("\\","/") + data_location.replace("\\","/")
                    result.append(other_addresses)

            except Exception as e:
                print(e)
                pass

        try:
            fresh_addresses = accounts_data_obj['freshAddress']
            currency_id = accounts_data_obj['currencyId']
            if '0x' in fresh_addresses:
                eth_type_addresses = 'Address', currency_id, fresh_addresses, 'Ledger Live', directory_path.replace("\\","/") + data_location.replace("\\","/")
                result.append(eth_type_addresses)

        except Exception as e:
            pass


    if not identified_paths:
        with open(logging_output, 'a') as log_file:
            log_file.write(f'\nERROR: Ledger Live - Wallet not found!')

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