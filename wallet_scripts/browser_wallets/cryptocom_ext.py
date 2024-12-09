#generic imports
import json
import os
import csv
import inspect

#controller imports
import controller.config
from controller.utils.wallet_utils import browser_dict

#ccl imports
from ccl_scripts.ccl_chromium_reader import ccl_chromium_indexeddb


wallet_name = 'Crypto.com'
ext_id = 'hifafgmccdpekplomjjkcfgodnhcellj'

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


def cryptocom_brave():
    appdata_dir = controller.config.APPDATA
    output_dir = controller.config.OUTPUT
    log_name = controller.config.WS_MAIN_LOG_NAME

    function_name = inspect.currentframe().f_code.co_name
    browser_name = function_name.split('_')[-1].capitalize()
    browser_path = browser_dict.get(browser_name)
    wallet_browser = f'{wallet_name} ({browser_name})'

    folders_list = os.listdir(f'{appdata_dir}{browser_path}')

    result = []

    #Checking profiles locations
    profiles_check = "Profile"
    profiles_list = [idx for idx in folders_list if idx.lower().startswith(profiles_check.lower())]
    profiles_list_len = len(profiles_list)
    
    #Checking default location
    default_check = "Default"
    default_list = [idx for idx in folders_list if idx.lower().startswith(default_check.lower())]

    addresses = []

    if profiles_list:
        for x in range(profiles_list_len):
            try:
                data_location = appdata_dir + browser_path + "/" + profiles_list[x] + "/IndexedDB/chrome-extension_" + ext_id + "_0.indexeddb.leveldb"
                wrapper = ccl_chromium_indexeddb.WrappedIndexDB(data_location)
            
            except:
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
                                        address_output = 'Address', key, value['address'], wallet_browser, data_location
                                        addresses.append(address_output)
                
                            else:
                                pass

                updated_list = [tuple(replacement_dict.get(item, item) for item in sublist) for sublist in addresses]            
                result = [sublist for sublist in updated_list if not any(item in remove_dict for item in sublist)]

            except:
                pass


    if default_list:
        try:
            data_location = appdata_dir + browser_path + "/" + profiles_list[x] + "/IndexedDB/chrome-extension_" + ext_id + "_0.indexeddb.leveldb"
            wrapper = ccl_chromium_indexeddb.WrappedIndexDB(data_location)
        
        except:
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
                                    address_output = 'Address', key, value['address'], wallet_browser, data_location
                                    addresses.append(address_output)
            
                        else:
                            pass

            updated_list = [tuple(replacement_dict.get(item, item) for item in sublist) for sublist in addresses]            
            result = [sublist for sublist in updated_list if not any(item in remove_dict for item in sublist)]

        except:
            pass

    if result:
        with open(f'{output_dir}/{wallet_name.lower()}^_{browser_name.lower()}_output.csv', 'w', newline='') as result_output:
            write = csv.writer(result_output, escapechar='\\')
            write.writerows(result)

        with open(f'{output_dir}/{log_name}', 'a') as log_file:
            log_file.write(f'ACTION: {wallet_browser} - Addresses Identified.\n')

    if not result:
        with open(f'{output_dir}/{log_name}', 'a') as log_file:
            log_file.write(f'ACTION: {wallet_browser} - No Addresses Identified.\n')


def cryptocom_chrome():
    appdata_dir = controller.config.APPDATA
    output_dir = controller.config.OUTPUT
    log_name = controller.config.WS_MAIN_LOG_NAME

    function_name = inspect.currentframe().f_code.co_name
    browser_name = function_name.split('_')[-1].capitalize()
    browser_path = browser_dict.get(browser_name)
    wallet_browser = f'{wallet_name} ({browser_name})'

    folders_list = os.listdir(f'{appdata_dir}{browser_path}')

    result = []

    #Checking profiles locations
    profiles_check = "Profile"
    profiles_list = [idx for idx in folders_list if idx.lower().startswith(profiles_check.lower())]
    profiles_list_len = len(profiles_list)
    
    #Checking default location
    default_check = "Default"
    default_list = [idx for idx in folders_list if idx.lower().startswith(default_check.lower())]

    addresses = []

    if profiles_list:
        for x in range(profiles_list_len):
            try:
                data_location = appdata_dir + browser_path + "/" + profiles_list[x] + "/IndexedDB/chrome-extension_" + ext_id + "_0.indexeddb.leveldb"
                wrapper = ccl_chromium_indexeddb.WrappedIndexDB(data_location)
            
            except:
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
                                        address_output = 'Address', key, value['address'], wallet_browser, data_location
                                        addresses.append(address_output)
                
                            else:
                                pass

                updated_list = [tuple(replacement_dict.get(item, item) for item in sublist) for sublist in addresses]            
                result = [sublist for sublist in updated_list if not any(item in remove_dict for item in sublist)]

            except:
                pass


    if default_list:
        try:
            data_location = appdata_dir + browser_path + "/" + profiles_list[x] + "/IndexedDB/chrome-extension_" + ext_id + "_0.indexeddb.leveldb"
            wrapper = ccl_chromium_indexeddb.WrappedIndexDB(data_location)
        
        except:
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
                                    address_output = 'Address', key, value['address'], wallet_browser, data_location
                                    addresses.append(address_output)
            
                        else:
                            pass

            updated_list = [tuple(replacement_dict.get(item, item) for item in sublist) for sublist in addresses]            
            result = [sublist for sublist in updated_list if not any(item in remove_dict for item in sublist)]

        except:
            pass

    if result:
        with open(f'{output_dir}/{wallet_name.lower()}^_{browser_name.lower()}_output.csv', 'w', newline='') as result_output:
            write = csv.writer(result_output, escapechar='\\')
            write.writerows(result)

        with open(f'{output_dir}/{log_name}', 'a') as log_file:
            log_file.write(f'ACTION: {wallet_browser} - Addresses Identified.\n')

    if not result:
        with open(f'{output_dir}/{log_name}', 'a') as log_file:
            log_file.write(f'ACTION: {wallet_browser} - No Addresses Identified.\n')