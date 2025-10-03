SUPPORTED_OPERATING_SYSTEMS = ['Windows', 'Mac']
SUPPORTED_BROWSERS = None
DEPENDENCIES = None
WALLET_METADATA = {
    'name': 'Atomic Wallet',
    'description': 'Atomic wallet is a non-custodial desktop wallet that supports various cryptocurrencies and tokens. Users are able to easily send and recieve cryptocurrency using the platform.',
    'websites': ['atomicwallet.io'],
    'ext_id': None,
    'author': ['CH-CLARK'],
    'plugin-iteration': '1',
    'plugin-last-update':'2025-09-29'
}

def atomic_wallet():
    try:
        from routes.config import configuration
        from utils.wallet_utils import extract_leveldb_data

        import inspect
        import os
        import json
        import csv
    
    except ImportError as e:
        import_catch = f'ERROR: Atomic Wallet - {e} identified! Execution aborted!'
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
        data_location = "/Roaming/atomic/Local Storage/leveldb"

    if operating_system == 'mac':
        user_data_subdir = "/Library"
        directory_path = directory_path + user_data_subdir
        data_location = "/Application Support/atomic/Local Storage/leveldb"

    function_name = inspect.currentframe().f_code.co_name

    result = []
    identified_paths = []

    if os.path.exists(directory_path + data_location):
        identified_paths.append(data_location)
        try:
            csv_data, location = extract_leveldb_data(directory_path, data_location)

            addresses_hex = "5f 66 69 6c 65 3a 2f 2f 00 01 61 64 64 72 65 73 73 65 73"

            col_keyhex = [x[0] for x in csv_data]
            col_valuetext = [x[2] for x in csv_data]

            if addresses_hex in col_keyhex:
                index_addresses = col_keyhex.index(addresses_hex)
                index_valuetext = col_valuetext[index_addresses]
                stripped_index_valuetext = index_valuetext[1:]

                json_obj = json.loads(stripped_index_valuetext)


            for i in json_obj:
                if i["address"] != "":
                    address_output = ['Address', i["id"], i["address"], 'Atomic Wallet', location.replace("\\","/")]
                    result.append(address_output)  

        except Exception as e:
            pass

    if not identified_paths:
        with open(logging_output, 'a') as log_file:
            log_file.write(f'\nERROR: Atomic Wallet - Wallet not found!')

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