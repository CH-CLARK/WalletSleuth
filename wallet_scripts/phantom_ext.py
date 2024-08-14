#generic imports
import csv
import json
import os
import sys

#controller imports
import controller.config

#CCL Imports
import ccl_chrome_ldb_scripts.ccl_leveldb


maxInt = sys.maxsize

while True:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

ENCODING = "iso-8859-1"

def phantom_chrome():
    appdata_dir = controller.config.APPDATA
    output_dir = controller.config.OUTPUT
    log_name = controller.config.WS_MAIN_LOG_NAME


    chrome_user_data = appdata_dir + "/Local/Google/Chrome/User Data"

    folders_list = os.listdir(chrome_user_data)

    profiles_check = "Profile"
    profiles_list = [idx for idx in folders_list if idx.lower().startswith(profiles_check.lower())]
    profiles_list_len = len(profiles_list)

    default_check = "Default"
    default_list = [idx for idx in folders_list if idx.lower().startswith(default_check.lower())]

    output_path = appdata_dir + r"\Phantom_chrome_LDB.csv"

    phantom_chrome_output = []
    if profiles_list:
        for x in range(profiles_list_len):
            profiles_ldb_loc = appdata_dir + "/Local/Google/Chrome/User Data/" + profiles_list[x] + "/Local Extension Settings/bfnaelmomeimhlpmgjnjophhpkkoljpa"
            profiles = profiles_list[x]

            if profiles_ldb_loc:
                try:
                    leveldb_records = ccl_chrome_ldb_scripts.ccl_leveldb.RawLevelDb(profiles_ldb_loc)

                    with open(output_path, "w", encoding="utf-8", newline="") as file1:
                        writes = csv.writer(file1, quoting=csv.QUOTE_ALL)
                        writes.writerow(
                            [
                                "key-text", "value-text", "offset","seq"
                            ])

                        for record in leveldb_records.iterate_records_raw():
                            writes.writerow([
                                record.user_key.decode(ENCODING, "replace"),
                                record.value.decode(ENCODING, "replace"),
                                record.offset,
                                record.seq,
                            ])

                    data_text = ".phantom-labs.vault.accounts"

                    with open(output_path, newline="", errors = 'ignore') as csvfile:
                        dataone = csv.DictReader(csvfile)

                        accounts_seq_list = []
                        for row in dataone:
                            if row['key-text'] == data_text:
                                accounts_seq_list.append(int(row["seq"]))
                                accounts_max_seq = max(accounts_seq_list)

                        csvfile.seek(0)

                        for row in dataone:
                            if row['key-text'] == data_text and int(row['seq']) == accounts_max_seq:
                                most_recent_valuetext = row['value-text']

                    json_obj = json.loads(most_recent_valuetext)

                    accounts = json_obj.get('accounts', [])

                    for account in accounts:
                        chains = account.get('chains', {})

                        for chain_type, chain_data in chains.items():
                            public_key = chain_data.get('publicKey')

                            if public_key and public_key.startswith('0x'):
                                mod_chain = 'eth'
                            else:
                                mod_chain = chain_type
                        
                            phantom_address_output = 'Address', mod_chain, public_key ,'Phantom (Chrome)', profiles_ldb_loc
                            phantom_chrome_output.append(phantom_address_output)

                    with open(output_dir + '/' + 'phantom^_chrome_output.csv', 'w', newline='') as file:
                        write = csv.writer(file) 
                        write.writerows(phantom_chrome_output)

                except Exception as e:
                    pass

    if default_list:
        try:
            leveldb_records = ccl_chrome_ldb_scripts.ccl_leveldb.RawLevelDb(appdata_dir + r"\Local\Google\Chrome\User Data\Default\Local Extension Settings\bfnaelmomeimhlpmgjnjophhpkkoljpa") 
            def_location = appdata_dir + "/Local/Google/Chrome/User Data/Default/Local Extension Settings/bfnaelmomeimhlpmgjnjophhpkkoljpa"
        except Exception as e:
            pass
        
        try:
            if leveldb_records:
                with open(output_path, "w", encoding="utf-8", newline="") as file1:
                    writes = csv.writer(file1, quoting=csv.QUOTE_ALL)
                    writes.writerow(
                        [
                            "key-text", "value-text", "offset", "seq"
                        ])

                    for record in leveldb_records.iterate_records_raw():
                        writes.writerow([
                            record.user_key.decode(ENCODING, "replace"),
                            record.value.decode(ENCODING, "replace"),
                            record.offset,
                            record.seq,
                        ])

                data_text = ".phantom-labs.vault.accounts"

                with open(output_path, newline="", errors = 'ignore') as csvfile:
                    dataone = csv.DictReader(csvfile)

                    accounts_seq_list = []
                
                    for row in dataone:
                        if row['key-text'] == data_text:
                            accounts_seq_list.append(int(row["seq"]))
                            accounts_max_seq = max(accounts_seq_list)
                            
                        
                    csvfile.seek(0)

                    for row in dataone:
                        if row['key-text'] == data_text and int(row['seq']) == accounts_max_seq:
                            most_recent_valuetext = row['value-text']
                    

                json_obj = json.loads(most_recent_valuetext)

                accounts = json_obj.get('accounts', [])

                for account in accounts:
                    chains = account.get('chains', {})

                    for chain_type, chain_data in chains.items():
                        public_key = chain_data.get('publicKey')

                        if public_key and public_key.startswith('0x'):
                            mod_chain = 'eth'
                        else:
                            mod_chain = chain_type
                        
                        phantom_address_output = 'Address', mod_chain, public_key ,'Phantom (Chrome)', def_location
                        phantom_chrome_output.append(phantom_address_output)

        except Exception as e:
            pass

    with open(output_dir + '/' + 'phantom^_chrome_output.csv', 'w', newline='') as file:
        write = csv.writer(file) 
        write.writerows(phantom_chrome_output)

    with open(output_dir + '/' + log_name, 'a') as log_file:
        log_file.write('ACTION: Phantom (Chrome) - Addresses Identified.\n') 

    os.remove(output_path)

