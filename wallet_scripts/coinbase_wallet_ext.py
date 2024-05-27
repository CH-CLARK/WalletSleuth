#generic imports
import json
import os
import csv

#controller imports
import controller.config

#CCL imports
import ccl_chrome_ldb_scripts.ccl_chromium_indexeddb


def coinbase_wallet_chrome():
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


    addresses_list = []

    addresses = []
    valid_display_names = {'Bitcoin', 'Dogecoin', 'Ethereum', 'Litecoin', 'Solana'}

    if default_list:
        ldb_path = appdata_dir + '/Local/Google/Chrome/User Data/Default/IndexedDB/chrome-extension_hnfanknocfeofbddgcijnmhnfnkdnaad_0.indexeddb.leveldb'

        wrapper = ccl_chrome_ldb_scripts.ccl_chromium_indexeddb.WrappedIndexDB(ldb_path)
        for db_info in wrapper.database_ids:

            db = wrapper[db_info.dbid_no]
            for obj_store_name in db.object_store_names:
                if obj_store_name == 'wallet':
                    obj_store = db[obj_store_name]
                    records = list(obj_store.iterate_records())
                    if records:
                        for record in records:
                            display_name = record.value.get('displayName')
                            if display_name in valid_display_names:
                                if 'primaryAddress' in record.value:
                                    primary_address = record.value['primaryAddress']
                                    addresses.append((display_name, primary_address))
                                if 'addresses' in record.value:
                                    try:
                                        addr_list = json.loads(record.value['addresses'])
                                        for addr in addr_list:
                                            if 'address' in addr:
                                                address = addr['address']
                                                addresses.append((display_name, address))
                                    except json.JSONDecodeError:
                                        pass
                    else:
                        pass

        unique_addresses = list(dict.fromkeys(addresses))
        for display_name, address in unique_addresses:
            output_string = 'Address', display_name, address, 'Coinbase Wallet', ldb_path
            addresses_list.append(output_string)

        with open(output_dir + '/' 'coinbase_wallet_addresses.csv', 'w', newline='') as file:
            write = csv.writer(file) 
            write.writerows(addresses_list)

    if profiles_list:
        profiles_addresses_list = []

        for x in range(profiles_list_len):
            profiles_ldb_loc = appdata_dir + "/Local/Google/Chrome/User Data/" + profiles_list[x] + "/IndexedDB/chrome-extension_hnfanknocfeofbddgcijnmhnfnkdnaad_0.indexeddb.leveldb"
            
            wrapper = ccl_chrome_ldb_scripts.ccl_chromium_indexeddb.WrappedIndexDB(profiles_ldb_loc)
            for db_info in wrapper.database_ids:

                db = wrapper[db_info.dbid_no]
                for obj_store_name in db.object_store_names:
                    if obj_store_name == 'wallet':
                        obj_store = db[obj_store_name]
                        records = list(obj_store.iterate_records())
                        if records:
                            for record in records:
                                display_name = record.value.get('displayName')
                                if display_name in valid_display_names:
                                    if 'primaryAddress' in record.value:
                                        primary_address = record.value['primaryAddress']
                                        addresses.append((display_name, primary_address))
                                    if 'addresses' in record.value:
                                        try:
                                            addr_list = json.loads(record.value['addresses'])
                                            for addr in addr_list:
                                                if 'address' in addr:
                                                    address = addr['address']
                                                    addresses.append((display_name, address))
                                        except json.JSONDecodeError:
                                            pass
                        else:
                            pass

            unique_addresses = list(dict.fromkeys(addresses))
            for display_name, address in unique_addresses:
                output_string = 'Address', display_name, address, 'Coinbase Wallet', profiles_ldb_loc
                profiles_addresses_list.append(output_string)
                # print(test)

            with open(output_dir + '/' 'coinbase_wallet_addresses.csv', 'a', newline='') as file:
                write = csv.writer(file) 
                write.writerows(profiles_addresses_list)
                
                        

    with open(output_dir + '/' + log_name, 'a') as log_file:
        log_file.write('ACTION: Coinbase Wallet (Chrome) - Addresses Identified.\n')  