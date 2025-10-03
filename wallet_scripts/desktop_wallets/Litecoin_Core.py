SUPPORTED_OPERATING_SYSTEMS = ['Windows', 'Mac']
SUPPORTED_BROWSERS = None
DEPENDENCIES = None
WALLET_METADATA = {
    'name': 'Litecoin Core',
    'description': 'Litecoin Core is a non-custodial desktop wallet for the Litecoin cryptocurrency. Users are able to easily send and recieve the Litecoin cryptocurrency using the platform.',
    'websites': ['bitcoin.org'],
    'ext_id': None,
    'author': ['CH-CLARK'],
    'plugin-iteration': '1',
    'plugin-last-update':'2025-09-29'
}

def litecoin_core():
    try:
        from routes.config import configuration

        import inspect
        import os
        import string
        import csv
    
    except ImportError as e:
        import_catch = f'ERROR: Litecoin Core - {e} identified! Execution aborted!'
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
        data_location = "/Roaming/Litecoin/wallets"

    if operating_system == 'mac':
        user_data_subdir = "/Library"
        directory_path = directory_path + user_data_subdir
        data_location = "/Application Support/Litecoin/wallets"

    function_name = inspect.currentframe().f_code.co_name
    special_chars = string.punctuation

    result = []
    identified_paths = []
    addresses_list = []

    if os.path.exists(directory_path + data_location):
        identified_paths.append(data_location)

        for folder_name in os.listdir(directory_path + data_location):
            folder_path = f'{directory_path + data_location}/{folder_name}'

            if os.path.isdir(folder_path):
                wallet_file = f'{folder_path}/wallet.dat'

                if os.path.isfile(wallet_file):
                    wallet_file = wallet_file.replace("\\", "/")

                    with open(wallet_file, 'rb') as file:

                        contents = file.read()
                        hex_content = contents.hex()
                        destdata_start_string = '646573746461' #searching for 'destda' strinng since i had more success in identifyign all addresses using this over 'name'
                        destdata_end_string = '037272'
                        start_index = 0

                        while True:
                            index = hex_content.find(destdata_start_string, start_index)
                            if index == -1:
                                break
                            
                            end_index = hex_content.find(destdata_end_string, index + len(destdata_start_string))
                            if end_index == -1:
                                break

                            bytes_found = bytes.fromhex(hex_content[index:end_index])
                            ascii_representation = bytes_found.decode('utf-8', errors='ignore')

                            stripped = ascii_representation[9:]

                            start_index = end_index + len(destdata_end_string)

                            if not any(char in stripped for char in special_chars):
                                output_string = 'Address','Litecoin', stripped, 'Litecoin Core', directory_path.replace("\\","/") + data_location.replace("\\","/")

                                addresses_list.append(output_string)
                                for i in addresses_list:
                                    if i not in result:
                                        result.append(i)

    if not identified_paths:
        with open(logging_output, 'a') as log_file:
            log_file.write(f'\nERROR: Bitcoin Core - Wallet not found!')

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