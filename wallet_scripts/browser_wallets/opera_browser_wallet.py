#generic imports
import csv
import json
import os
import inspect
import ast

#controller imports
import controller.config
from controller.utils.wallet_utils import extract_leveldb_data, browser_dict


wallet_name = 'Opera Browser'
ext_id = 'gojhcdgcpbpfigcaejpfhfegekdgiblk'

def browser_opera():
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

    if default_list:
        data_location = browser_path + '/Default/Local Extension Settings/' + ext_id

        try:
            csv_data, location = extract_leveldb_data(appdata_dir, data_location)

            accounts_seq_list = []
            data_text = 'wallet-accounts'

            for row in csv_data:
                if row[1] == data_text:
                    accounts_seq_list.append(int(row[3]))

            accounts_seq_list.sort(reverse=True)
            most_recent_valuetext = None

            for seq in accounts_seq_list:
                for row in csv_data:
                    if row[1] == data_text and int(row[3]) == seq:
                        most_recent_valuetext = row[2]

                        try:
                            json_obj = json.loads(most_recent_valuetext)
                            ammended_json_obj = ast.literal_eval(json_obj)
                            break

                        except json.JSONDecodeError:
                            continue
                        
                if most_recent_valuetext:
                    break

            if most_recent_valuetext:
                for key, value in ammended_json_obj.items():
                    if value["coinType"] == 0:
                        btc = ("Extended Public Key (XPUB)", "BTC", key, wallet_name + " Wallet", location)
                        result.append(btc)
                    elif value["coinType"] == 60:
                        eth = ("Address", "ETH", key, wallet_name + " Wallet", location)
                        result.append(eth)
                    elif value["coinType"] == 501:
                        sol = ("Address", "SOL", key, wallet_name + " Wallet", location)
                        result.append(sol)
                    elif value["coinType"] == 397:
                        near = ("Address", "NEAR", key, wallet_name + " Wallet", location)
                        result.append(near)
                    elif value["coinType"] == 235:
                        fio = ("Address", "FIO", key, wallet_name + " Wallet", location)
                        result.append(fio)
                    elif value["coinType"] == 508:
                        egld = ("Address", "EGLD", key, wallet_name + " Wallet", location)
                        result.append(egld)

        except Exception as e:
            pass

    if result:
        with open(f'{output_dir}/opera_browser_wallet_output.csv', 'w', newline='') as result_output:
            write = csv.writer(result_output, escapechar='\\')
            write.writerows(result)

        with open(f'{output_dir}/{log_name}', 'a') as log_file:
            log_file.write(f'ACTION: {wallet_name} Wallet - Addresses Identified.\n')

    if not result:
        with open(f'{output_dir}/{log_name}', 'a') as log_file:
            log_file.write(f'ACTION: {wallet_name} Wallet - No Addresses Identified.\n')
