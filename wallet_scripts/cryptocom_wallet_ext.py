#generic imports
import json
import os
import csv

#controller imports
import controller.config

#CCL imports
import ccl_chrome_ldb_scripts.ccl_chromium_indexeddb

def cryptocom_wallet_chrome():
    appdata_dir = controller.config.APPDATA
    output_dir = controller.config.OUTPUT
    log_name = controller.config.WS_MAIN_LOG_NAME


    chrome_user_data = appdata_dir + "/Local/Google/Chrome/User Data"
    folders_list = os.listdir(chrome_user_data)

    #Checking profiles locations
    profiles_check = "Profile"
    profiles_list = [idx for idx in folders_list if idx.lower().startswith(profiles_check.lower())]
    profiles_list_len = len(profiles_list)

    #Checking default location
    default_check = "Default"
    default_list = [idx for idx in folders_list if idx.lower().startswith(default_check.lower())]

    #makes the names more human readable - might look at implementing this over the output file.
    replacement_dict = {
        'BTC_P2PKH': 'btc',
        'BTC_P2WPKH': 'btc',
        'BTC_P2TR': 'btc',
        'BTC_P2SH_P2WPKH': 'btc',
        'BTC_M44_P2WPKH': 'btc',
        'BTC_M44_P2TR': 'btc',
        'TON_V4R2_NONBOUNCEABLE': 'ton',
        'TON_V4R2_BOUNCEABLE': 'ton'
    }

    #this removes testnet addresses from the output
    remove_dict = {
        'tBTC_P2PKH',
        'tBTC_P2WPKH',
        'tBTC_P2TR',
        'tBTC_P2SH_P2WPKH',
        'tBTC_M44_P2WPKH',
        'tBTC_M44_P2TR',
        'tTON_V4R2_BOUNCEABLE',
        'tTON_V4R2_NONBOUNCEABLE'
    }

    addresses = []

    if default_list:
        try:
            ldb_path = appdata_dir + '/Local/Google/Chrome/User Data/Default/IndexedDB/chrome-extension_hifafgmccdpekplomjjkcfgodnhcellj_0.indexeddb.leveldb'
            wrapper = ccl_chrome_ldb_scripts.ccl_chromium_indexeddb.WrappedIndexDB(ldb_path)
        except Exception as e:
            pass

        try:
            for db_info in wrapper.database_ids:
                db = wrapper[db_info.dbid_no]
                for obj_store_name in db.object_store_names:
                    if obj_store_name == 'wallets':
                        obj_store = db[obj_store_name]
                        records = list(obj_store.iterate_records())

                        if records:
                            for record in records:
                                display_name = record.value.get('addresses')

                                for key, value in display_name.items():
                                    test_var = 'Address', key, value['address'], 'Crypto.com Wallet', ldb_path
                                    addresses.append(test_var)
               
                        else:
                            pass

            updated_list = [tuple(replacement_dict.get(item, item) for item in sublist) for sublist in addresses]
 
            filtered_list = [sublist for sublist in updated_list if not any(item in remove_dict for item in sublist)]

        except:
            pass

        with open(output_dir + '/' 'crypto.com_wallet^_chrome_addresses.csv', 'w', newline='') as file:
            write = csv.writer(file) 
            write.writerows(filtered_list)


    if not addresses:
        with open(output_dir + '/' + log_name, 'a') as log_file:
            log_file.write('ACTION: Crypto.com Wallet (Chrome) - No Addresses Identified!\n')


    if addresses:
        with open(output_dir + '/' + log_name, 'a') as log_file:
            log_file.write('ACTION: Crypto.com Wallet (Chrome) - Addresses Identified.\n')