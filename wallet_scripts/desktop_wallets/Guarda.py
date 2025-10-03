SUPPORTED_OPERATING_SYSTEMS = ['Windows']
SUPPORTED_BROWSERS = None
DEPENDENCIES = None
WALLET_METADATA = {
    'name': 'Guarda',
    'description': """Guarda is a non-custodial desktop wallet that supports various cryptocurrencies and tokens. 
                    Users are able to easily send and recieve cryptocurrency using the platform. A noted limitation is that during the testing, it was not possible to identify the users Monero address.""",
    'websites': ['guarda.com/desktop/'],
    'ext_id': None,
    'author': ['CH-CLARK'],
    'plugin-iteration': '1',
    'plugin-last-update':'2025-09-29'
}

def guarda():
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
        import_catch = f'ERROR: Guarda - {e} identified! Execution aborted!'
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
        data_location = f"{directory_path}/Roaming/Guarda/Cache"

    # if operating_system == 'mac':
    #     user_data_subdir = "/Library"
    #     directory_path = directory_path + user_data_subdir
    #     data_location = f"{directory_path}/Application Support/Guarda/Partitions/main/Cache/Cache_Data"

    function_name = inspect.currentframe().f_code.co_name

    default_row_headers = ["file_hash", "key", "request_time", "response_time", "date", "content-type"]
    
    identified_addresses = []
    addresses_result = []
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

                    if "key" in row and "/api/v1/balances" in row["key"]:
                        addy_string = row["key"].split("/api/v1/balances")[1].strip("/")
                        identified_addresses.append(addy_string)
                        identified_addresses = [item for item in identified_addresses if "?" not in item.split("/")[1]]

            for item in identified_addresses:
                currency, address = item.split("/",1)
                output_string = "Address", currency, address, "Guarda", data_location.replace("\\","/")
                result.append(output_string)
    
    if not identified_paths:
        with open(logging_output, 'a') as log_file:
            log_file.write(f'\nERROR: Guarda - Wallet not found!')

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