def phantom_brave():
    appdata_dir = controller.config.APPDATA
    output_dir = controller.config.OUTPUT
    log_name = controller.config.WS_MAIN_LOG_NAME

    brave_user_data = appdata_dir + "/Local/BraveSoftware/Brave-Browser/User Data"

    folders_list = os.listdir(brave_user_data)

    profiles_check = "Profile"
    profiles_list = [idx for idx in folders_list if idx.lower().startswith(profiles_check.lower())]
    profiles_list_len = len(profiles_list)

    default_check = "Default"
    default_list = [idx for idx in folders_list if idx.lower().startswith(default_check.lower())]

    output_path = appdata_dir + r"\Phantom_brave_LDB.csv"

    phantom_brave_output = []
    if profiles_list:
        for x in range(profiles_list_len):
            profiles_ldb_loc = appdata_dir + "/Local/BraveSoftware/Brave-Browser/User Data/" + profiles_list[x] + "/Local Extension Settings/bfnaelmomeimhlpmgjnjophhpkkoljpa"
            profiles = profiles_list[x]

            if profiles_ldb_loc:
                try:
                    leveldb_records = ccl_chrome_ldb_scripts.ccl_leveldb.RawLevelDb(profiles_ldb_loc)
                except Exception as e:
                    pass

                try:
                    with open(output_path, "w", encoding="utf-8", newline="") as file1:
                        writes = csv.writer(file1, quoting=csv.QUOTE_ALL)
                        writes.writerow(
                            [
                                "key-text", "value-text", "offset","seq"
                            ])

                        for record in leveldb_records.iterate_records_raw():
                            writes.writerow([
                                record.user_key.decode(ENCODING, "replace"),
                                record.value.decode(ENCODING, "replace"),
                                record.offset,
                                record.seq,
                            ])

                    
                    data_text = ".phantom-labs.vault.accounts"

                    with open(output_path, newline="", errors = 'ignore') as csvfile:
                        dataone = csv.DictReader(csvfile)

                        accounts_seq_list = []
                        for row in dataone:
                            if row['key-text'] == data_text:
                                accounts_seq_list.append(int(row["seq"]))
                                accounts_max_seq = max(accounts_seq_list)

                        csvfile.seek(0)

                        for row in dataone:
                            if row['key-text'] == data_text and int(row['seq']) == accounts_max_seq:
                                most_recent_valuetext = row['value-text']

                    json_obj = json.loads(most_recent_valuetext)

                    accounts = json_obj.get('accounts', [])

                    for account in accounts:
                        chains = account.get('chains', {})

                        for chain_type, chain_data in chains.items():
                            public_key = chain_data.get('publicKey')

                            if public_key and public_key.startswith('0x'):
                                mod_chain = 'eth'
                            else:
                                mod_chain = chain_type
                        
                            phantom_address_output = 'Address', mod_chain, public_key ,'Phantom (brave)', profiles_ldb_loc
                            phantom_brave_output.append(phantom_address_output)

                    with open(output_dir + '/' + 'phantom^_brave_output.csv', 'w', newline='') as file:
                        write = csv.writer(file) 
                        write.writerows(phantom_brave_output)

                except Exception as e:
                    pass

    if default_list:
        try:
            leveldb_records = ccl_chrome_ldb_scripts.ccl_leveldb.RawLevelDb(appdata_dir + r"\Local\BraveSoftware\Brave-Browser\User Data\Default\Local Extension Settings\bfnaelmomeimhlpmgjnjophhpkkoljpa") 
            def_location = appdata_dir + "/Local/BraveSoftware/Brave-Browser/User Data/Default/Local Extension Settings/bfnaelmomeimhlpmgjnjophhpkkoljpa"
        except:
            pass

        try:
            if leveldb_records:
                with open(output_path, "w", encoding="utf-8", newline="") as file1:
                    writes = csv.writer(file1, quoting=csv.QUOTE_ALL)
                    writes.writerow(
                        [
                            "key-text", "value-text", "offset", "seq"
                        ])

                    for record in leveldb_records.iterate_records_raw():
                        writes.writerow([
                            record.user_key.decode(ENCODING, "replace"),
                            record.value.decode(ENCODING, "replace"),
                            record.offset,
                            record.seq,
                        ])

                data_text = ".phantom-labs.vault.accounts"

                with open(output_path, newline="", errors = 'ignore') as csvfile:
                    dataone = csv.DictReader(csvfile)

                    accounts_seq_list = []
                
                    for row in dataone:
                        if row['key-text'] == data_text:
                            accounts_seq_list.append(int(row["seq"]))
                            accounts_max_seq = max(accounts_seq_list)
                            
                        
                    csvfile.seek(0)

                    for row in dataone:
                        if row['key-text'] == data_text and int(row['seq']) == accounts_max_seq:
                            most_recent_valuetext = row['value-text']
                    

                json_obj = json.loads(most_recent_valuetext)

                accounts = json_obj.get('accounts', [])

                for account in accounts:
                    chains = account.get('chains', {})

                    for chain_type, chain_data in chains.items():
                        public_key = chain_data.get('publicKey')

                        if public_key and public_key.startswith('0x'):
                            mod_chain = 'eth'
                        else:
                            mod_chain = chain_type
                        
                        phantom_address_output = 'Address', mod_chain, public_key ,'Phantom (brave)', def_location
                        phantom_brave_output.append(phantom_address_output)
        except:
            pass

    with open(output_dir + '/' + 'phantom^_brave_output.csv', 'w', newline='') as file:
        write = csv.writer(file) 
        write.writerows(phantom_brave_output)

    with open(output_dir + '/' + log_name, 'a') as log_file:
        log_file.write('ACTION: Phantom (brave) - Addresses Identified.\n') 

    os.remove(output_path)