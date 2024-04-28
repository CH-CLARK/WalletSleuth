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
from wallet_scripts.guarda_ext import guarda_chrome
from wallet_scripts.opera_browser_wallet import opera_wallet
from wallet_scripts.ledger_live import ledger_live_wallet
from wallet_scripts.phantom_ext import phantom_chrome, phantom_brave
from wallet_scripts.exodus_wallet import exodus_wallet
from wallet_scripts.wasabi_wallet import wasabi_wallet
from wallet_scripts.litecoin_core_wallet import litecoin_core_wallet
from wallet_scripts.bitcoin_core_wallet import bitcoin_core_wallet


def run_func():
    try:
        appdata_dir = controller.config.APPDATA
        output_dir = controller.config.OUTPUT

        selection = []

        get_now_datetime = datetime.datetime.now()
        now_formated = get_now_datetime.strftime('%Y-%m-%d %H:%M:%S')

        with open(output_dir + '/' + 'WalletSleuth_log.txt', 'w') as log_file:
            log_file.write('+-----------------------------------------------------------------------------------------+\n')
            log_file.write('|----------------------------------- WALLET SLEUTH LOG -----------------------------------|\n')
            log_file.write('+-----------------------------------------------------------------------------------------+\n')
            log_file.write('Start Time: ' + str(now_formated) + '\n')

        #Atomic Wallet 
        if ('Atomic Wallet', None) in Wallet_Selector.selection:
            try:
                atomic_wallet()
                selection.append(output_dir + '/' + 'atomic_wallet_addresses.csv')
            except:
                with open(output_dir + '/' + 'WalletSleuth_log.txt', 'a') as log_file:
                    log_file.write("ERROR: Atomic wallet - Wallet not found!\n")

        #Bitkeep Extension
        if ('Bitget*', 'Brave') in Wallet_Selector.selection:
            try:
                bitkeep_brave()
                selection.append(output_dir + '/' + 'bitkeep_brave_addresses.csv')
            except:
                with open(output_dir + '/' + 'WalletSleuth_log.txt', 'a') as log_file:
                    log_file.write('ERROR: Bitget (Brave) - Wallet Not Found!\n')

        if ('Bitget*', 'Chrome') in Wallet_Selector.selection:
            try:
                bitkeep_chrome()
                selection.append(output_dir + '/' + 'bitkeep_chrome_addresses.csv')
            except:
                with open(output_dir + '/' + 'WalletSleuth_log.txt', 'a') as log_file:
                    log_file.write('ERROR: Bitget (Chrome) - Wallet Not Found!\n')

        #Brave Browser Wallet
        if ('Brave Browser Wallet', None) in Wallet_Selector.selection:
            try:
                brave_wallet()
                selection.append(output_dir + '/' + 'brave_browser_addresses.csv')
            except:
                with open(output_dir + '/' + 'WalletSleuth_log.txt', 'a') as log_file:
                    log_file.write('ERROR: Brave Browser Wallet - Wallet Not Found!\n')

        #Brave Browser Legacy Wallet - SPELLING ERROR
        if ('Brave Browser Legacy', None) in Wallet_Selector.selection:
            try:
                brave_legacy()
                selection.append(output_dir + '/' + 'brave_legacy_addresses.csv')
            except:
                with open(output_dir + '/' + 'WalletSleuth_log.txt', 'a') as log_file:
                    log_file.write('ERROR: Brave Browser Legacy Wallet - Wallet Not Found!\n')

        #Guarda Extension
        if ('Guarda*', 'Chrome') in Wallet_Selector.selection:
            try:
                guarda_chrome()
                selection.append(output_dir + '/' + 'guarda_chrome_addresses.csv')
            except:
                with open(output_dir + '/' + 'WalletSleuth_log.txt', 'a') as log_file:
                    log_file.write('ERROR: Guarda (Chrome) - Wallet Not Found!\n')

        #MetaMask Extension
        if ('MetaMask*', 'Brave') in Wallet_Selector.selection:
            try:
                metamask_brave()
                selection.append(output_dir + '/' + 'metamask_brave_addresses.csv')
            except:
                with open(output_dir + '/' + 'WalletSleuth_log.txt', 'a') as log_file:
                    log_file.write('ERROR: Metamask (Brave) - Wallet Not Found!\n')

        if ('MetaMask*', 'Chrome') in Wallet_Selector.selection:
            try:
                metamask_chrome()
                selection.append(output_dir + '/' + 'metamask_chrome_addresses.csv')
            except:
                with open(output_dir + '/' + 'WalletSleuth_log.txt', 'a') as log_file:
                    log_file.write('ERROR: Metamask (Chrome) - Wallet Not Found!\n')

        if ('MetaMask*', 'Edge') in Wallet_Selector.selection:
            try:
                metamask_edge()
                selection.append(output_dir + '/' + 'metamask_edge_addresses.csv')
            except:
                with open(output_dir + '/' + 'WalletSleuth_log.txt', 'a') as log_file:
                    log_file.write('ERROR: Metamask (Edge) - Wallet Not Found!\n')

        #Opera Browser Wallet
        if ('Opera Browser Wallet', None) in Wallet_Selector.selection:
            try:
                opera_wallet()
                selection.append(output_dir + '/' + 'opera_browser_addresses.csv')
            except:
                with open(output_dir + '/' + 'WalletSleuth_log.txt', 'a') as log_file:
                    log_file.write('ERROR: Opera Browser Wallet - Wallet Not Found!\n')

        #Ledger Live
        if ('Ledger Live', None) in Wallet_Selector.selection:
            try:
                ledger_live_wallet()
                selection.append(output_dir + '/' + 'ledger_live_addresses.csv')
            except:
                with open(output_dir + '/' + 'WalletSleuth_log.txt', 'a') as log_file:
                    log_file.write('ERROR: Ledger Live Wallet - Wallet Not Found!\n')

        #Phantom Extension - WIP
        if ('Phantom*', 'Brave') in Wallet_Selector.selection:
            try:
                phantom_brave()
                selection.append(output_dir + '/' + 'phantom_brave_addresses.csv')
            except:
                with open(output_dir + '/' + 'WalletSleuth_log.txt', 'a') as log_file:
                    log_file.write('ERROR: Phantom (Brave) - Wallet Not Found!\n')

        if ('Phantom*', 'Chrome') in Wallet_Selector.selection:
            try:
                phantom_chrome()
                selection.append(output_dir + '/' + 'phantom_chrome_addresses.csv')
            except:
                with open(output_dir + '/' + 'WalletSleuth_log.txt', 'a') as log_file:
                    log_file.write('ERROR: Phantom (Chrome) - Wallet Not Found!\n')

        #Exodus Wallet 
        if ('Exodus Wallet', None) in Wallet_Selector.selection:
            try:
                exodus_wallet()
                selection.append(output_dir + '/' + 'exodus_wallet_transactions.csv')
            except:
                with open(output_dir + '/' + 'WalletSleuth_log.txt', 'a') as log_file:
                    log_file.write("ERROR: Exodus Wallet - Wallet not found!\n")

       #Wasabi Wallet 
        if ('Wasabi Wallet', None) in Wallet_Selector.selection:
            try:
                wasabi_wallet()
                selection.append(output_dir + '/' + 'wasabi_wallet_addresses.csv')
            except:
                with open(output_dir + '/' + 'WalletSleuth_log.txt', 'a') as log_file:
                    log_file.write("ERROR: Wasabi Wallet - Wallet not found!\n")

       #Litecoin Core Wallet 
        if ('Litecoin Core', None) in Wallet_Selector.selection:
            try:
                litecoin_core_wallet()
                selection.append(output_dir + '/' + 'litecoin_core_addresses.csv')
            except:
                with open(output_dir + '/' + 'WalletSleuth_log.txt', 'a') as log_file:
                    log_file.write("ERROR: Litecoin Core Wallet - Wallet not found!\n")

        if ('Bitcoin Core', None) in Wallet_Selector.selection:
            try:
                bitcoin_core_wallet()
                selection.append(output_dir + '/' + 'bitcoin_core_addresses.csv')
            except:
                with open(output_dir + '/' + 'WalletSleuth_log.txt', 'a') as log_file:
                    log_file.write("ERROR: bitcoin Core Wallet - Wallet not found!\n")

        
    #---------------------------------#
    #---------------------------------#
        #create output file
        with open(output_dir + '/' + 'output.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Type', 'Currency', 'Address', 'Wallet', 'Path'])
            for file in selection:
                with open(file, 'r', newline='') as f1:
                    reader = csv.reader(f1)
                    new_data = [row for row in reader]
                    writer.writerows(new_data)
        
        #completion notification
        messagebox.showinfo('Wallet Sleuth', 'Search Complete!')
    
    except Exception:
        messagebox.showerror('Error', "You must select an 'Appdata' & 'Output' directory first!")
