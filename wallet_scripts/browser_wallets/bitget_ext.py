#Removed for maintenance

#generic imports
import os
import json
import csv
import sys
import inspect

#controller imports

import controller.config
from controller.utils.wallet_utils import extract_leveldb_data, browser_dict

wallet_name = 'Bitget'
ext_id = 'jiidiaalihmmhddjgbnbgdfflelocpak'


def bitget_brave():
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
                    
                    data_text = "accounts"

                    for row in csv_data:
                        if row[1] == data_text:
                            accounts_seq_list.append(int(row[3]))
                            accounts_max_seq = max(accounts_seq_list)
                        
                        if row[1] == data_text and int(row[3]) == accounts_max_seq:
                            most_recent_valuetext = row[2]
                    
                    json_obj = json.loads(most_recent_valuetext)
                    currency_data = json_obj.get('currency')

                    for x in range(len(currency_data)):
                        address_output = 'Address', currency_data[x]['symbol'], currency_data[x]['address'] ,'Bitget (Chrome)', location
                        result.append(address_output)    

                except:
                    pass


    if default_list:
        data_location = browser_path + '/Default/Local Extension Settings/' + ext_id

        try:
            csv_data, location = extract_leveldb_data(appdata_dir, data_location)
            
            accounts_seq_list = []
            
            data_text = "accounts"

            for row in csv_data:
                if row[1] == data_text:
                    accounts_seq_list.append(int(row[3]))
                    accounts_max_seq = max(accounts_seq_list)
                
                if row[1] == data_text and int(row[3]) == accounts_max_seq:
                    most_recent_valuetext = row[2]
            
            json_obj = json.loads(most_recent_valuetext)
            currency_data = json_obj.get('currency')

            for x in range(len(currency_data)):
                address_output = 'Address', currency_data[x]['symbol'], currency_data[x]['address'] ,'Bitget (Chrome)', location
                result.append(address_output)

        except Exception as e:
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


def bitget_chrome():
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
                    
                    data_text = "accounts"

                    for row in csv_data:
                        if row[1] == data_text:
                            accounts_seq_list.append(int(row[3]))
                            accounts_max_seq = max(accounts_seq_list)
                        
                        if row[1] == data_text and int(row[3]) == accounts_max_seq:
                            most_recent_valuetext = row[2]
                    
                    json_obj = json.loads(most_recent_valuetext)
                    currency_data = json_obj.get('currency')

                    for x in range(len(currency_data)):
                        address_output = 'Address', currency_data[x]['symbol'], currency_data[x]['address'] ,'Bitget (Chrome)', location
                        result.append(address_output)    

                except:
                    pass


    if default_list:
        data_location = browser_path + '/Default/Local Extension Settings/' + ext_id

        try:
            csv_data, location = extract_leveldb_data(appdata_dir, data_location)
            
            accounts_seq_list = []
            
            data_text = "accounts"

            for row in csv_data:
                if row[1] == data_text:
                    accounts_seq_list.append(int(row[3]))
                    accounts_max_seq = max(accounts_seq_list)
                
                if row[1] == data_text and int(row[3]) == accounts_max_seq:
                    most_recent_valuetext = row[2]
            
            json_obj = json.loads(most_recent_valuetext)
            currency_data = json_obj.get('currency')

            for x in range(len(currency_data)):
                address_output = 'Address', currency_data[x]['symbol'], currency_data[x]['address'] ,'Bitget (Chrome)', location
                result.append(address_output)

        except Exception as e:
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