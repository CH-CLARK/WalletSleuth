SUPPORTED_OPERATING_SYSTEMS = ['Windows']
SUPPORTED_BROWSERS = {
    'Windows': ['Chrome'],
}
DEPENDENCIES = None
WALLET_METADATA = {
    'name': 'Tonkeeper',
    'description': '''Tonkeeper is a non-custodial cryptocurrency browser extension wallet, specifically 
                    for the Toncoin blockchain. User are able to easily send and recieve cryptocurrency, 
                    as well as interact with decrentralised applications.''',
    'websites': ['tonkeeper.com'],
    'ext_id': {'chrome':'omaabbefbmiijedngplfjmnooppbclkk'},
    'author': ['CH-CLARK'],
    # 'tested_versions':'4.3.3' #yes... the plan it to add 'tested versions' to WS... i just need to figure out hwo im going to manage that.
    'plugin-iteration': '1',
    'plugin-last-update':'2026-02-18'
}

def tonkeeper_chrome():
    try:        
        from routes.config import configuration
        from utils.wallet_utils import windows_browser_dict, mac_browser_dict, extract_leveldb_data
        from utils.ton_raw2freindly import raw_to_friendly

        import inspect
        import os
        import json
        import csv

    except ImportError as e: 
        import_catch = f'ERROR: Tonkeeper (Chrome) - {e} identified! Execution aborted!'
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
    addresses = []
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
                    data_text = 'accounts'

                    for row in csv_data:
                        if row[1] == data_text:
                            accounts_seq_list.append(int(row[3]))
                            accounts_max_seq = max(accounts_seq_list)

                        if row[1] == data_text and int(row[3]) == accounts_max_seq:
                            most_recent_valuetext = row[2]

                    json_obj = json.loads(most_recent_valuetext)



                    for items in json_obj:
                        tonWallets = items.get('tonWallets')
                        for items in tonWallets:
                            #raw format
                            rawAddress = items.get('rawAddress')

                            #bouncable
                            friendly_bouncable_addy = raw_to_friendly(rawAddress, bounceable=True)

                            #non-bouncable
                            friendly_nonbouncable_addy = raw_to_friendly(rawAddress, bounceable=False)

                            #anyone of the above address types in a tonexplorer **SHOULD** result in all address types beign displayed. but we will use the non-bouncable in this instance
                            address_output = 'Address', 'Ton', friendly_nonbouncable_addy, wallet_browser, location.replace("\\","/")   
                            result.append(address_output)

                except Exception as e:
                    pass

    if default_list:
        data_location =  browser_path + "/Default/Local Extension Settings/" + ext_id

        if os.path.exists(directory_path + data_location):
            identified_paths.append(data_location)

            try:
                csv_data, location = extract_leveldb_data(directory_path, data_location)
                accounts_seq_list = []
                data_text = 'accounts'

                for row in csv_data:
                    if row[1] == data_text:
                        accounts_seq_list.append(int(row[3]))
                        accounts_max_seq = max(accounts_seq_list)

                    if row[1] == data_text and int(row[3]) == accounts_max_seq:
                        most_recent_valuetext = row[2]

                json_obj = json.loads(most_recent_valuetext)



                for items in json_obj:
                    tonWallets = items.get('tonWallets')
                    for items in tonWallets:
                        #raw format
                        rawAddress = items.get('rawAddress')

                        #bouncable
                        friendly_bouncable_addy = raw_to_friendly(rawAddress, bounceable=True)

                        #non-bouncable
                        friendly_nonbouncable_addy = raw_to_friendly(rawAddress, bounceable=False)

                        #anyone of the above address types in a tonexplorer **SHOULD** result in all address types beign displayed. but we will use the non-bouncable in this instance
                        address_output = 'Address', 'Ton', friendly_nonbouncable_addy, wallet_browser, location.replace("\\","/")   
                        result.append(address_output)

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