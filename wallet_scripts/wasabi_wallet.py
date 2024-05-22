#generic imports
import csv
import json
import os
import sys

#controller imports
import controller.config

def wasabi_wallet():

    wasabi_output = []

    appdata_dir = controller.config.APPDATA
    output_dir = controller.config.OUTPUT
    log_name = controller.config.WS_MAIN_LOG_NAME

    wasabi_wallets_loc = appdata_dir + "/Roaming/WalletWasabi/Client/Wallets"
    try:
        for files in os.listdir(wasabi_wallets_loc):
            all_locations = wasabi_wallets_loc + '/' + files

            with open(all_locations, 'r') as f:
                read_files = f.read()
                strip_first = read_files.lstrip(read_files[0:3])
                json_obj = json.loads(strip_first)
                data_obj = json_obj['ExtPubKey']

                output = 'Extended Public Key (XPUB)', 'Bitcoin', data_obj, 'Wasabi Wallet', all_locations
            wasabi_output.append(output)

        with open(output_dir + '/' + 'wasabi_wallet_addresses.csv', 'w', newline='') as output_file:
            write = csv.writer(output_file)
            write.writerows(wasabi_output)
        
        with open(output_dir + '/' + log_name, 'a') as log_file:
            log_file.write('ACTION: Wasabi Wallet - Addresses Identified.\n')    

    except Exception as e:
        pass