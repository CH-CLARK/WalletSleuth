#generic imports
import os
import json
import csv
import inspect

#controller imports
import controller.config
from controller.utils.wallet_utils import extract_leveldb_data, browser_dict


wallet_name = 'MetaMask'
ext_id = 'nkbihfbeogaeaoehlefnkodbefgpgknn'


def metamask_brave():
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

    if profiles_list:
        for x in range(profiles_list_len):
            data_location =  browser_path + "/" + profiles_list[x] + "/Local Extension Settings/" + ext_id

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
                        new_varible = identities_data[key]
                        metamask_address = new_varible['address']
                        address_output = 'Address', 'VARIOUS - See Documention!', metamask_address, wallet_browser, location
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
                if row[1] ==data_text and 'AlertController' in row[2] and int(row[3] == accounts_max_seq):
                    most_recent_valuetext = row[2]

            json_obj = json.loads(most_recent_valuetext)
            pref_controller_data = json_obj.get('PreferencesController')
            identities_data = pref_controller_data["identities"]

            for key in identities_data:
                new_varible = identities_data[key]
                metamask_address = new_varible['address']
                address_output = 'Address', 'VARIOUS - See Documention!', metamask_address, wallet_browser, location
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


def metamask_chrome():
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

    if profiles_list:
        for x in range(profiles_list_len):
            data_location =  browser_path + "/" + profiles_list[x] + "/Local Extension Settings/" + ext_id

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
                        if row[1] ==data_text and 'AlertController' in row[2] and int(row[3] == accounts_max_seq):
                            most_recent_valuetext = row[2]

                    json_obj = json.loads(most_recent_valuetext)
                    pref_controller_data = json_obj.get('PreferencesController')
                    identities_data = pref_controller_data["identities"]

                    for key in identities_data:
                        new_varible = identities_data[key]
                        metamask_address = new_varible['address']
                        address_output = 'Address', 'VARIOUS - See Documention!', metamask_address, wallet_browser, location
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
                if row[1] ==data_text and 'AlertController' in row[2] and int(row[3] == accounts_max_seq):
                    most_recent_valuetext = row[2]

            json_obj = json.loads(most_recent_valuetext)
            pref_controller_data = json_obj.get('PreferencesController')
            identities_data = pref_controller_data["identities"]

            for key in identities_data:
                new_varible = identities_data[key]
                metamask_address = new_varible['address']
                address_output = 'Address', 'VARIOUS - See Documention!', metamask_address, wallet_browser, location
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


def metamask_edge():
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

    if profiles_list:
        for x in range(profiles_list_len):
            data_location =  browser_path + "/" + profiles_list[x] + "/Local Extension Settings/" + ext_id

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
                        if row[1] ==data_text and 'AlertController' in row[2] and int(row[3] == accounts_max_seq):
                            most_recent_valuetext = row[2]

                    json_obj = json.loads(most_recent_valuetext)
                    pref_controller_data = json_obj.get('PreferencesController')
                    identities_data = pref_controller_data["identities"]

                    for key in identities_data:
                        new_varible = identities_data[key]
                        metamask_address = new_varible['address']
                        address_output = 'Address', 'VARIOUS - See Documention!', metamask_address, wallet_browser, location
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
                if row[1] ==data_text and 'AlertController' in row[2] and int(row[3] == accounts_max_seq):
                    most_recent_valuetext = row[2]

            json_obj = json.loads(most_recent_valuetext)
            pref_controller_data = json_obj.get('PreferencesController')
            identities_data = pref_controller_data["identities"]

            for key in identities_data:
                new_varible = identities_data[key]
                metamask_address = new_varible['address']
                address_output = 'Address', 'VARIOUS - See Documention!', metamask_address, wallet_browser, location
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