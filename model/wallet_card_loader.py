#generic imports
import sys
import os
import ast

#utils imports
from utils.pyinstaller_utils import resource_path

def load_wallet_metadata(wallet_dir='wallet_scripts'):

    wallet_dir = resource_path(wallet_dir)

    metadata_list = []

    for root, _, files in os.walk(wallet_dir):
        for file in files:
            if file.startswith('__'):
                continue

            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        source = f.read()
                    tree = ast.parse(source)
                    for node in tree.body:
                        if isinstance(node, ast.Assign):
                            for target in node.targets:
                                if isinstance(target, ast.Name) and target.id == 'WALLET_METADATA':
                                    metadata = ast.literal_eval(node.value)
                                    metadata['source'] = os.path.relpath(filepath, wallet_dir)
                                    metadata_list.append(metadata)
                except Exception as e:
                    print(f"ERROR: wallet_card_loader.py - {e}")
                    pass

    metadata_list.sort(key=lambda m: m.get('name', '').lower())
    return metadata_list
