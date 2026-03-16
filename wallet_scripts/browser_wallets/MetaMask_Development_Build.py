SUPPORTED_OPERATING_SYSTEMS = ['Windows']
SUPPORTED_BROWSERS = {
    'Windows': ['Chrome'],
}
DEPENDENCIES = None
WALLET_METADATA = {
    'name': 'MetaMask Development Build',
    'description': '''MetaMask Development Build is a non-custodial browser extension wallet, primarily for the Solana and Ethereum cryptocurrencies and tokens built on the Ethereum network, support for other Ethereum Virtual Machine (EVM) 
                    compatable networks is also possible. Users are able to easily send and recieve cryptocurrency, as well as interact with decentralised applications. 
                    The development build allows access to additional unstable APIs to maximize developer control. ''',
    'websites': ['metamask.io'],
    'ext_id': {'chrome':'ljfoeinjpaedjfecbmggjgodbgkmjkjk'},
    'author': ['CH-CLARK'],
    'plugin-iteration': '1',
    'plugin-last-update':'2026-01-20'
}

def metamask_development_build_chrome():
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
                    data_text = 'data'

                    for row in csv_data:
                        if row[1] == data_text:
                            accounts_seq_list.append(int(row[3]))
                            accounts_max_seq = max(accounts_seq_list)
                            
                    for row in csv_data:
                        if row[1] == data_text and 'AlertController' in row[2] and int(row[3] == accounts_max_seq):
                            most_recent_valuetext = row[2]

                    json_obj = json.loads(most_recent_valuetext)
                    pref_controller_data = json_obj.get('PreferencesController')
                    identities_data = pref_controller_data["identities"]

                    #this accoutns for the new 'AccountsController' which gives further adress inforamtion, and allwos for theolder identities if that does not exist
                    try:
                        accounts_controller = json_obj.get('AccountsController')
                        internal_accounts = accounts_controller.get('internalAccounts')
                        accounts = internal_accounts.get('accounts', [])

                        if 'AccountsController' in json_obj:
                            for item in accounts.values():
                                currency_address = item.get('address')

                                metadata = item.get('metadata')
                                snap = metadata.get('snap')
                                if snap:
                                    currency_name = snap.get('name')
                                else:
                                    currency_name = 'Ethereum'

                                address_output = 'Address', currency_name, currency_address, wallet_browser, location.replace("\\","/")
                                result.append(address_output)

                    except Exception as e:
                        pass
                        for key in identities_data:
                            new_varible = identities_data[key]
                            metamask_address = new_varible['address']
                            address_output = 'Address', ' Multiple Chain Types', metamask_address, wallet_browser, location.replace("\\","/")
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
                data_text = 'data'

                for row in csv_data:
                    if row[1] == data_text:
                        accounts_seq_list.append(int(row[3]))
                        accounts_max_seq = max(accounts_seq_list)
                        
                for row in csv_data:
                    if row[1] == data_text and 'AlertController' in row[2] and int(row[3] == accounts_max_seq):
                        most_recent_valuetext = row[2]

                json_obj = json.loads(most_recent_valuetext)
                pref_controller_data = json_obj.get('PreferencesController')
                identities_data = pref_controller_data["identities"]

                #this accoutns for the new 'AccountsController' which gives further adress inforamtion, and allwos for theolder identities if that does not exist
                try:
                    accounts_controller = json_obj.get('AccountsController')
                    internal_accounts = accounts_controller.get('internalAccounts')
                    accounts = internal_accounts.get('accounts', [])

                    if 'AccountsController' in json_obj:
                        for item in accounts.values():
                            currency_address = item.get('address')

                            metadata = item.get('metadata')
                            snap = metadata.get('snap')
                            if snap:
                                currency_name = snap.get('name')
                            else:
                                currency_name = 'Ethereum'

                            address_output = 'Address', currency_name, currency_address, wallet_browser, location.replace("\\","/")
                            result.append(address_output)

                except Exception as e:
                    pass
                    for key in identities_data:
                        new_varible = identities_data[key]
                        metamask_address = new_varible['address']
                        address_output = 'Address', ' Multiple Chain Types', metamask_address, wallet_browser, location.replace("\\","/")
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