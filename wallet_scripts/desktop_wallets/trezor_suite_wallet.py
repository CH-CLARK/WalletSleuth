#generic imports
import os
import csv
import inspect

#controller imports
import controller.config


def trezor_suite_wallet():
    appdata_dir = controller.config.APPDATA
    output_dir = controller.config.OUTPUT
    log_name = controller.config.WS_MAIN_LOG_NAME

    function_name = inspect.currentframe().f_code.co_name
    wallet_name = function_name.replace('_', ' ').replace('wallet', '').strip().title()

    files_list = []

    txid_result = []
    zpub_result = []

    wallet_directory = f'{appdata_dir}/Roaming/@trezor/suite-desktop/IndexedDB/file__0.indexeddb.leveldb/'
    
    for files in os.listdir(wallet_directory):
        if files.endswith('.ldb'):
            files_list.append(files)
        if files.endswith('.log'):
            files_list.append(files)

    for log_file in files_list:
        data_location = f'{wallet_directory}{log_file}'

        with open(f'{data_location}', 'rb') as file:
            
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
        output_string = 'Transaction ID', items[6:9],  items[29:], wallet_name, data_location
        txid_result.append(output_string)
    txid_result = list(set(txid_result))

    if txid_result:
        with open(f'{output_dir}/trezor_suite_output.csv', 'w', newline='') as result_output:
            write = csv.writer(result_output, escapechar='\\')
            write.writerows(txid_result)

        with open(f'{output_dir}/{log_name}', 'a') as log_file:
            log_file.write('ACTION: Trezor Suite Wallet - Transactions Identified.\n')  

    if not txid_result:
        with open(f'{output_dir}/{log_name}', 'a') as log_file:
            log_file.write('ACTION: Trezor Suite Wallet - No Transactions Identified.\n')


    for log_file in files_list:
        data_location = f'{wallet_directory}{log_file}'

        with open(f'{data_location}', 'rb') as file:
            
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
        output_string = 'Extended Public Key (ZPUB)', items[204:207], items[7:118], wallet_name, data_location
        zpub_result.append(output_string)

    if zpub_result:
        with open(f'{output_dir}/trezor_suite_output.csv', 'a', newline='') as result_output:
            write = csv.writer(result_output, escapechar='\\')
            write.writerows(zpub_result)

        with open(f'{output_dir}/{log_name}', 'a') as log_file:
            log_file.write('ACTION: Trezor Suite Wallet - Addresses Identified.\n')  

    if not zpub_result:
        with open(f'{output_dir}/{log_name}', 'a') as log_file:
            log_file.write('ACTION: Trezor Suite Wallet - No  Addresses Identified.\n')