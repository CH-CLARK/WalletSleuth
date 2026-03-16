SUPPORTED_OPERATING_SYSTEMS = ['Windows']
SUPPORTED_BROWSERS = {
    'Windows': ['Chrome'],
}
DEPENDENCIES = None
WALLET_METADATA = {
    'name': 'Solflare Wallet',
    'description': '''Solfalre is a non-custodial cryptocurrency browser extension  wallet, specifically 
                    for the Solana blockchain. User are able to easily send and recieve cryptocurrency, 
                    as well as interact with decrentralised applications.''',
    'websites': ['solflare.com'],
    'ext_id': {'chrome':'bhhhlbepdkbapadjdnnojkbgioiodbic'},
    'author': ['CH-CLARK'],
    'plugin-iteration': '1',
    # 'tested_versions': ['2.19.2'],
    'plugin-last-update':'2026-02-12'
}

def solflare_wallet_chrome():
    try:        
        from routes.config import configuration
        from utils.wallet_utils import windows_browser_dict, mac_browser_dict
        from ccl_scripts.ccl_chromium_reader import ccl_chromium_indexeddb

        import inspect
        import os
        import json
        import csv

    except ImportError as e:
        import_catch = f'ERROR: Solflare Wallet (Chrome) - {e} identified! Execution aborted!'
        pass

    operating_system = configuration.OS_SELECTION
    directory_path = configuration.DIRECTORY_PATH
    output_path = configuration.OUTPUT_PATH

    logging_output = os.path.join(output_path, 'wallet_sleuth_logging.txt')

    # logging error and exit
    try:
        if import_catch:
            with open(logging_output, 'a') as log_file:
                log_file.write(f'\n{import_catch}')
            return
    except:
        pass

    # OS check and apply sub directory (Library or Appdata)
    if operating_system == 'windows':
        user_data_subdir = "/AppData"
        browser_dict = windows_browser_dict
        directory_path = directory_path + user_data_subdir

    # if operating_system == 'mac':
    #     user_data_subdir = "/Library"
    #     browser_dict = mac_browser_dict
    #     directory_path = directory_path + user_data_subdir

    # inspect variables
    function_name = inspect.currentframe().f_code.co_name
    browser_name = function_name.split('_')[-1]
    browser_path = browser_dict.get(browser_name)
    wallet_browser = f"{WALLET_METADATA.get('name')} ({browser_name.capitalize()})"
    ext_id = WALLET_METADATA.get('ext_id', {}).get(browser_name)

    # checking profiles and default
    try:
        folders_list = os.listdir(f'{directory_path}{browser_path}')
    except Exception as e:
        folders_list = 'PATH NOT FOUND'

    profiles_check = "Profile"
    profiles_list = [idx for idx in folders_list if idx.lower().startswith(profiles_check.lower())]
    profiles_list_len = len(profiles_list)
    
    default_check = "Default"
    default_list = [idx for idx in folders_list if idx.lower().startswith(default_check.lower())]

    # results and paths list
    identified_paths = []
    addresses = []
    result = []

    if profiles_list:
        for x in range(profiles_list_len):
            data_location_temp = browser_path + "/" + profiles_list[x] + "/IndexedDB/chrome-extension_" + ext_id + "_0.indexeddb.leveldb"
            
            if os.path.exists(directory_path + data_location_temp):
                identified_paths.append(data_location_temp)

                data_location = directory_path + browser_path + "/" + profiles_list[x] + "/IndexedDB/chrome-extension_" + ext_id + "_0.indexeddb.leveldb"
                try:
                    wrapper = ccl_chromium_indexeddb.WrappedIndexDB(data_location)

                except:
                    pass

            try:
                for db_info in wrapper.database_ids:
                    db = wrapper[db_info.dbid_no]

                    for obj_store_name in db.object_store_names:
                        if obj_store_name == 'keyval':
                            obj_store = db[obj_store_name]
                            records = list(obj_store.iterate_records())

                            if records:
                                for record in records:
                                    clientState = record.value.get('clientState')
                                    queries = clientState.get('queries')

                                for items in queries:
                                    state = items.get('state')
                                    data = state.get('data')

                                    if 'netWorth' in data:
                                        inner_data = data.get('data', [])
                                        for item in inner_data:              
                                            #wallet only support SOL anyway, so im not looking for currency codes... yet
                                            addresses.append(item.get('publicKey'))
                            else:
                                pass

                unique_addresses = list(dict.fromkeys(addresses))
                
                for address in unique_addresses:
                    address_output = 'Address', 'Solana', address, wallet_browser, data_location.replace("\\","/")
                    result.append(address_output)

                result = list(set(result))
                    
            except Exception as e:
                pass

    if default_list:
        data_location = directory_path + browser_path + "/Default/IndexedDB/chrome-extension_" + ext_id + "_0.indexeddb.leveldb"

        if os.path.exists(data_location):
            identified_paths.append(data_location)
            data_location = directory_path + browser_path + "/Default/IndexedDB/chrome-extension_" + ext_id + "_0.indexeddb.leveldb"

            try:
                wrapper = ccl_chromium_indexeddb.WrappedIndexDB(data_location)
            except:
                pass

        try:
            for db_info in wrapper.database_ids:
                db = wrapper[db_info.dbid_no]

                for obj_store_name in db.object_store_names:
                    if obj_store_name == 'keyval':
                        obj_store = db[obj_store_name]
                        records = list(obj_store.iterate_records())

                        if records:
                            for record in records:
                                clientState = record.value.get('clientState')
                                queries = clientState.get('queries')

                            for items in queries:
                                state = items.get('state')
                                data = state.get('data')

                                if 'netWorth' in data:
                                    inner_data = data.get('data', [])
                                    for item in inner_data:              
                                        #wallet only support SOL anyway, so im not looking for currency codes... yet
                                        addresses.append(item.get('publicKey'))
                        else:
                            pass

            unique_addresses = list(dict.fromkeys(addresses))
            
            for address in unique_addresses:
                address_output = 'Address', 'Solana', address, wallet_browser, data_location.replace("\\","/")
                result.append(address_output)

            result = list(set(result))
                
        except Exception as e:
            pass

    if not identified_paths:
        with open(logging_output, 'a') as log_file:
            log_file.write(f'\nERROR: {wallet_browser} - Wallet not found!')

    if result:
        header = 'Type', 'Currency', 'Address/Transaction', 'Wallet', 'Path'
        output_file = f'{function_name}_ws_output.csv'
        wallet_output_path = os.path.join(output_path, output_file)
        
        with open(wallet_output_path, 'w', newline='') as result_output:
            write = csv.writer(result_output, escapechar='*')
            write.writerow(header)
            write.writerows(result)

        with open(logging_output, 'a') as log_file:
            log_file.write(f"\nACTION: {wallet_browser} - Addresses identified.")

    if identified_paths and not result:
        with open(logging_output, 'a') as log_file:
            log_file.write(f"\nACTION: {wallet_browser} - No addresses identified.") 