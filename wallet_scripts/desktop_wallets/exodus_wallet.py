#generic
import csv
import hashlib
import itertools
import mimetypes
import gzip
import zlib
import inspect

try:
    import brotli
except:
    pass

#controller
import controller.config

#CCL Imports
from ccl_scripts.ccl_chromium_reader import ccl_chromium_cache


def exodus_wallet():
    appdata_dir = controller.config.APPDATA
    output_dir = controller.config.OUTPUT
    log_name = controller.config.WS_MAIN_LOG_NAME

    function_name = inspect.currentframe().f_code.co_name
    wallet_name = function_name.split('_')[0].capitalize()

    in_cache_dir = appdata_dir + "/Roaming/Exodus/Partitions/main/Cache/Cache_Data"

    output_path = output_dir

    default_row_headers = ["file_hash", "key", "request_time", "response_time", "date", "content-type"]
    result = []
    rows = []

    cache_type = ccl_chromium_cache.guess_cache_class(in_cache_dir)

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
                        result.append({"text_between": text_between, "tx_string": tx_string})

    if result:
        with open(f'{output_path}/{wallet_name.lower()}_wallet_output.csv', 'w', newline='') as results_output:
            write = csv.writer(results_output, dialect=csv.excel, quoting=csv.QUOTE_ALL)
            
            for row in result:
                write.writerow(["Transaction ID"] + list(row.values()) + [wallet_name, str(in_cache_dir)])

        with open(f'{output_dir}/{log_name}', 'a') as log_file:
            log_file.write(f'ACTION: {wallet_name} - Transactions Identified.\n')


    if not result:
        with open(f'{output_path}/{log_name}', 'a') as log_file:
            log_file.write(f'ACTION: {wallet_name} - No Transactions Identified \n')