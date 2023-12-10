#generic imports
import csv

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


def run_func():
    appdata_dir = controller.config.APPDATA
    output_dir = controller.config.OUTPUT

    selection = []

    with open(output_dir + '/' + 'WalletSleuth_log.txt', 'w') as log_file:
        log_file.write('+-----------------------------------------------------------------------------------------+\n')
        log_file.write('|----------------------------------- WALLET SLEUTH LOG -----------------------------------|\n')
        log_file.write('+-----------------------------------------------------------------------------------------+\n')

    print('Run Button Pressed')

    #Atomic Wallet 
    if ('Atomic Wallet', None) in Wallet_Selector.selection:
        try:
            atomic_wallet()
            selection.append(output_dir + '/' + 'atomic_wallet_addresses.csv')
        except:
            with open(output_dir + '/' + 'WalletSleuth_log.txt', 'a') as log_file:
                log_file.write("ERROR: (ATOMIC WALLET) - Wallet not found!\n")

    #Bitkeep Extension
    if ('Bitkeep*', 'Brave') in Wallet_Selector.selection:
        try:
            bitkeep_brave()
            selection.append(output_dir + '/' + 'bitkeep_brave_addresses.csv')
        except Exception:
            print('Bitkeep Brave - Wallet Not Found')

    if ('Bitkeep*', 'Chrome') in Wallet_Selector.selection:
        try:
            bitkeep_chrome()
            selection.append(output_dir + '/' + 'bitkeep_chrome_addresses.csv')
        except Exception:
            print('Bitkeep Chrome - Wallet Not Found')

    #Brave Browser Wallet
    if ('Brave Browser Wallet', None) in Wallet_Selector.selection:
        try:
            brave_wallet()
            selection.append(output_dir + '/' + 'brave_browser_addresses.csv')
        except Exception:
            print('Brave Browser Wallet - Wallet Not Found')

    #Brave Browser Legacy Wallet - SPELLING ERROR
    if ('Brave Browser Legacy', None) in Wallet_Selector.selection:
        try:
            brave_legacy()
            selection.append(output_dir + '/' + 'brave_legacy_addresses.csv')
        except Exception:
            print('Brave Browser Legacy Wallet - Wallet Not Found')

    #Guarda Extension
    if ('Guarda*', 'Chrome') in Wallet_Selector.selection:
        try:
            guarda_chrome()
            selection.append(output_dir + '/' + 'guarda_chrome_addresses.csv')
        except Exception:
            print('Guarda Chrome - Wallet Not Found')

    #MetaMask Extension
    if ('MetaMask*', 'Brave') in Wallet_Selector.selection:
        try:
            metamask_brave()
            selection.append(output_dir + '/' + 'metamask_brave_addresses.csv')
        except:
            print('Metamask Brave - Wallet Not Found')

    if ('MetaMask*', 'Chrome') in Wallet_Selector.selection:
        try:
            metamask_chrome()
            selection.append(output_dir + '/' + 'metamask_chrome_addresses.csv')
        except:
            print('MetaMask Chrome - Wallet Not Found')

    if ('MetaMask*', 'Edge') in Wallet_Selector.selection:
        try:
            metamask_edge()
            selection.append(output_dir + '/' + 'metamask_edge_addresses.csv')
        except:
            print('Metamask Edge - Wallet Not Found')

    #Opera Browser Wallet
    if ('Opera Browser Wallet', None) in Wallet_Selector.selection:
        try:
            opera_wallet()
            selection.append(output_dir + '/' + 'opera_browser_addresses.csv')
        except Exception:
            print('Opera Browser Wallet - Wallet Not Found')

    #Ledger Live
    if ('Ledger Live', None) in Wallet_Selector.selection:
        try:
            ledger_live_wallet()
            selection.append(output_dir + '/' + 'ledger_live_addresses.csv' )
        except Exception:
            print('Ledger Live Wallet - Wallet Not Found')

    #Phantom Extension - WIP
    if ('Phantom*', 'Brave') in Wallet_Selector.selection:
        print('Phantom Brave function ran')

    if ('Phantom*', 'Chrome') in Wallet_Selector.selection:
        print('Phantom Chrome function ran')

#---------------------------------#
#---------------------------------#
    #create output file
    with open(output_dir + '/' + 'output.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Currency', 'Address', 'Wallet', 'Path'])
        for file in selection:
            with open(file, 'r', newline='') as f1:
                reader = csv.reader(f1)
                new_data = [row for row in reader]
                writer.writerows(new_data)
    
    #completion notification
    messagebox.showinfo('Wallet Sleuth', 'Search Complete!')
