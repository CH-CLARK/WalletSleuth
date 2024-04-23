import csv
import os

import controller.config

def litecoin_core_wallet():

    litecoin_core_output = []

    appdata_dir = controller.config.APPDATA
    output_dir = controller.config.OUTPUT

    litecoin_app_data = appdata_dir + "/Roaming/Litecoin/wallets"

    try:
        for folder_name in os.listdir(litecoin_app_data):
            folder_path = os.path.join(litecoin_app_data, folder_name)
            
            if os.path.isdir(folder_path):
                wallet_file = os.path.join(folder_path, 'wallet.dat')
                if os.path.isfile(wallet_file):
                    wallet_file = wallet_file.replace("\\", "/")


                    with open(wallet_file, 'rb') as file:
                        contents = file.read()
                        hex_content = contents.hex()
                        search_hex_string = '646573746461'
                        end_hex_string = '037272'

                        start_index = 0

                        while True:
                            index = hex_content.find(search_hex_string, start_index)
                            if index == -1:
                                break

                            end_index = hex_content.find(end_hex_string, index + len(search_hex_string))
                            if end_index == -1:
                                break
                            
                            bytes_found = bytes.fromhex(hex_content[index:end_index])
                            ascii_representation = bytes_found.decode('utf-8', errors='ignore')

                            
                            stripped = ascii_representation[9:]
                            output = 'Address', 'Litecoin', stripped, 'Litecoin Core', wallet_file
                            litecoin_core_output.append(output)
                                        
                            start_index = end_index + len(end_hex_string)

        with open(output_dir + '/' + 'litecoin_core_addresses.csv', 'w', newline='') as output_file:
            write= csv.writer(output_file)
            write.writerows(litecoin_core_output)

        with open(output_dir + '/' + 'WalletSleuth_log.txt', 'a') as log_file:
            log_file.write('ACTION: Litecoin Core Wallet - Addresses Identified.\n')            

                
    except Exception:
        pass

