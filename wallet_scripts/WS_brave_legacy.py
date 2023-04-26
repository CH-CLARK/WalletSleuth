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

def brave_legacy_dump(ask_dir, output_dir):
    brave_user_data = ask_dir + "/Local/BraveSoftware/Brave-Browser/User Data"
    folders_list = os.listdir(brave_user_data)

    #Checking profiles locations
    profiles_check  = "Profile"
    profiles_list = [idx for idx in folders_list if idx.lower().startswith(profiles_check.lower())]
    profiles_list_len = len(profiles_list)

    #Checking default location
    default_check = "Default"
    default_list = [idx for idx in folders_list if idx.lower().startswith(default_check.lower())]


    output_path = ask_dir + r"\MM_brave_legacy_LDB.csv"
    metamask_brave_output = []


    if profiles_list:

        for x in range(profiles_list_len):
            profiles_ldb_loc = ask_dir + "/Local/BraveSoftware/Brave-Browser/User Data/" + profiles_list[x] + "/Local Extension Settings/odbfpeeihdkbihmopkbjmoonfanlbfcl"

            if profiles_ldb_loc:
                try:
                    leveldb_records = ccl_chrome_ldb_scripts.ccl_leveldb.RawLevelDb(profiles_ldb_loc)
            
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
                            if row['key-hex'] == data_hex and 'AlertController' in row['value-text'] and int(row['seq']) == max_seq:
                                
                                most_recent_valuetext = row['value-text']
                    
                    json_obj = json.loads(most_recent_valuetext)
                    
                    pref_controller_data = json_obj.get('PreferencesController')
                    identities_data = pref_controller_data["identities"]


                    #Writing identified data to CSV
                    for key in identities_data:
                        new_variable = identities_data[key]
                        metamask_address = new_variable["address"]
                        default_output = 'VARIOUS - See Documention!', metamask_address, 'Brave Legacy Extension (Brave)', profiles_ldb_loc
                        metamask_brave_output.append(default_output)
                    
                    with open(output_dir + '/' + 'MM_brave_legacy_addresses.csv', 'a', newline='') as file:
                        write = csv.writer(file) 
                        write.writerow(metamask_brave_output)

                    with open(output_dir + '/' + 'WalletSleuth_log.txt', 'a') as log_file:
                        log_file.write('ACTION: (BRAVE LEGACY EXTENSION - BRAVE) - Addresses identified in ' +  profiles_list[x] + '.\n')     
                
                except Exception:
                    pass

    if default_list:

        leveldb_records = ccl_chrome_ldb_scripts.ccl_leveldb.RawLevelDb(ask_dir + r"\Local\BraveSoftware\Brave-Browser\User Data\Default\Local Extension Settings\odbfpeeihdkbihmopkbjmoonfanlbfcl") 
        def_location = ask_dir + "/Local/BraveSoftware/Brave-Browser/User Data/Default/Local Extension Settings/odbfpeeihdkbihmopkbjmoonfanlbfcl"
        
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
                    if row['key-hex'] == data_hex and 'AlertController' in row['value-text'] and int(row['seq']) == max_seq:
                        most_recent_valuetext = row['value-text']
            
            json_obj = json.loads(most_recent_valuetext)
            
            pref_controller_data = json_obj.get('PreferencesController')
            identities_data = pref_controller_data["identities"]

            #Writing identified data to CSV
            for key in identities_data:
                new_variable = identities_data[key]
                metamask_address = new_variable["address"]
                profiles_output = 'VARIOUS - See Documention!', metamask_address, 'Brave Legacy Extension (Brave)', def_location
                metamask_brave_output.append(profiles_output)


    with open(output_dir + '/' + 'WalletSleuth_log.txt', 'a') as log_file:
        log_file.write('ACTION: (BRAVE LEGACY EXTENSION - BRAVE) - Addresses identified in Default Profile.\n')

    with open(output_dir + '/' + 'MM_brave_legacy_addresses.csv', 'w', newline='') as file:
        write = csv.writer(file) 
        write.writerows(metamask_brave_output)

    os.remove(output_path)