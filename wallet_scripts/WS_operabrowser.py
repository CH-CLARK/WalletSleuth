#Generic Imports
import sys
import os
import json
import csv
import pathlib
import ast

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


def operabrowser_dump(ask_dir,output_dir):
    operabrowser_user_data = ask_dir + "/Roaming/Opera Software/Opera Stable/Local Extension Settings/gojhcdgcpbpfigcaejpfhfegekdgiblk"

    if operabrowser_user_data:
        output_data = []

        output_path = ask_dir + r"\operabrowser_wallet_LDB.csv"

        leveldb_records = ccl_chrome_ldb_scripts.ccl_leveldb.RawLevelDb(ask_dir + "/Roaming/Opera Software/Opera Stable/Local Extension Settings/gojhcdgcpbpfigcaejpfhfegekdgiblk")

        location = (ask_dir + "/Roaming/Opera Software/Opera Stable/Local Extension Settings/gojhcdgcpbpfigcaejpfhfegekdgiblk")

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
        ammended_json_obj = ast.literal_eval(json_obj)

        for key, value in ammended_json_obj.items():
            if value["coinType"] == 0:
                btc = ("BTC", key, "Opera Browser Wallet", operabrowser_user_data)
                output_data.append(btc)
            elif value["coinType"] == 60:
                eth = ("ETH", key, "Opera Browser Wallet", operabrowser_user_data)
                output_data.append(eth)
            elif value["coinType"] == 501:
                sol = ("SOL", key, "Opera Browser Wallet", operabrowser_user_data)
                output_data.append(sol)
            elif value["coinType"] == 397:
                near = ("NEAR", key, "Opera Browser Wallet", operabrowser_user_data)
                output_data.append(near)
            elif value["coinType"] == 235:
                fio = ("FIO", key, "Opera Browser Wallet", operabrowser_user_data)
                output_data.append(fio)
            elif value["coinType"] == 508:
                egld = ("EGLD", key, "Opera Browser Wallet", operabrowser_user_data)
                output_data.append(egld)

        with open(output_dir + '/' + 'WalletSleuth_log.txt', 'a') as log_file:
            log_file.write('ACTION: (OPERA) - Addresses identified. \n')

    with open(output_dir + '/' + 'operabrowser_addresses.csv', 'w', newline='') as output_file:
        write = csv.writer(output_file)
        write.writerows(output_data)

    os.remove(output_path)