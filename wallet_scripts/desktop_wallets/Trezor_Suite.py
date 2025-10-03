SUPPORTED_OPERATING_SYSTEMS = ['Windows', 'Mac']
SUPPORTED_BROWSERS = None
DEPENDENCIES = None
WALLET_METADATA = {
    'name': 'Trezor Suite',
    'description': '''Trezor Suite is a non-custodial desktop application for interacting with Trezor hardware wallets. 
                    Trezor supports a variety of cryptocurrencies and tokens, using the Trezor Suite platform a user is able to easily send and recieve cryptocurrency.''',
    'websites': ['trezor.io'],
    'ext_id': None,
    'author': ['CH-CLARK'],
    'plugin-iteration': '1',
    'plugin-last-update':'2025-09-29'
}

def trezor_suite():
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
        data_location = "/Roaming/@trezor/suite-desktop/IndexedDB/file__0.indexeddb.leveldb/"

    if operating_system == 'mac':
        user_data_subdir = "/Library"
        directory_path = directory_path + user_data_subdir
        data_location = "/Application Support/@trezor/suite-desktop/IndexedDB/file__0.indexeddb.leveldb/"

    function_name = inspect.currentframe().f_code.co_name

    identified_paths = []
    files_list = []
    txid_result = []
    zpub_result = []


    if os.path.exists(directory_path + data_location):
        identified_paths.append(data_location)

        for files in os.listdir(directory_path + data_location):
            if files.endswith('.ldb'):
                files_list.append(files)
            if files.endswith('.log'):
                files_list.append(files)
    try:
        for log_file in files_list:
            log_file_path = f'{directory_path + data_location}{log_file}'

            with open(f'{log_file_path}', 'rb') as file:
                
                contents = file.read()
                hex_content = contents.hex()

                txid_hex = '7379'
                end_txid_hex = '220368'

                start_index = 0
                txid_dump = []
                
                while True:
                    index = hex_content.find(txid_hex, start_index)
                    if index == -1:
                        break
                    
                    end_index = hex_content.find(end_txid_hex, index + len(txid_hex))
                    if end_index == -1:
                        break

                    extracted_hex = hex_content[index + len(txid_hex):end_index]

                    try:
                        extracted_text = bytes.fromhex(extracted_hex).decode('utf-8', errors='ignore')

                        if len(extracted_text) == 93:
                            txid_dump.append(extracted_text)
                            
                    except:
                        pass          

                    start_index = end_index + len(end_txid_hex)

        for items in txid_dump:
            output_string = 'Transaction ID', items[6:9],  items[29:], 'Trezor Suite', log_file_path.replace("\\","/")
            txid_result.append(output_string)
        txid_result = list(set(txid_result))

    except Exception as e:
        pass
    

    try:
        for log_file in files_list:
            log_file_path = f'{directory_path + data_location}{log_file}'

            with open(f'{log_file_path}', 'rb') as file:
                    
                contents = file.read()
                hex_content = contents.hex()

                start_hex = '65736372'
                end_hex = '7479'

                start_index = 0
                zpub_dump = []

                while True:
                    index = hex_content.find(start_hex, start_index)
                    if index == -1:
                        break

                    end_index = hex_content.find(end_hex, index + len(start_hex))
                    if end_index == -1:
                        break

                    extracted_hex = hex_content[index + len(start_hex):end_index]

                    try:
                        extracted_text = bytes.fromhex(extracted_hex).decode('utf-8', errors='ignore')

                        if len(extracted_text) == 209:
                            zpub_dump.append(extracted_text)
                    
                        zpub_dump = list(set(zpub_dump))

                    except:
                        pass

                    start_index = end_index + len(end_hex)
            
            for items in zpub_dump:
                output_string = 'Extended Public Key (ZPUB)', items[204:207], items[7:118], 'Trezor Suite', log_file_path.replace("\\","/")
                zpub_result.append(output_string)


    except Exception as e:
        pass

    if not identified_paths:
        with open(logging_output, 'a') as log_file:
            log_file.write(f'\nERROR: Trezor Suite - Wallet not found!')

    if zpub_result:
        header = 'Type', 'Currency', 'Address/Transaction', 'Wallet', 'Path'
        output_file = f'{function_name}_ws_output.csv'
        wallet_output_path = os.path.join(output_path, output_file)
    
        with open(wallet_output_path, 'w', newline='') as result_output:
            write = csv.writer(result_output, escapechar='*')
            write.writerow(header)
            write.writerows(zpub_result)

        with open(logging_output, 'a') as log_file:
            log_file.write(f"\nACTION: {WALLET_METADATA.get('name')} - Addresses identified.")

    if identified_paths and not zpub_result:
        with open(logging_output, 'a') as log_file:
            log_file.write(f"\nACTION: {WALLET_METADATA.get('name')} - No addresses identified.")

    if txid_result:
        output_file = f'{function_name}_ws_output.csv'
        wallet_output_path = os.path.join(output_path, output_file)
    
        with open(wallet_output_path, 'a', newline='') as result_output:
            write = csv.writer(result_output, escapechar='*')
            write.writerows(txid_result)

        with open(logging_output, 'a') as log_file:
            log_file.write(f"\nACTION: {WALLET_METADATA.get('name')} - Transactions identified.")

    if identified_paths and not zpub_result:
        with open(logging_output, 'a') as log_file:
            log_file.write(f"\nACTION: {WALLET_METADATA.get('name')} - No transactions identified.")