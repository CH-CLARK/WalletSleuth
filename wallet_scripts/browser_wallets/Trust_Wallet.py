SUPPORTED_OPERATING_SYSTEMS = ['Windows']
SUPPORTED_BROWSERS = {
    'Windows': ['Chrome'],
}
DEPENDENCIES = None
WALLET_METADATA = {
    'name': 'Trust Wallet',
    'description': '''Trust Wallet is a non-custodial browser extension wallet that supports a variety of popular cryptocurrencies. Users are able to easily send 
        and recieve cryptocurrency, as well as interact with decentralised applications.''',
    'websites': ['trustwallet.com'],
    'ext_id': {'chrome':'egjidjbpglichdcondbcbdnbeeppgdph'},
    'author': ['CH-CLARK'],
    'plugin-iteration': '1',
    'plugin-last-update':'2026-01-20'
}

def trust_wallet_chrome():
    try:        
        from routes.config import configuration
        from utils.wallet_utils import windows_browser_dict, mac_browser_dict, extract_leveldb_data

        import inspect
        import os
        import json
        import csv

    except ImportError as e: 
        import_catch = f'ERROR: MetaMask (Chrome) - {e} identified! Execution aborted!'
        pass

    # user set varibles
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
    result = []
    identified_paths = []

    if profiles_list:

        for x in range(profiles_list_len):
            data_location =  browser_path + "/" + profiles_list[x] + "/Local Extension Settings/" + ext_id
            
            if os.path.exists(directory_path + data_location):
                identified_paths.append(data_location)
    
                try:
                    csv_data, location = extract_leveldb_data(directory_path, data_location)
                    accounts_seq_list = []
                    data_text = 'trust:store'
                    
                    for row in csv_data:
                        if row[1] == data_text:
                            accounts_seq_list.append(int(row[3]))
                            accounts_max_seq = max(accounts_seq_list)    

                    for row in csv_data:
                        if row[1] == data_text and 'balancesPerWalletAccount' in row[2] and int(row[3] == accounts_max_seq):
                            most_recent_valuetext = row[2]

                    json_obj = json.loads(most_recent_valuetext)
                    
                    asset_json = json_obj[2]["asset"]
                    assets_per_wallet = asset_json.get("assetsPerWallet", {})

                    wallet_json = json_obj[2]["wallet"]
                    accounts_per_wallet = wallet_json.get('accountsPerWallet')

                    try:
                        for wallet_id, assets in assets_per_wallet.items():

                            if wallet_id == "null" or wallet_id not in accounts_per_wallet:
                                continue

                            combined_dict = []

                            asset_lookup = {
                                asset["assetId"]: asset["name"]
                                for asset in assets.get("itemsV2", [])
                            }

                            for account in accounts_per_wallet[wallet_id].values():
                                for coin_id, item in account["items"].items():

                                    asset_id = f"c{coin_id}"

                                    if asset_id in asset_lookup:
                                        combined_dict.append({
                                            "id": asset_id,
                                            "address": item["address"],
                                            "name": asset_lookup[asset_id]
                                        })
                        
                            for items in combined_dict:
                                address_output = 'Address', items.get('name'), items.get('address'), wallet_browser, location.replace("\\","/")
                                result.append(address_output)
                        
                    except Exception as e:
                        pass
                            
                except Exception as e:
                    pass

    if default_list:
        data_location =  browser_path + "/Default/Local Extension Settings/" + ext_id

        try:
            csv_data, location = extract_leveldb_data(directory_path, data_location)
            accounts_seq_list = []
            data_text = 'trust:store'
            
            for row in csv_data:
                if row[1] == data_text:
                    accounts_seq_list.append(int(row[3]))
                    accounts_max_seq = max(accounts_seq_list)    

            for row in csv_data:
                if row[1] == data_text and 'balancesPerWalletAccount' in row[2] and int(row[3] == accounts_max_seq):
                    most_recent_valuetext = row[2]

            json_obj = json.loads(most_recent_valuetext)
            
            asset_json = json_obj[2]["asset"]
            assets_per_wallet = asset_json.get("assetsPerWallet", {})

            wallet_json = json_obj[2]["wallet"]
            accounts_per_wallet = wallet_json.get('accountsPerWallet')

            try:
                for wallet_id, assets in assets_per_wallet.items():

                    if wallet_id == "null" or wallet_id not in accounts_per_wallet:
                        continue

                    combined_dict = []

                    asset_lookup = {
                        asset["assetId"]: asset["name"]
                        for asset in assets.get("itemsV2", [])
                    }

                    for account in accounts_per_wallet[wallet_id].values():
                        for coin_id, item in account["items"].items():

                            asset_id = f"c{coin_id}"

                            if asset_id in asset_lookup:
                                combined_dict.append({
                                    "id": asset_id,
                                    "address": item["address"],
                                    "name": asset_lookup[asset_id]
                                })

                    for items in combined_dict:
                        address_output = 'Address', items.get('name'), items.get('address'), wallet_browser, location.replace("\\","/")
                        result.append(address_output)
                
            except Exception as e:
                pass
                    
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
            log_file.write(f'\nACTION: {wallet_browser} - Addresses identified.')

    if identified_paths and not result:
        with open(logging_output, 'a') as log_file:
            log_file.write(f'\nACTION: {wallet_browser} - No addresses identified.') 