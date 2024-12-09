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


wallet_name = 'Coinbase'
ext_id = 'hnfanknocfeofbddgcijnmhnfnkdnaad'

valid_display_names = {'Bitcoin', 'Dogecoin', 'Ethereum', 'Litecoin', 'Solana'}


def coinbase_brave():
    appdata_dir = controller.config.APPDATA
    output_dir = controller.config.OUTPUT
    log_name = controller.config.WS_MAIN_LOG_NAME

    function_name = inspect.currentframe().f_code.co_name
    browser_name = function_name.split('_')[-1].capitalize()
    browser_path = browser_dict.get(browser_name)
    wallet_browser = f'{wallet_name} ({browser_name})'

    folders_list = os.listdir(f'{appdata_dir}{browser_path}')

    addresses = []
    result = []

    profiles_check = "Profile"
    profiles_list = [idx for idx in folders_list if idx.lower().startswith(profiles_check.lower())]
    profiles_list_len = len(profiles_list)
    
    default_check = "Default"
    default_list = [idx for idx in folders_list if idx.lower().startswith(default_check.lower())]

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
                address_output = 'Address', display_name, address, wallet_browser, data_location
                result.append(address_output)

        except:
            pass

    if default_list:
        try:
            data_location = appdata_dir + browser_path + "/Default/IndexedDB/chrome-extension_" + ext_id + "_0.indexeddb.leveldb"

            wrapper = ccl_chromium_indexeddb.WrappedIndexDB(data_location)
        
        except:
            pass

        try:
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
                address_output = 'Address', display_name, address, wallet_browser, data_location
                result.append(address_output)

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


def coinbase_chrome():
    appdata_dir = controller.config.APPDATA
    output_dir = controller.config.OUTPUT
    log_name = controller.config.WS_MAIN_LOG_NAME

    function_name = inspect.currentframe().f_code.co_name
    browser_name = function_name.split('_')[-1].capitalize()
    browser_path = browser_dict.get(browser_name)
    wallet_browser = f'{wallet_name} ({browser_name})'

    folders_list = os.listdir(f'{appdata_dir}{browser_path}')

    addresses = []
    result = []

    profiles_check = "Profile"
    profiles_list = [idx for idx in folders_list if idx.lower().startswith(profiles_check.lower())]
    profiles_list_len = len(profiles_list)
    
    default_check = "Default"
    default_list = [idx for idx in folders_list if idx.lower().startswith(default_check.lower())]

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
                address_output = 'Address', display_name, address, wallet_browser, data_location
                result.append(address_output)

        except:
            pass

    if default_list:
        try:
            data_location = appdata_dir + browser_path + "/Default/IndexedDB/chrome-extension_" + ext_id + "_0.indexeddb.leveldb"

            wrapper = ccl_chromium_indexeddb.WrappedIndexDB(data_location)
        
        except:
            pass

        try:
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
                address_output = 'Address', display_name, address, wallet_browser, data_location
                result.append(address_output)

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