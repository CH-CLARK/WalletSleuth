SUPPORTED_OPERATING_SYSTEMS = ['Windows', 'Mac']
SUPPORTED_BROWSERS = None
DEPENDENCIES = None
WALLET_METADATA = {
    'name': 'Exodus',
    'description': """Exodus is a non-custodial desktop wallet that supports various cryptocurrencies and tokens. Users are able to easily send and recieve cryptocurrency using the platform. 
                    Currently Wallet Sleuth is only able to parse transaction ID's from the Exodus wallet.""",
    'websites': ['exodus.com'],
    'ext_id': None,
    'author': ['CH-CLARK'],
    'plugin-iteration': '1',
    'plugin-last-update':'2025-09-29'
}

def exodus():
    try:
        from routes.config import configuration
        from ccl_scripts.ccl_chromium_reader import ccl_chromium_cache

        import brotli
        import hashlib
        import itertools
        import mimetypes
        import gzip
        import zlib
        import inspect
        import os
        import csv
    
    except ImportError as e:
        import_catch = f'ERROR: Exodus - {e} identified! Execution aborted!'
        pass

    # user set varibless
    operating_system = configuration.OS_SELECTION
    directory_path = configuration.DIRECTORY_PATH
    output_path = configuration.OUTPUT_PATH

    logging_output = os.path.join(output_path, 'wallet_sleuth_logging.txt')

    try:
        if import_catch:
            with open(logging_output, 'a') as log_file:
                log_file.write(f'\n{import_catch}')
            return
    except:
        pass

    if operating_system == 'windows':
        user_data_subdir = "/AppData"
        directory_path = directory_path + user_data_subdir
        data_location = f"{directory_path}/Roaming/Exodus/Partitions/main/Cache/Cache_Data"

    if operating_system == 'mac':
        user_data_subdir = "/Library"
        directory_path = directory_path + user_data_subdir
        data_location = f"{directory_path}/Application Support/Exodus/Partitions/main/Cache/Cache_Data"

    function_name = inspect.currentframe().f_code.co_name

    default_row_headers = ["file_hash", "key", "request_time", "response_time", "date", "content-type"]
    
    cache_result = []
    rows = []
    identified_paths = []
    result = []

    if os.path.exists(data_location):
        identified_paths.append(data_location)
        cache_type = ccl_chromium_cache.guess_cache_class(data_location)

        if cache_type is None:
            pass

        with cache_type(data_location) as cache:
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
                            output_string = "Transaction ID", text_between, tx_string, "Exodus", data_location.replace("\\","/")
                            cache_result.append(output_string)
        
        for i in cache_result:
            if i not in result:
                result.append(i)

    if not identified_paths:
        with open(logging_output, 'a') as log_file:
            log_file.write(f'\nERROR: Exodus - Wallet not found!')

    if result:
        header = 'Type', 'Currency', 'Address/Transaction', 'Wallet', 'Path'
        output_file = f'{function_name}_ws_output.csv'
        wallet_output_path = os.path.join(output_path, output_file)

        with open(wallet_output_path, 'w', newline='') as result_output:
            write = csv.writer(result_output, escapechar='*')
            write.writerow(header)
            write.writerows(result)  

        with open(logging_output, 'a') as log_file:
            log_file.write(f"\nACTION: {WALLET_METADATA.get('name')} - Addresses identified.")

    if identified_paths and not result:
        with open(logging_output, 'a') as log_file:
            log_file.write(f"\nACTION: {WALLET_METADATA.get('name')} - No addresses identified.")