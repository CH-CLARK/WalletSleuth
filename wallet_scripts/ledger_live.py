#generic imports
import csv
import json
import os
import sys

#controller imports
import controller.config

#CCL Imports
import ccl_chrome_ldb_scripts.ccl_leveldb


def ledger_live_wallet():

    ledgerlive_output = []
    appdata_dir = controller.config.APPDATA
    output_dir = controller.config.OUTPUT

    ledger_app_data = appdata_dir + "/Roaming/Ledger Live/app.json"

    with open(ledger_app_data, 'r') as file:
        read_data = file.read()
        
        json_obj = json.loads(read_data)
        data_obj = json_obj['data']
        accounts_obj = data_obj['accounts']

    for keys in accounts_obj:
        accounts_data_obj = keys['data']

        try:
            bit_resources = accounts_data_obj['bitcoinResources']
            walletAccount_obj = bit_resources['walletAccount']
            params_obj = walletAccount_obj['params']
            xpub_obj = walletAccount_obj['xpub']
            xpub_data_obj = xpub_obj['data']
            addycache = xpub_data_obj['addressCache']

            xpub_addy = 'Extended Public Key (XPUB)', params_obj['currency'], params_obj['xpub'], 'Ledger Live', ledger_app_data
            ledgerlive_output.append(xpub_addy)
            
            for k, v in addycache.items():
                other_addys = 'Address', params_obj['currency'], v, 'Ledger Live', ledger_app_data
                ledgerlive_output.append(other_addys)

        except Exception as e:
            pass

        try:
            fresh_addresses = accounts_data_obj['freshAddress']
            currency_id = accounts_data_obj['currencyId']
            if '0x' in fresh_addresses:
                eth_type_addy = 'Address', currency_id, fresh_addresses, 'Ledger Live', ledger_app_data
                ledgerlive_output.append(eth_type_addy)

        except Exception as e:
            pass

    with open(output_dir + '/' + 'ledger_live_addresses.csv', 'w', newline='') as output_file:
        write = csv.writer(output_file)
        write.writerows(ledgerlive_output)
        
    with open(output_dir + '/' + 'WalletSleuth_log.txt', 'a') as log_file:
        log_file.write('ACTION: Ledger Live Wallet - Addresses Identified.\n')            
