# generic imports
import os
import sys
import importlib

#utils imports
from utils.pyinstaller_utils import resource_path

wallets_root_dir = resource_path("wallet_scripts")

windows_wallets_list = {}
mac_wallets_list = {}

# new dict to store folder/path for each wallet
wallets_folders = {}

for dirpath, dirnames, filenames in os.walk(wallets_root_dir):
    for filename in filenames:
        if filename.endswith('.py') and not filename.startswith('__'):
            relative_path = os.path.relpath(dirpath, os.path.dirname(wallets_root_dir))
            script_path = os.path.join(relative_path, filename[:-3]).replace(os.sep, '.')

            try:
                wallet_script = importlib.import_module(script_path)
            except Exception as e:
                # print(f"ERROR: wallets_list.py -  importing {script_path}: {e}") #kept for logging
                continue
            
            # read wallet script globals
            operating_system = getattr(wallet_script, 'SUPPORTED_OPERATING_SYSTEMS', [])
            browsers = getattr(wallet_script, 'SUPPORTED_BROWSERS', None)
            dependencies = getattr(wallet_script, 'DEPENDENCIES', [])

            # this try and except allows for DEPENDANCIES to be none
            skip_wallet = False
            
            try:
                for dep in dependencies:
                    try:
                        importlib.import_module(dep)
                    except ImportError:
                        print(f'ERROR: wallet_list.py - {e} in path {script_path}! Wallet removed from "Wallet Selection" list.')
                        skip_wallet = True
                        break
            except Exception:
                pass

            if skip_wallet:
                continue

            relative_path_to_root = os.path.relpath(dirpath, wallets_root_dir)
            if relative_path_to_root != '.':
                subdir_name = relative_path_to_root.replace(os.sep, '_')
                wallet_name = f"{filename[:-3].replace('_', ' ')}-{subdir_name}"
            else:
                wallet_name = filename[:-3].replace('_', ' ')

            def get_browsers_for_os(target_os):
                if isinstance(browsers, dict):
                    return set(browsers.get(target_os, [])) or None
                elif isinstance(browsers, list):
                    return set(browsers) if browsers else None
                else:
                    return None

            if 'Windows' in operating_system:
                windows_wallets_list[wallet_name] = get_browsers_for_os('Windows')
                wallets_folders[wallet_name] = dirpath

            if 'Mac' in operating_system:
                mac_wallets_list[wallet_name] = get_browsers_for_os('Mac')
                wallets_folders[wallet_name] = dirpath

# sort the final dictionaries
windows_wallets_list = dict(sorted(windows_wallets_list.items()))
mac_wallets_list = dict(sorted(mac_wallets_list.items()))
wallets_folders = dict(sorted(wallets_folders.items()))