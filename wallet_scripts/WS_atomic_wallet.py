#Generic Imports
import sys
import os
import json
import csv
import pathlib

#CCL Imports
import ccl_chrome_ldb_scripts.ccl_leveldb


ENCODING = "iso-8859-1"

def atomic_wallet_dump(ask_dir, output_dir):
    data = []

    output_path = ask_dir + r"\atomic_wallet_LDB.csv"

    leveldb_records = ccl_chrome_ldb_scripts.ccl_leveldb.RawLevelDb(ask_dir + r"\Roaming\atomic\Local Storage\leveldb")

    location = (ask_dir + "/Roaming/atomic/Local Storage")

    with open(output_path, "w", encoding="utf-8", newline="") as file1:
        writes = csv.writer(file1, quoting=csv.QUOTE_ALL, escapechar='£')
        writes.writerow(
            [
                "key-hex", "key-text", "value-text", "origin_file"
            ])

        for record in leveldb_records.iterate_records_raw():
            writes.writerow([
                record.user_key.hex(" ", 1),
                record.user_key.decode(ENCODING, "replace"),
                record.value.decode(ENCODING, "replace"),
                str(record.origin_file)
            ])

    with open(output_path, encoding="UTF-8", errors="ignore") as f:
        reader = csv.reader(x.replace('\0','' ) for x in f)
        for row in reader:
            data.append(row)

        col_keyhex = [x[0] for x in data]
        col_valuetext = [x[2] for x in data]

        addresses_hex = "5f 66 69 6c 65 3a 2f 2f 00 01 61 64 64 72 65 73 73 65 73"
        index_addresses = col_keyhex.index(addresses_hex)
        index_valuetext = col_valuetext[index_addresses]
        stripped_index_valuetext = index_valuetext[1:]

        json_obj = json.loads(stripped_index_valuetext)

        atomic_output = []
        for i in json_obj:
            if i["address"] != "":
                atomic_output = [i["id"] + "," + i["address"] + "," + "Atomic Wallet", location]

    with open(output_dir + '/' + 'atomic_wallet_addresses.csv', 'w', newline='') as file:
        write = csv.writer(file)
        for i in json_obj:
            if i["address"] != "":
                atomic_output = [i["id"], i["address"], "Atomic Wallet", location]
                write.writerow(atomic_output)
    
    with open(output_dir + '/' + 'WalletSleuth_log.txt', 'a') as log_file:
        log_file.write('ACTION: (ATOMIC WALLET) - Addresses identified.\n')

    os.remove(output_path)
    