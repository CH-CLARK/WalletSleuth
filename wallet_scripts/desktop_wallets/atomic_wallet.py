#generic imports
import csv
import json
import os
import inspect

# controller imports
import controller.config
from controller.utils.wallet_utils import extract_leveldb_data


def atomic_wallet():
    appdata_dir = controller.config.APPDATA
    output_dir = controller.config.OUTPUT
    log_name = controller.config.WS_MAIN_LOG_NAME

    function_name = inspect.currentframe().f_code.co_name
    wallet_name = function_name.split('_')[0].capitalize()

    data_location = '/Roaming/atomic/Local Storage/leveldb'

    csv_data, location = extract_leveldb_data(appdata_dir, data_location)

    result = []

    col_keyhex = [x[0] for x in csv_data]
    col_valuetext = [x[2] for x in csv_data]

    addresses_hex = "5f 66 69 6c 65 3a 2f 2f 00 01 61 64 64 72 65 73 73 65 73"
    if addresses_hex in col_keyhex:
        index_addresses = col_keyhex.index(addresses_hex)
        index_valuetext = col_valuetext[index_addresses]
        stripped_index_valuetext = index_valuetext[1:]

        json_obj = json.loads(stripped_index_valuetext)
    
    try:
        # Process json_obj data specific to Atomic Wallet
        for i in json_obj:
            if i["address"] != "":
                address_output = ['Address', i["id"], i["address"], wallet_name + ' Wallet', location]
                result.append(address_output)
    except:
        pass

    if result:
        with open(f'{output_dir}/{wallet_name.lower()}_wallet_output.csv', 'w', newline='') as result_output:
            write = csv.writer(result_output, escapechar='\\')
            write.writerows(result)
        
        with open(f'{output_dir}/{log_name}', 'a') as log_file:
            log_file.write(f'ACTION: {wallet_name} Wallet - Addresses Identified.\n')

    if not result:
        with open(f'{output_dir}/{log_name}', 'a') as log_file:
            log_file.write(f'ACTION: {wallet_name} Wallet - No Addresses Identified.\n')