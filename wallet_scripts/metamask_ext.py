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

def metamask_chrome():
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

    output_path = output_dir + r"\MM_chrome_LDB.csv"
    metamask_chrome_output = []

    if profiles_list:
        for x in range(profiles_list_len):
            profiles_ldb_loc = appdata_dir + "/Local/Google/Chrome/User Data/" + profiles_list[x] + "/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn"

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
                        profiles_output = 'Address', 'VARIOUS - See Documention!', metamask_address, 'MetaMask (Chrome)', profiles_ldb_loc
                        metamask_chrome_output.append(profiles_output)

                    with open(output_dir + '/' + 'metamask_chrome_addresses.csv', 'w', newline='') as file:
                        write = csv.writer(file)
                        write.writerows(metamask_chrome_output)

                except Exception as e:
                    pass

    if default_list:

        leveldb_records = ccl_chrome_ldb_scripts.ccl_leveldb.RawLevelDb(appdata_dir + r"\Local\Google\Chrome\User Data\Default\Local Extension Settings\nkbihfbeogaeaoehlefnkodbefgpgknn") 
        def_location = appdata_dir + "/Local/Google/Chrome/User Data/Default/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn"

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
                profiles_output = 'Address', 'VARIOUS - See Documention!', metamask_address, 'MetaMask (Chrome)', def_location
                metamask_chrome_output.append(profiles_output)

    
#this should check for identifies data and if the length of the string is 0, it wil inform the user that no addessses exist. the reason for this is i noticed that a user might have MM installed, but never have opened it
        if len(identities_data) == 0:
            with open(output_dir + '/' + 'WalletSleuth_log.txt', 'a') as log_file:
                log_file.write('ACTION: Metamask (Chrome) - No Addresses Identified.\n')    
    
        else:
            with open(output_dir + '/' + 'metamask_chrome_addresses.csv', 'w', newline='') as file:
                write = csv.writer(file) 
                write.writerows(metamask_chrome_output)

            with open(output_dir + '/' + 'WalletSleuth_log.txt', 'a') as log_file:
                log_file.write('ACTION: Metamask (Chrome) - Addresses Identified.\n')            

    os.remove(output_path)

def metamask_edge():
    appdata_dir = controller.config.APPDATA
    output_dir = controller.config.OUTPUT

    edge_user_data = appdata_dir + "/Local/Microsoft/Edge/User Data"
    folders_list = os.listdir(edge_user_data)

    #Checking profiles locations
    profiles_check = "Profile"
    profiles_list = [idx for idx in folders_list if idx.lower().startswith(profiles_check.lower())]
    profiles_list_len = len(profiles_list)
    
    #Checking default location
    default_check = "Default"
    default_list = [idx for idx in folders_list if idx.lower().startswith(default_check.lower())]

    output_path = output_dir + r"\MM_edge_LDB.csv"
    metamask_edge_output = []

    if profiles_list:
        for x in range(profiles_list_len):
            profiles_ldb_loc = appdata_dir + "/Local/Microsoft/Edge/User Data/" + profiles_list[x] + "/Local Extension Settings/ejbalbakoplchlghecdalmeeeajnimhm"

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
                        profiles_output = 'Address', 'VARIOUS - See Documention!', metamask_address, 'MetaMask (Edge)', profiles_ldb_loc
                        metamask_edge_output.append(profiles_output)

                    with open(output_dir + '/' + 'metamask_edge_addresses.csv', 'w', newline='') as file:
                        write = csv.writer(file)
                        write.writerows(metamask_edge_output)

                except Exception as e:
                    pass
    
    if default_list:

        leveldb_records = ccl_chrome_ldb_scripts.ccl_leveldb.RawLevelDb(appdata_dir + r"\Local\Microsoft\Edge\User Data\Default\Local Extension Settings\ejbalbakoplchlghecdalmeeeajnimhm") 
        def_location = appdata_dir + "/Local/Microsoft/Edge/User Data/Default/Local Extension Settings/ejbalbakoplchlghecdalmeeeajnimhm"

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
                default_output = 'Address', 'VARIOUS - See Documention!', metamask_address, 'MetaMask (Edge)', def_location
                metamask_edge_output.append(default_output)

#this should check for identifies data and if the length of the string is 0, it wil inform the user that no addessses exist. the reason for this is i noticed that a user might have MM installed, but never have opened it
        if len(identities_data) == 0:
            with open(output_dir + '/' + 'WalletSleuth_log.txt', 'a') as log_file:
                log_file.write('ACTION: Metamask (Brave) - No Addresses Identified.\n')    
    
        else:
            with open(output_dir + '/' + 'metamask_chrome_addresses.csv', 'w', newline='') as file:
                write = csv.writer(file) 
                write.writerows(metamask_edge_output)

            with open(output_dir + '/' + 'WalletSleuth_log.txt', 'a') as log_file:
                log_file.write('ACTION: Metamask (Edge) - Addresses Identified.\n')          

    os.remove(output_path)

def metamask_brave():
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

    output_path = output_dir + r"\MM_brave_LDB.csv"
    metamask_brave_output = []

    if profiles_list:
        for x in range(profiles_list_len):
            profiles_ldb_loc = appdata_dir + "/Local/BraveSoftware/Brave-Browser/User Data/" + profiles_list[x] + "/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn"
    
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
                        profiles_output = 'Address', 'VARIOUS - See Documention!', metamask_address, 'MetaMask (Brave)', profiles_ldb_loc
                        metamask_brave_output.append(profiles_output)

                    with open(output_dir + '/' + 'metamask_brave_addresses.csv', 'w', newline='') as file:
                        write = csv.writer(file)
                        write.writerows(metamask_brave_output)

                except Exception as e:
                    pass

    if default_list:
        leveldb_records = ccl_chrome_ldb_scripts.ccl_leveldb.RawLevelDb(appdata_dir + r"\Local\BraveSoftware\Brave-Browser\User Data\Default\Local Extension Settings\nkbihfbeogaeaoehlefnkodbefgpgknn") 
        def_location = appdata_dir + "/Local/BraveSoftware/Brave-Browser/User Data/Default/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn"

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
                default_output = 'Address', 'VARIOUS - See Documention!', metamask_address, 'MetaMask (Brave)', def_location
                metamask_brave_output.append(default_output)

#this should check for identifies data and if the length of the string is 0, it wil inform the user that no addessses exist. the reason for this is i noticed that a user might have MM installed, but never have opened it
        if len(identities_data) == 0:
            with open(output_dir + '/' + 'WalletSleuth_log.txt', 'a') as log_file:
                log_file.write('ACTION: Metamask (Brave) - No Addresses Identified.\n')    
    
        else:
            with open(output_dir + '/' + 'metamask_brave_addresses.csv', 'w', newline='') as file:
                write = csv.writer(file) 
                write.writerows(metamask_brave_output)

            with open(output_dir + '/' + 'WalletSleuth_log.txt', 'a') as log_file:
                log_file.write('ACTION: Metamask (Brave) - Addresses Identified.\n')        

    os.remove(output_path)
