#Generic Imports
import sys
import os
import json
import csv
import pathlib

def bravebrowser_dump(ask_dir, output_dir):
    bravebrowser_userdata = ask_dir + "/Local/BraveSoftware/Brave-Browser/User Data"

    folders_list = os.listdir(bravebrowser_userdata)

    #checking for profile locations
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
                    default_output = 'VARIOUS - See Documention!', default_addresses,  'Brave Browser Wallet', default_user_location
                    bravebrowser_output.append(default_output)

            if filecoin_obj:
                for i in filecoin_metas_obj:
                    filecoin_num_wallets = (len(filecoin_metas_obj))

                for c in range(0, filecoin_num_wallets):
                    num = str(c)
                    meta_objs = "m/44'/461'/0'/0/" + num
                    address_obj = filecoin_metas_obj[meta_objs]
                    filecoin_addresses = address_obj['account_address']      
                    filecoin_output = 'VARIOUS - See Documention!', filecoin_addresses,  'Brave Browser Wallet', default_user_location
                    bravebrowser_output.append(filecoin_output)
            
            if solana_obj:
                for i in solana_metas_obj:
                    solana_num_wallets = (len(solana_metas_obj))

                for c in range(0, solana_num_wallets):
                    num = str(c)
                    meta_objs = "m/44'/501'/" + num + "'/0'"
                    address_obj = solana_metas_obj[meta_objs]
                    solana_addresses = address_obj['account_address']      
                    solana_ouput = 'VARIOUS - See Documention!', solana_addresses,  'Brave Browser Wallet', default_user_location
                    bravebrowser_output.append(solana_ouput)

        with open(output_dir + '/' + 'WalletSleuth_log.txt', 'a') as log_file:
            log_file.write('ACTION: (BRAVE BROWSER) - Addresses Identified in Default.\n')


    if profiles_list:
        print("DO PROFILES LOCATIONS")
    