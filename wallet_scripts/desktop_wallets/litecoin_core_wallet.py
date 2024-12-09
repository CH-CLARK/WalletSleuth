#generic imports
import os
import csv
import string

#controller imports
import controller.config


def litecoin_core_wallet():
    appdata_dir = controller.config.APPDATA
    output_dir = controller.config.OUTPUT
    log_name = controller.config.WS_MAIN_LOG_NAME

    special_chars = string.punctuation

    addresses_list = []
    result = []

    wallet_directory = f'{appdata_dir}/Roaming/Litecoin/wallets'
    
    for folder_name in os.listdir(wallet_directory):
        folder_path = f'{wallet_directory}/{folder_name}'

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
                            output_string = 'Address','Litecoin', stripped,'Litecoin Core', wallet_file

                            addresses_list.append(output_string)
                            for i in addresses_list:
                                if i not in result:
                                    result.append(i)
    
    if result:
        with open(f'{output_dir}/Litecoin_core_output.csv', 'w', newline='') as result_output:
            write = csv.writer(result_output, escapechar='\\')
            write.writerows(result)

        with open(f'{output_dir}/{log_name}', 'a') as log_file:
            log_file.write('ACTION: Litecoin Core Wallet - Addresses Identified.\n')  

    if not result:
        with open(f'{output_dir}/{log_name}', 'a') as log_file:
            log_file.write('ACTION: Litecoin Core Wallet - No Addresses Identified.\n')