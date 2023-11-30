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

def bitkeep_chrome():
    appdata_dir = controller.config.APPDATA
    output_dir = controller.config.OUTPUT

    chrome_user_data = appdata_dir + "/Local/Google/Chrome/User Data"
    folders_list = os.listdir(chrome_user_data)

    #Checking profiles locations
    profiles_check = "Profile"
    profiles_list = [idx for idx in folders_list if idx.lower().startswith(profiles_check.lower())]
    profiles_list_len = len(profiles_list)
    
    #Checking default location
    default_check = "Default"
    default_list = [idx for idx in folders_list if idx.lower().startswith(default_check.lower())]

    output_path = output_dir + r"\BK_chrome_LDB.csv"
    bitkeep_chrome_output = []

    if profiles_list:
        for x in range(profiles_list_len):
            profiles_ldb_loc = appdata_dir + "/Local/Google/Chrome/User Data/" + profiles_list[x] + "/Local Extension Settings/jiidiaalihmmhddjgbnbgdfflelocpak"
            
            if profiles_ldb_loc:
                try:
                    leveldb_records = ccl_chrome_ldb_scripts.ccl_leveldb.RawLevelDb(profiles_ldb_loc)

                    with open(output_path, "w", encoding="utf-8", newline="") as file1:
                        writes = csv.writer(file1, quoting=csv.QUOTE_ALL)
                        writes.writerow(
                            [
                                "key-text", "value-text", "seq"
                            ])

                        for record in leveldb_records.iterate_records_raw():
                            writes.writerow([
                                record.user_key.decode(ENCODING, "replace"),
                                record.value.decode(ENCODING, "replace"),
                                record.seq,
                            ])

                    data_text = "accounts"
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
                    

                    currency_data = json_obj.get('currency')

                    for x in range(len(currency_data)):
                        bk_address_output = currency_data[x]['symbol'], currency_data[x]['address'], 'Bitkeep (Chrome)', profiles_ldb_loc
                        bitkeep_chrome_output.append(bk_address_output)


                    with open(output_dir + '/' + 'bitkeep_chrome_addresses.csv', 'w', newline='') as file:
                        write = csv.writer(file) 
                        write.writerows(bitkeep_chrome_output)  
                
                except:
                    pass

    if default_list:
        leveldb_records = ccl_chrome_ldb_scripts.ccl_leveldb.RawLevelDb(appdata_dir + r"\Local\Google\Chrome\User Data\Default\Local Extension Settings\jiidiaalihmmhddjgbnbgdfflelocpak") 
        def_location = appdata_dir + "/Local/Google/Chrome/User Data/Default/Local Extension Settings/jiidiaalihmmhddjgbnbgdfflelocpak"
        
        if leveldb_records:
            with open(output_path, "w", encoding="utf-8", newline="") as file1:
                writes = csv.writer(file1, quoting=csv.QUOTE_ALL)
                writes.writerow(
                    [
                        "key-text", "value-text", "seq"
                    ])

                for record in leveldb_records.iterate_records_raw():
                    writes.writerow([
                        record.user_key.decode(ENCODING, "replace"),
                        record.value.decode(ENCODING, "replace"),
                        record.seq,
                    ])

            data_text = "accounts"
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
            
            currency_data = json_obj.get('currency')

            for x in range(len(currency_data)):
                
                bk_address_output = currency_data[x]['symbol'], currency_data[x]['address'] ,'Bitkeep (Chrome)', def_location
                
                bitkeep_chrome_output.append(bk_address_output) 

        with open(output_dir + '/' + 'bitkeep_chrome_addresses.csv', 'w', newline='') as file:
            write = csv.writer(file) 
            write.writerows(bitkeep_chrome_output)

    os.remove(output_path)

def bitkeep_brave():
    appdata_dir = controller.config.APPDATA
    output_dir = controller.config.OUTPUT

    brave_user_data = appdata_dir + "/Local/BraveSoftware/Brave-Browser/User Data"
    folders_list = os.listdir(brave_user_data)

    #Checking profiles locations
    profiles_check = "Profile"
    profiles_list = [idx for idx in folders_list if idx.lower().startswith(profiles_check.lower())]
    profiles_list_len = len(profiles_list)
    
    #Checking default location
    default_check = "Default"
    default_list = [idx for idx in folders_list if idx.lower().startswith(default_check.lower())]

    output_path = output_dir + r"\BK_brave_LDB.csv"
    bitkeep_brave_output = []

    if profiles_list:
        for x in range(profiles_list_len):
            profiles_ldb_loc = appdata_dir + "/Local/BraveSoftware/Brave-Browser/User Data/" + profiles_list[x] + "/Local Extension Settings/jiidiaalihmmhddjgbnbgdfflelocpak"
            
            if profiles_ldb_loc:
                try:
                    leveldb_records = ccl_chrome_ldb_scripts.ccl_leveldb.RawLevelDb(profiles_ldb_loc)

                    with open(output_path, "w", encoding="utf-8", newline="") as file1:
                        writes = csv.writer(file1, quoting=csv.QUOTE_ALL)
                        writes.writerow(
                            [
                                "key-text", "value-text", "seq"
                            ])

                        for record in leveldb_records.iterate_records_raw():
                            writes.writerow([
                                record.user_key.decode(ENCODING, "replace"),
                                record.value.decode(ENCODING, "replace"),
                                record.seq,
                            ])

                    data_text = "accounts"
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

                    currency_data = json_obj.get('currency')

                    for x in range(len(currency_data)):
                        bk_address_output = currency_data[x]['symbol'], currency_data[x]['address'], 'Bitkeep (Brave)', profiles_ldb_loc
                        bitkeep_brave_output.append(bk_address_output)


                    with open(output_dir + '/' + 'bitkeep_brave_addresses.csv', 'w', newline='') as file:
                        write = csv.writer(file) 
                        write.writerows(bitkeep_brave_output)  
                
                except Exception as e:
                    pass

    if default_list:
        leveldb_records = ccl_chrome_ldb_scripts.ccl_leveldb.RawLevelDb(appdata_dir + r"\Local\BraveSoftware\Brave-Browser\User Data\Default\Local Extension Settings\jiidiaalihmmhddjgbnbgdfflelocpak") 
        def_location = appdata_dir + "/Local/BraveSoftware/Brave-Software/User Data/Default/Local Extension Settings/jiidiaalihmmhddjgbnbgdfflelocpak"

        if leveldb_records:
            with open(output_path, "w", encoding="utf-8", newline="") as file1:
                writes = csv.writer(file1, quoting=csv.QUOTE_ALL)
                writes.writerow(
                    [
                        "key-text", "value-text", "seq"
                    ])

                for record in leveldb_records.iterate_records_raw():
                    writes.writerow([
                        record.user_key.decode(ENCODING, "replace"),
                        record.value.decode(ENCODING, "replace"),
                        record.seq,
                    ])

            data_text = "accounts"
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
            
            currency_data = json_obj.get('currency')

            for x in range(len(currency_data)):
                
                bk_address_output = currency_data[x]['symbol'], currency_data[x]['address'] ,'Bitkeep (Brave)', def_location
                
                bitkeep_brave_output.append(bk_address_output)

        with open(output_dir + '/' + 'bitkeep_Brave_addresses.csv', 'w', newline='') as file:
            write = csv.writer(file) 
            write.writerows(bitkeep_brave_output)

    os.remove(output_path)