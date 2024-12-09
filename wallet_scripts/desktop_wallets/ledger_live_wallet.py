#generic imports
import csv
import json
import os
import sys
import inspect

#controller imports
import controller.config


def ledger_live_wallet():
    appdata_dir = controller.config.APPDATA
    output_dir = controller.config.OUTPUT
    log_name = controller.config.WS_MAIN_LOG_NAME

    function_name = inspect.currentframe().f_code.co_name
    wallet_name = function_name.replace('_', ' ').replace('wallet', '').strip().title()
    alt_wallet_name = function_name.replace('_wallet', '')

    data_location = appdata_dir + "/Roaming/Ledger Live/app.json"

    result = []

    with open(data_location, 'r') as file:
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

            xpub_addresses = 'Extended Public Key (XPUB)', params_obj['currency'], params_obj['xpub'], wallet_name, data_location
            result.append(xpub_addresses)
            
            for k, v in address_cache.items():
                other_addresses = 'Address', params_obj['currency'], v, wallet_name, data_location
                result.append(other_addresses)

        except Exception as e:
            pass

        try:
            fresh_addresses = accounts_data_obj['freshAddress']
            currency_id = accounts_data_obj['currencyId']
            if '0x' in fresh_addresses:
                eth_type_addresses = 'Address', currency_id, fresh_addresses, wallet_name, data_location
                result.append(eth_type_addresses)

        except Exception as e:
            pass


    if result:
        with open(f'{output_dir}/{alt_wallet_name}_output.csv', 'w', newline='') as result_output:
            write = csv.writer(result_output, escapechar='\\')
            write.writerows(result)
        
        with open(f'{output_dir}/{log_name}', 'a') as log_file:
            log_file.write(f'ACTION: {wallet_name} Wallet - Addresses Identified.\n')

    if not result:
        with open(f'{output_dir}/{log_name}', 'a') as log_file:
            log_file.write(f'ACTION: {wallet_name} Wallet - No Addresses Identified.\n')