#generic
import csv
import hashlib
import itertools
import mimetypes
import gzip
import zlib

try:
    import brotli
except:
    pass

#controller
import controller.config

#CCL Imports
import ccl_chrome_ldb_scripts.ccl_chromium_cache

def exodus_wallet():
    appdata_dir = controller.config.APPDATA
    output_dir = controller.config.OUTPUT
    log_name = controller.config.WS_MAIN_LOG_NAME

    in_cache_dir = appdata_dir + "/Roaming/Exodus/Partitions/main/Cache/Cache_Data"

    output_path = output_dir

    default_row_headers = ["file_hash", "key", "request_time", "response_time", "date", "content-type"]
    rows = []
    filtered_rows = []

    cache_type = ccl_chrome_ldb_scripts.ccl_chromium_cache.guess_cache_class(in_cache_dir)
    if cache_type is None:
        pass

    with cache_type(in_cache_dir) as cache:

        for key in cache.keys():
            out_extension = ""
            content_encoding = ""
            row = {"key": key}
            rows.append(row)

            metas = cache.get_metadata(key)
            datas = cache.get_cachefile(key)

            for meta, data in itertools.zip_longest(metas, datas, fillvalue=None):
                if meta is not None:
                    row["request_time"] = meta.request_time
                    row["response_time"] = meta.response_time
                    for attribute, value in meta.http_header_attributes:
                        if attribute in default_row_headers:
                            row[attribute] = value

                    if mime := meta.get_attribute("content-type"):
                        out_extension = mimetypes.guess_extension(mime[0]) or ""

                    content_encoding = (meta.get_attribute("content-encoding") or [""])[0]

                if data is not None:
                    if content_encoding.strip() == "gzip":
                        data = gzip.decompress(data)
                    elif content_encoding.strip() == "br":
                        data = brotli.decompress(data)
                    elif content_encoding.strip() == "deflate":
                        data = zlib.decompress(data, -zlib.MAX_WBITS)
                    elif content_encoding.strip() != "":
                        pass

                    h = hashlib.sha256()
                    h.update(data)
                    cache_file_hash = h.hexdigest()
                    row["file_hash"] = cache_file_hash
                else:
                    row["file_hash"] = "<No cache file data>"

                if "key" in row and "insight/tx" in row["key"]:
                    tx_string = row["key"].split("insight/tx")[1].strip("/")
                    start_index = row["key"].find("://")
                    end_index = row["key"].find(".a")
                    if start_index != -1 and end_index != -1:
                        text_between = row["key"][start_index + 3:end_index]
                        filtered_rows.append({"text_between": text_between, "tx_string": tx_string})

    if not filtered_rows:
        with open(output_path + "/" "exodus_wallet_output.csv", "w", newline="") as csv_filtered_out_f:
            csv_filtered_out = csv.writer(csv_filtered_out_f, dialect=csv.excel, quoting=csv.QUOTE_ALL)
            
            for row in filtered_rows:
                csv_filtered_out.writerow(["Transaction ID"] + list(row.values()) + ["Exodus Wallet", str(in_cache_dir)])

        with open(output_dir + '/' + log_name, 'a') as log_file:
            log_file.write('ACTION: Exodus Wallet - No Transactions Identified \n')
    
    if filtered_rows:
        with open(output_path + "/" "exodus_wallet_output.csv", "w", newline="") as csv_filtered_out_f:
            csv_filtered_out = csv.writer(csv_filtered_out_f, dialect=csv.excel, quoting=csv.QUOTE_ALL)
            
            for row in filtered_rows:
                csv_filtered_out.writerow(["Transaction ID"] + list(row.values()) + ["Exodus Wallet", str(in_cache_dir)])

        with open(output_dir + '/' + log_name, 'a') as log_file:
            log_file.write('ACTION: Exodus Wallet - Transactions Identified.\n')