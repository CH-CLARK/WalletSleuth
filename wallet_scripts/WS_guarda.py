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

def guarda_chrome_dump(ask_dir, output_dir):
    chrome_user_data = ask_dir + "/Local/Google/Chrome/User Data"
    folders_list = os.listdir(chrome_user_data)

    #Checking profiles locations
    profiles_check = "Profile"
    profiles_list = [idx for idx in folders_list if idx.lower().startswith(profiles_check.lower())]
    profiles_list_len = len(profiles_list)

    #Checking default location
    default_check = "Default"
    default_list = [idx for idx in folders_list if idx.lower().startswith(default_check.lower())]

    output_path = ask_dir + r"\Guarda_chrome_LDB.csv"
    guarda_chrome_output = []

    if default_list:
        leveldb_records = ccl_chrome_ldb_scripts.ccl_leveldb.RawLevelDb(ask_dir + r"\Local\Google\Chrome\User Data\Default\Local Extension Settings\hpglfhgfnhbgpjdenjgmdgoeiappafln")
        def_location = ask_dir + "/Local/Google/Chrome/User Data/Default/Local Extension Settings/hpglfhgfnhbgpjdenjgmdgoeiappafln"
        
        if leveldb_records:
            with open(output_path, "w", encoding="utf-8", newline="") as file1:
                writes = csv.writer(file1, quoting=csv.QUOTE_ALL)
                writes.writerow(
                    [
                        "key-hex", "value-text", "seq"
                    ])

                for record in leveldb_records.iterate_records_raw():
                    writes.writerow([
                        record.user_key.hex(" ", 1),
                        record.value.decode(ENCODING, "replace"),
                        record.seq,
                    ])

            #Identifies specific values in LDB for correct address identification
            data_hex = "64 61 74 61"
            with open(output_path, newline="") as csvfile:
                dataone = csv.DictReader(csvfile)
                max_seq_list = []
                for row in dataone:
                    max_seq_list.append(int(row["seq"]))
                    max_seq = max(max_seq_list)

                csvfile.seek(0)
                
                for row in dataone:
                    if row['key-hex'] == data_hex and 'defaultWallet' in row['value-text'] and int(row['seq']) == max_seq:
                        most_recent_valuetext = row['value-text']

            json_obj = json.loads(most_recent_valuetext)

            data = json_obj.get('data')
            wallet_data = data['wallets']

            for x in range(len(wallet_data)):
                guarda_address_output = wallet_data[x]['currency'], wallet_data[x]['address'], 'Guarda (Chrome)', def_location

                guarda_chrome_output.append(guarda_address_output)


    with open(output_dir + '/' + 'WalletSleuth_log.txt', 'a') as log_file:
        log_file.write('ACTION: (GUARDA - CHROME) - Addresses identified in Default Profile.\n')

    with open(output_dir + '/' + 'guarda_chrome_addresses.csv', 'w', newline='') as file:
        write = csv.writer(file) 
        write.writerows(guarda_chrome_output)

    
    os.remove(output_path)

    if profiles_list:
        print('THIS IS TO DO')
        #TODO!