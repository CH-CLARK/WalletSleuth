#generic imports
import csv
import datetime

#tkinter imports
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import LEFT, W, messagebox

#controller imports
from controller.wallet_selector import Wallet_Selector
import controller.config

#wallet imports
from wallet_scripts.atomic_wallet import atomic_wallet
from wallet_scripts.metamask_ext import metamask_chrome, metamask_edge, metamask_brave
from wallet_scripts.bitkeep_ext import bitkeep_chrome, bitkeep_brave
from wallet_scripts.brave_browser_legacy import brave_legacy
from wallet_scripts.brave_browser_wallet import brave_wallet
from wallet_scripts.guarda_ext import guarda_chrome, guarda_opera
from wallet_scripts.opera_browser_wallet import opera_wallet
from wallet_scripts.ledger_live import ledger_live_wallet
from wallet_scripts.phantom_ext import phantom_chrome, phantom_brave
from wallet_scripts.exodus_wallet import exodus_wallet
from wallet_scripts.wasabi_wallet import wasabi_wallet
from wallet_scripts.litecoin_core_wallet import litecoin_core_wallet
from wallet_scripts.bitcoin_core_wallet import bitcoin_core_wallet
from wallet_scripts.coinbase_wallet_ext import coinbase_wallet_chrome, coinbase_wallet_brave
from wallet_scripts.cryptocom_wallet_ext import cryptocom_wallet_chrome

def process_wallet(wallet_name, browser_type, function, output_dir, log_file_path, selection):
    try:
        function()
        wallet_name = wallet_name.lower().replace(' ', '_')

        if browser_type:
            browser_type = browser_type.lower()
            csv_file = f"{output_dir}/{wallet_name}_{browser_type}_addresses.csv"

        else:
            csv_file = f"{output_dir}/{wallet_name}_addresses.csv"
        selection.append(csv_file)

    except Exception as e:
        messagebox.showerror('ERROR', f"ERROR: {wallet_name} ({browser_type}) - Wallet Not Found!")
        error_message = f"ERROR: {wallet_name} ({browser_type}) - Wallet Not Found!"

        with open(log_file_path, 'a') as log_file:
            log_file.write(f"{error_message}\n")


def run_func():
    try:
        appdata_dir = controller.config.APPDATA
        output_dir = controller.config.OUTPUT
        log_name = controller.config.WS_MAIN_LOG_NAME
        log_file_path = f"{output_dir}/{log_name}"

        #check directories set
        if not appdata_dir:
            raise ValueError("Appdata directory is not set!")
        if not output_dir:
            raise ValueError("Output directory is not set!")

        selection = []
        now_formatted = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with open(log_file_path, 'w') as log_file:
            log_file.write('+-----------------------------------------------------------------------------------------+\n')
            log_file.write('|----------------------------------- WALLET SLEUTH LOG -----------------------------------|\n')
            log_file.write('+-----------------------------------------------------------------------------------------+\n')
            log_file.write('Start Time: ' + str(now_formatted) + '\n')

        #dicationary map to wallet fucntions
        wallet_functions = {
            ('Atomic Wallet', None): atomic_wallet,
            ('Bitget^', 'Brave'): bitkeep_brave,
            ('Bitget^', 'Chrome'): bitkeep_chrome,
            ('Brave Browser Wallet', None): brave_wallet,
            ('Brave Browser Legacy', None): brave_legacy,
            ('Guarda^', 'Chrome'): guarda_chrome,
            ('Guarda^', 'Opera'): guarda_opera,
            ('MetaMask^', 'Brave'): metamask_brave,
            ('MetaMask^', 'Chrome'): metamask_chrome,
            ('MetaMask^', 'Edge'): metamask_edge,
            ('Opera Browser Wallet', None): opera_wallet,
            ('Ledger Live', None): ledger_live_wallet,
            ('Phantom^', 'Brave'): phantom_brave,
            ('Phantom^', 'Chrome'): phantom_chrome,
            ('Exodus Wallet', None): exodus_wallet,
            ('Wasabi Wallet', None): wasabi_wallet,
            ('Litecoin Core', None): litecoin_core_wallet,
            ('Bitcoin Core', None): bitcoin_core_wallet,
            ('Coinbase Wallet^', 'Chrome'): coinbase_wallet_chrome,
            ('Coinbase Wallet^', 'Brave'): coinbase_wallet_brave,
            ('Crypto.com Wallet^', 'Chrome'): cryptocom_wallet_chrome
        }

        #process slected wallets
        for selection_key in Wallet_Selector.selection:
            if selection_key in wallet_functions:
                wallet_name, browser_type = selection_key
                function = wallet_functions[selection_key]
                process_wallet(wallet_name, browser_type, function, output_dir, log_file_path, selection)

        #output creation
        with open(f"{output_dir}/output.csv", 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Type', 'Currency', 'Address', 'Wallet', 'Path'])
            for file in selection:
                with open(file, 'r', newline='') as f1:
                    reader = csv.reader(f1)
                    writer.writerows(reader)

        #completion notifications
        if Wallet_Selector.selection:
            messagebox.showinfo('Wallet Sleuth', 'Search Complete!')
        else:
            messagebox.showerror('Wallet Sleuth', 'No Wallets Selected!')

    #all other errors
    except Exception as e:
        messagebox.showerror('Error', f'An unexpected error occurred: "{str(e)}"\n\nPlease report this to the developer!')
