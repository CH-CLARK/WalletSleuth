# generic imports
import os
import sys
import importlib
import inspect

#utils imports
from utils.pyinstaller_utils import resource_path

def load_wallet_functions(wallet_dirs):
    wallet_functions = {}

    # find root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    try:
        for wallet_dir in wallet_dirs:

            abs_wallet_dir = resource_path(wallet_dir)
            
            for root, subs_dirs, files in os.walk(abs_wallet_dir):
                for file in files:
                    if file.endswith(".py") and not file.startswith("__"):

                        full_path = os.path.join(root, file)
                        relative_path = os.path.relpath(full_path, project_root)
                        script_path = os.path.splitext(relative_path)[0].replace(os.sep, ".")

                        try:
                            script = importlib.import_module(script_path)

                            for name, obj in inspect.getmembers(script, inspect.isfunction):
                                if obj.__module__ == script.__name__:
                                    wallet_functions[name] = obj

                        except Exception as e:
                            print(f'ERROR: load_wallets.py - {e}')
                            pass

    except Exception as e:
        print(f'ERROR: load_wallets.py outer - {e}')
        pass

    return wallet_functions
