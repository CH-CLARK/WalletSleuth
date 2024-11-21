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
from wallet_scripts.desktop_wallets.atomic_wallet import atomic_wallet
from wallet_scripts.desktop_wallets.bitcoin_core_wallet import bitcoin_core_wallet
from wallet_scripts.desktop_wallets.ledger_live_wallet import ledger_live_wallet
from wallet_scripts.desktop_wallets.litecoin_core_wallet import litecoin_core_wallet
from wallet_scripts.desktop_wallets.wasabi_wallet import wasabi_wallet
from wallet_scripts.desktop_wallets.exodus_wallet import exodus_wallet
from wallet_scripts.desktop_wallets.trezor_suite_wallet import trezor_suite_wallet

# from wallet_scripts.browser_wallets.bitget_ext import bitget_chrome
from wallet_scripts.browser_wallets.metamask_ext import metamask_brave, metamask_chrome, metamask_edge
from wallet_scripts.browser_wallets.guarda_ext import guarda_chrome, guarda_opera
from wallet_scripts.browser_wallets.phantom_ext import phantom_brave, phantom_chrome
from wallet_scripts.browser_wallets.coinbase_ext import coinbase_brave, coinbase_chrome
from wallet_scripts.browser_wallets.cryptocom_ext import cryptocom_brave, cryptocom_chrome
from wallet_scripts.browser_wallets.brave_browser_wallet import browser_brave
from wallet_scripts.browser_wallets.opera_browser_wallet import browser_opera

def process_wallet(wallet_name, browser_type, function, output_dir, log_file_path, selection):
    try:
        function()
        wallet_name = wallet_name.lower().replace(' ', '_')

        if browser_type:
            browser_type = browser_type.lower()
            csv_file = f"{output_dir}/{wallet_name}_{browser_type}_output.csv"

        else:
            csv_file = f"{output_dir}/{wallet_name}_output.csv"
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
            log_file.write(f'Start Time: {str(now_formatted)}\n')

        #dicationary map to wallet fucntions
        wallet_functions = {
            ('Atomic Wallet', None): atomic_wallet,
            #bitkeep here
            ('Bitcoin Core', None): bitcoin_core_wallet,
            ('Brave Browser Wallet', None): browser_brave,
            ('Coinbase^', 'Brave'): coinbase_brave,
            ('Coinbase^', 'Chrome'): coinbase_chrome,
            ('Crypto.com^', 'Brave'): cryptocom_brave,
            ('Crypto.com^', 'Chrome'): cryptocom_chrome,
            ('Exodus Wallet', None): exodus_wallet,
            ('Guarda^', 'Chrome'): guarda_chrome,
            ('Guarda^', 'Opera'): guarda_opera,
            ('Ledger Live', None): ledger_live_wallet,
            ('Litecoin Core', None): litecoin_core_wallet,
            ('MetaMask^', 'Brave'): metamask_brave,
            ('MetaMask^', 'Chrome'): metamask_chrome,
            ('MetaMask^', 'Edge'): metamask_edge,
            ('Opera Browser Wallet', None): browser_opera,
            ('Phantom^', 'Brave'): phantom_brave,
            ('Phantom^', 'Chrome'): phantom_chrome,
            ('Trezor Suite', None): trezor_suite_wallet,
            ('Wasabi Wallet', None): wasabi_wallet,
        }

        for selection_key in Wallet_Selector.selection:
            if selection_key in wallet_functions:
                wallet_name, browser_type = selection_key
                function = wallet_functions[selection_key]
                process_wallet(wallet_name, browser_type, function, output_dir, log_file_path, selection)

        with open(f"{output_dir}/output.csv", 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Type', 'Currency', 'Address', 'Wallet', 'Path'])
            try:
                for file in selection:
                    with open(file, 'r', newline='') as f1:
                        reader = csv.reader(f1)
                        writer.writerows(reader)
            except:
                pass

        if Wallet_Selector.selection:
            messagebox.showinfo('Wallet Sleuth', 'Search Complete!')
        else:
            messagebox.showerror('Wallet Sleuth', 'No Wallets Selected!')

    except Exception as e:
        messagebox.showerror('Error', f'An unexpected error occurred: "{str(e)}"\n\nPlease report this to the developer!')