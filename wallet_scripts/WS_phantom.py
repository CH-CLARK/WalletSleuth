#Generic Imports
import sys
import os
import json
import csv
import pathlib

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

def phantom_chrome_dump(ask_dir, output_dir):
    chrome_user_data = ask_dir + "/Local/Google/Chrome/User Data"

    folders_list = os.listdir(chrome_user_data)

    #Checking profiles locations
    profiles_check  = "Profile"
    profiles_list = [idx for idx in folders_list if idx.lower().startswith(profiles_check.lower())]
    profiles_list_len = len(profiles_list)

    #Checking default location
    default_check = "Default"
    default_list = [idx for idx in folders_list if idx.lower().startswith(default_check.lower())]

    output_path = ask_dir + r"\phantom_chrome_LDB.csv"

    phantom_chrome_output = []

    if profiles_list:
        for x in range(profiles_list_len):
            profiles_ldb_loc = ask_dir + "/Local/Google/Chrome/User Data/" + profiles_list[x] + "/Local Extension Settings/bfnaelmomeimhlpmgjnjophhpkkoljpa"
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

                    data_text = "ownerToClusterToLamportBalance"
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

                    for x in range(len(json_obj['value'])):
                        currency_data = list(json_obj["value"].keys())[x]
                        print(currency_data)
                        
                        phantom_address_output = 'SOL', currency_data ,'Phantom (Chrome)', def_location
                        
                        phantom_chrome_output.append(phantom_address_output) 

                        print(phantom_address_output)


                    with open(output_dir + '/' + 'phantom_chrome_addresses.csv', 'a', newline='') as file:
                        write = csv.writer(file) 
                        write.writerow(phantom_chrome_output)
                    

                    with open(output_dir + '/' + 'WalletSleuth_log.txt', 'a') as log_file:
                        log_file.write('ACTION: (PHANTOM - CHROME) - Addresses identified in ' + profiles +'.\n')


                except Exception:
                    pass

    if default_list:
        leveldb_records = ccl_chrome_ldb_scripts.ccl_leveldb.RawLevelDb(ask_dir + r"\Local\Google\Chrome\User Data\Default\Local Extension Settings\bfnaelmomeimhlpmgjnjophhpkkoljpa") 
        def_location = ask_dir + "/Local/Google/Chrome/User Data/Default/Local Extension Settings/bfnaelmomeimhlpmgjnjophhpkkoljpa"
        
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

            data_text = "ownerToClusterToLamportBalance"
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

            for x in range(len(json_obj['value'])):
                currency_data = list(json_obj["value"].keys())[x]
                print(currency_data)
                
                phantom_address_output = 'SOL', currency_data ,'Phantom (Chrome)', def_location
                
                phantom_chrome_output.append(phantom_address_output) 

                print(phantom_address_output)

    with open(output_dir + '/' + 'WalletSleuth_log.txt', 'a') as log_file:
        log_file.write('ACTION: (PHANTOM - CHROME) - Addresses identified in Default Profile.\n')


    with open(output_dir + '/' + 'phantom_chrome_addresses.csv', 'w', newline='') as file:
        write = csv.writer(file) 
        write.writerows(phantom_chrome_output)

    os.remove(output_path)