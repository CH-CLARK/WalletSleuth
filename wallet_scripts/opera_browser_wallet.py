#generic imports
import csv
import json
import os
import sys
import ast

#controller imports
import controller.config

#CCL Imports
import ccl_chrome_ldb_scripts.ccl_leveldb

# Handling large CSV fields
maxInt = sys.maxsize
while True:
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

ENCODING = "iso-8859-1"

def opera_wallet():
    appdata_dir = controller.config.APPDATA
    output_dir = controller.config.OUTPUT
    log_name = controller.config.WS_MAIN_LOG_NAME

    operabrowser_user_data = os.path.join(appdata_dir + "/Roaming/Opera Software/Opera Stable/default/Local Extension Settings/gojhcdgcpbpfigcaejpfhfegekdgiblk")

    if operabrowser_user_data:
        output_data = []

        output_path = os.path.join(appdata_dir, "operabrowser_wallet_LDB.csv")

        leveldb_records = ccl_chrome_ldb_scripts.ccl_leveldb.RawLevelDb(operabrowser_user_data)

        with open(output_path, "w", encoding="utf-8", newline="") as file1:
            writes = csv.writer(file1, quoting=csv.QUOTE_ALL, escapechar='£')
            writes.writerow(
                [
                    "key-hex", "key-text", "value-text", "seq"
                ])

            for record in leveldb_records.iterate_records_raw():
                writes.writerow([
                    record.user_key.hex(" ", 1),
                    record.user_key.decode(ENCODING, "replace"),
                    record.value.decode(ENCODING, "replace"),
                    record.seq,
                ])

        data_text = "wallet-accounts"
        with open(output_path, newline="", errors='ignore') as csvfile:
            dataone = csv.DictReader(csvfile)

            accounts_seq_list = []
            for row in dataone:
                if row['key-text'] == data_text:
                    accounts_seq_list.append(int(row["seq"]))
            
            #this sorts the sequence numbers into decending order... this needs to be done since the highest sequence may not always be populated. might have to update the others with this...
            accounts_seq_list.sort(reverse=True)

            most_recent_valuetext = None

            for seq in accounts_seq_list:
                csvfile.seek(0)

                for row in dataone:
                    if row['key-text'] == data_text and int(row['seq']) == seq:
                        most_recent_valuetext = row['value-text']

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
                    btc = ("Extended Public Key (XPUB)", "BTC", key, "Opera Browser Wallet", operabrowser_user_data)
                    output_data.append(btc)
                elif value["coinType"] == 60:
                    eth = ("Address", "ETH", key, "Opera Browser Wallet", operabrowser_user_data)
                    output_data.append(eth)
                elif value["coinType"] == 501:
                    sol = ("Address", "SOL", key, "Opera Browser Wallet", operabrowser_user_data)
                    output_data.append(sol)
                elif value["coinType"] == 397:
                    near = ("Address", "NEAR", key, "Opera Browser Wallet", operabrowser_user_data)
                    output_data.append(near)
                elif value["coinType"] == 235:
                    fio = ("Address", "FIO", key, "Opera Browser Wallet", operabrowser_user_data)
                    output_data.append(fio)
                elif value["coinType"] == 508:
                    egld = ("Address", "EGLD", key, "Opera Browser Wallet", operabrowser_user_data)
                    output_data.append(egld)

    with open(os.path.join(output_dir, 'opera_browser_wallet_output.csv'), 'w', newline='') as output_file:
        write = csv.writer(output_file)
        write.writerows(output_data)

    with open(os.path.join(output_dir, log_name), 'a') as log_file:
        log_file.write('ACTION: Opera Browser Wallet - Addresses Identified.\n')

    os.remove(output_path)


