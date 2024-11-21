#generic imports
import csv
import json
import os
import inspect

#controller imports
import controller.config
from controller.utils.wallet_utils import extract_leveldb_data, browser_dict

wallet_name = 'Brave Browser'
ext_id = 'odbfpeeihdkbihmopkbjmoonfanlbfcl'


def browser_brave():
    appdata_dir = controller.config.APPDATA
    output_dir = controller.config.OUTPUT
    log_name = controller.config.WS_MAIN_LOG_NAME

    function_name = inspect.currentframe().f_code.co_name
    browser_name = function_name.split('_')[-1].capitalize()
    browser_path = browser_dict.get(browser_name)
    wallet_browser = f'{wallet_name} ({browser_name})'

    folders_list = os.listdir(f'{appdata_dir}{browser_path}')

    result = []

    profiles_check  = "Profile"
    profiles_list = [idx for idx in folders_list if idx.lower().startswith(profiles_check.lower())]
    profiles_list_len = len(profiles_list)

    default_check = "Default"
    default_list = [idx for idx in folders_list if idx.lower().startswith(default_check.lower())]


    def brave_legacy():
        if profiles_list:
            for x in range(profiles_list_len):
                data_location = browser_path + "/" + profiles_list[x] + "/Local Extension Settings/" + ext_id

                if data_location:
                    try:
                        csv_data, location = extract_leveldb_data(appdata_dir, data_location)

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

                        for key in identities_data:
                            new_variable = identities_data[key]
                            brave_legacy_address = new_variable["address"]
                            address_output = 'Address', 'VARIOUS - See Documention!', brave_legacy_address, wallet_name + ' Legacy Wallet', location
                            result.append(address_output)

                    except:
                        pass

        if default_list:
            data_location = browser_path + '/Default/Local Extension Settings/' + ext_id

            try:
                csv_data, location = extract_leveldb_data(appdata_dir, data_location)

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

                for key in identities_data:
                    new_variable = identities_data[key]
                    brave_legacy_address = new_variable["address"]
                    address_output = 'Address', 'VARIOUS - See Documention!', brave_legacy_address, wallet_name + ' Legacy Wallet', location
                    result.append(address_output)

            except:
                pass
    
    def brave_wallet():
        if profiles_list:

            temp = []

            for x in range(profiles_list_len):
                data_location = appdata_dir + browser_path + "/" + profiles_list[x] + "/Preferences"

                with open(data_location, 'r') as preferences_file:
                    read_profiles = preferences_file.read()

                    json_obj = json.loads(read_profiles)
                    brave_obj = json_obj['brave']
                    wallet_obj = brave_obj['wallet']
                    keyrings_obj = wallet_obj['keyrings']

                    default_obj = keyrings_obj['default']
                    default_metas_obj = default_obj['account_metas']

                    filecoin_obj = keyrings_obj['filecoin']
                    filecoin_metas_obj = filecoin_obj['account_metas']

                    solana_obj = keyrings_obj['solana']
                    solana_metas_obj = solana_obj['account_metas']


                    if default_obj:
                        for i in default_metas_obj:
                            default_num_wallets = (len(default_metas_obj))

                        for c in range(0, default_num_wallets):
                            num = str(c)
                            meta_objs = "m/44'/60'/0'/0/" + num
                            address_obj = default_metas_obj[meta_objs]
                            default_addresses = address_obj['account_address']
                            default_output = 'Address', 'VARIOUS - See Documention!', default_addresses,  wallet_name + ' Wallet', data_location
                            result.append(default_output)

                    if filecoin_obj:
                        for i in filecoin_metas_obj:
                            filecoin_num_wallets = (len(filecoin_metas_obj))

                        for c in range(0, filecoin_num_wallets):
                            num = str(c)
                            meta_objs = "m/44'/461'/0'/0/" + num
                            address_obj = filecoin_metas_obj[meta_objs]
                            filecoin_addresses = address_obj['account_address']
                            filecoin_output = 'Address', 'Filecoin', filecoin_addresses,  wallet_name + ' Wallet', data_location
                            result.append(filecoin_output)

                    if solana_obj:
                        for i in solana_metas_obj:
                            solana_num_wallets = (len(solana_metas_obj))

                        for c in range(0, solana_num_wallets):
                            num = str(c)
                            meta_objs = "m/44'/501'/" + num + "'/0'"
                            address_obj = solana_metas_obj[meta_objs]
                            solana_addresses = address_obj['account_address']
                            solana_output = 'Address', 'Solana', solana_addresses,  wallet_name + ' Wallet', data_location
                            result.append(solana_output)


        if default_list:
            data_location = appdata_dir + browser_path + "/Default/Preferences"        

            with open(data_location, 'r') as preferences_file:
                read_profiles = preferences_file.read()

                json_obj = json.loads(read_profiles)
                brave_obj = json_obj['brave']
                wallet_obj = brave_obj['wallet']
                keyrings_obj = wallet_obj['keyrings']

                default_obj = keyrings_obj['default']
                default_metas_obj = default_obj['account_metas']

                filecoin_obj = keyrings_obj['filecoin']
                filecoin_metas_obj = filecoin_obj['account_metas']

                solana_obj = keyrings_obj['solana']
                solana_metas_obj = solana_obj['account_metas']


                if default_obj:
                    for i in default_metas_obj:
                        default_num_wallets = (len(default_metas_obj))

                    for c in range(0, default_num_wallets):
                        num = str(c)
                        meta_objs = "m/44'/60'/0'/0/" + num
                        address_obj = default_metas_obj[meta_objs]
                        default_addresses = address_obj['account_address']
                        default_output = 'Address', 'VARIOUS - See Documention!', default_addresses,  'Brave Browser Wallet', data_location
                        result.append(default_output)

                if filecoin_obj:
                    for i in filecoin_metas_obj:
                        filecoin_num_wallets = (len(filecoin_metas_obj))

                    for c in range(0, filecoin_num_wallets):
                        num = str(c)
                        meta_objs = "m/44'/461'/0'/0/" + num
                        address_obj = filecoin_metas_obj[meta_objs]
                        filecoin_addresses = address_obj['account_address']
                        filecoin_output = 'Address', 'Filecoin', filecoin_addresses,  'Brave Browser Wallet', data_location
                        result.append(filecoin_output)

                if solana_obj:
                    for i in solana_metas_obj:
                        solana_num_wallets = (len(solana_metas_obj))

                    for c in range(0, solana_num_wallets):
                        num = str(c)
                        meta_objs = "m/44'/501'/" + num + "'/0'"
                        address_obj = solana_metas_obj[meta_objs]
                        solana_addresses = address_obj['account_address']
                        solana_output = 'Address', 'Solana', solana_addresses,  'Brave Browser Wallet', data_location
                        result.append(solana_output)                    

        if result:
            with open(f'{output_dir}/brave_browser_wallet_output.csv', 'w', newline='') as result_output:
                write = csv.writer(result_output, escapechar='\\')
                write.writerows(result)

            with open(f'{output_dir}/{log_name}', 'a') as log_file:
                log_file.write(f'ACTION: {wallet_name} Wallet - Addresses Identified.\n')

        if not result:
            with open(f'{output_dir}/{log_name}', 'a') as log_file:
                log_file.write(f'ACTION: {wallet_name} Wallet - No Addresses Identified.\n')

    brave_legacy()
    brave_wallet()