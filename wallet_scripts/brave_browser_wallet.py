#generic imports
import csv
import json
import os
import sys

#controller imports
import controller.config

#CCL Imports
import ccl_chrome_ldb_scripts.ccl_leveldb


def brave_wallet():
    appdata_dir = controller.config.APPDATA
    output_dir = controller.config.OUTPUT
    log_name = controller.config.WS_MAIN_LOG_NAME

    bravebrowser_userdata = appdata_dir + "/Local/BraveSoftware/Brave-Browser/User Data"

    folders_list = os.listdir(bravebrowser_userdata)

    profiles_check  = "Profile"
    profiles_list = [idx for idx in folders_list if idx.lower().startswith(profiles_check.lower())]
    profiles_list_len = len(profiles_list)

    #checking for default location
    default_check = "Default"
    default_list = [idx for idx in folders_list if idx.lower().startswith(default_check.lower())]

    bravebrowser_output = []

    if default_list:
        default_user_location = bravebrowser_userdata + '/Default/Preferences'

        with open(default_user_location, 'r') as def_user_loc_pref:
            read_def = def_user_loc_pref.read()

            json_obj = json.loads(read_def)
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
                    default_output = 'Address', 'VARIOUS - See Documention!', default_addresses,  'Brave Browser Wallet', default_user_location
                    bravebrowser_output.append(default_output)

            if filecoin_obj:
                for i in filecoin_metas_obj:
                    filecoin_num_wallets = (len(filecoin_metas_obj))

                for c in range(0, filecoin_num_wallets):
                    num = str(c)
                    meta_objs = "m/44'/461'/0'/0/" + num
                    address_obj = filecoin_metas_obj[meta_objs]
                    filecoin_addresses = address_obj['account_address']      
                    filecoin_output = 'Address', 'VARIOUS - See Documention!', filecoin_addresses,  'Brave Browser Wallet', default_user_location
                    bravebrowser_output.append(filecoin_output)
            
            if solana_obj:
                for i in solana_metas_obj:
                    solana_num_wallets = (len(solana_metas_obj))

                for c in range(0, solana_num_wallets):
                    num = str(c)
                    meta_objs = "m/44'/501'/" + num + "'/0'"
                    address_obj = solana_metas_obj[meta_objs]
                    solana_addresses = address_obj['account_address']      
                    solana_ouput = 'Address', 'VARIOUS - See Documention!', solana_addresses,  'Brave Browser Wallet', default_user_location
                    bravebrowser_output.append(solana_ouput)

    if profiles_list:
        try:
            for x in range(profiles_list_len):
                profiles_user_location = bravebrowser_userdata + '/' + profiles_list[x] +'/Preferences'
                with open(profiles_user_location, 'r') as profiles_loc_pref:
                    read_profiles = profiles_loc_pref.read()

                    pro_json_obj = json.loads(read_profiles)
                    pro_brave_obj = pro_json_obj['brave']
                    pro_waller_obj = pro_brave_obj['wallet']
                    pro_keyrings_obj = pro_waller_obj['keyrings']

                    pro_def_obj = pro_keyrings_obj['default']
                    pro_def_metas_obj = pro_def_obj['account_metas']

                    pro_file_obj = pro_keyrings_obj['filecoin']
                    pro_file_metas_obj = pro_file_obj['account_metas']

                    pro_sol_obj = pro_keyrings_obj['solana']
                    pro_sol_metas_obj = pro_sol_obj['account_metas']

                    if pro_def_obj:
                        for i in pro_def_metas_obj:
                            pro_default_num_wallets = (len(pro_def_metas_obj))
                        
                        for c in range(0, pro_default_num_wallets):
                            pro_num = str(c)
                            pro_meta_objs = "m/44'/60'/0'/0/" + pro_num
                            pro_address_obj = pro_def_metas_obj[pro_meta_objs]
                            pro_default_addresses = pro_address_obj['account_address']      
                            pro_default_output = 'Address', 'VARIOUS - See Documention!', pro_default_addresses,  'Brave Browser Wallet', profiles_user_location
                            bravebrowser_output.append(pro_default_output)

                    if pro_file_obj:
                        for i in pro_file_metas_obj:
                            pro_file_num_wallets = (len(pro_file_metas_obj))

                        for c in range(0, pro_file_num_wallets):
                            pro_num = str(c)
                            pro_meta_objs = "m/44'/461'/0'/0/"  + pro_num
                            pro_address_obj = pro_file_metas_obj[pro_meta_objs]
                            pro_file_addresses = pro_address_obj['account_address']      
                            pro_file_output = 'Address', 'VARIOUS - See Documention!', pro_file_addresses,  'Brave Browser Wallet', profiles_user_location
                            bravebrowser_output.append(pro_file_output)

                    if pro_sol_obj:
                        for i in pro_sol_metas_obj:
                            pro_sol_num_wallets = (len(pro_sol_metas_obj))

                    for c in range(0, pro_sol_num_wallets):
                        pro_num = str(c)
                        pro_meta_objs = "m/44'/501'/" + pro_num + "'/0'"
                        pro_address_obj = pro_sol_metas_obj[pro_meta_objs]
                        pro_sol_addresses = pro_address_obj['account_address']      
                        pro_sol_ouput = 'Address', 'VARIOUS - See Documention!', pro_sol_addresses,  'Brave Browser Wallet', profiles_user_location
                        bravebrowser_output.append(pro_sol_ouput)

        except Exception as e:
            pass

    with open(output_dir + '/' + 'brave_browser_wallet_addresses.csv', 'w', newline='') as output_file:
        write = csv.writer(output_file)
        write.writerows(bravebrowser_output)

    with open(output_dir + '/' + log_name, 'a') as log_file:
        log_file.write('ACTION: Brave Browser Wallet - Addresses Identified.\n')  