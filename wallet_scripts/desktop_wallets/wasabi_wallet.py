#generic imports
import csv
import json
import os
import inspect

#controller imports
import controller.config


def wasabi_wallet():
    appdata_dir = controller.config.APPDATA
    output_dir = controller.config.OUTPUT
    log_name = controller.config.WS_MAIN_LOG_NAME

    function_name = inspect.currentframe().f_code.co_name
    wallet_name = function_name.split('_')[0].capitalize()

    data_location = appdata_dir + '/Roaming/WalletWasabi/Client/Wallets'

    result = []

    for files in os.listdir(data_location):
        all_locations = data_location + '/' + files

        with open(all_locations, 'r') as f:
            read_files = f.read()
            strip_first = read_files.lstrip(read_files[0:3])
            json_obj = json.loads(strip_first)
            data_obj = json_obj['ExtPubKey']

            address_output = 'Extended Public Key (XPUB)', 'Bitcoin', data_obj, wallet_name + ' Wallet', all_locations
        
        result.append(address_output)

    
    if result:
        with open(f'{output_dir}/{wallet_name.lower()}_wallet_output.csv', 'w', newline='') as result_output:
            write = csv.writer(result_output, escapechar='\\')
            write.writerows(result)
        
        with open(f'{output_dir}/{log_name}', 'a') as log_file:
            log_file.write(f'ACTION: {wallet_name} Wallet - Addresses Identified.\n')

    if not result:
        with open(f'{output_dir}/{log_name}', 'a') as log_file:
            log_file.write(f'ACTION: {wallet_name} Wallet - No Addresses Identified.\n')