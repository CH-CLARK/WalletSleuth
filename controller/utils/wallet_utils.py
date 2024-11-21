from ccl_scripts.ccl_chromium_reader.storage_formats import ccl_leveldb


browser_dict = {
    'Brave': '/Local/BraveSoftware/Brave-Browser/User Data',
    'Chrome': '/Local/Google/Chrome/User Data',
    'Edge': '/Local/Microsoft/Edge/User Data',
    'Opera': '/Roaming/Opera Software/Opera Stable'

}


def extract_leveldb_data(appdata_dir, data_location):
    encoding = "iso-8859-1"

    leveldb_records = ccl_leveldb.RawLevelDb(f"{appdata_dir}{data_location}")
    location = f"{appdata_dir}{data_location}"

    csv_data = []
 
    csv_data.append([
        "key-hex", "key-text", "value-text", "seq"
    ])

    for record in leveldb_records.iterate_records_raw():
        csv_data.append([
            record.user_key.hex(" ", 1),
            record.user_key.decode(encoding, "replace"),
            record.value.decode(encoding, "replace"),
            record.seq
        ])

    return csv_data, location

