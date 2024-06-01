#generic
import os

#controller imports
import controller.config

#tkinter imports
import tkinter as tk
from tkinter import messagebox, filedialog

#paths to check - Limitation currently is that it only checks the default (NOT PROFILEs) for each wallet
paths = {
    r'Roaming\atomic' : 'Atomic Wallet',
    
    r'Local\Google\Chrome\User Data\Default\Local Extension Settings\jiidiaalihmmhddjgbnbgdfflelocpak' : 'Bitget (Chrome)',
    r'Local\BraveSoftware\Brave-Browser\User Data\Default\Local Extension Settings\jiidiaalihmmhddjgbnbgdfflelocpak' : 'Bitget (Brave)',

    r'Local\BraveSoftware\Brave-Browser\User Data\Default\Local Extension Settings\odbfpeeihdkbihmopkbjmoonfanlbfcl' : 'Brave Browser Legacy',
    r'Local\BraveSoftware\Brave-Browser\User Data\Default\Preferences' : 'Brave Browser Wallet',

    r'Local\Google\Chrome\User Data\Default\Local Extension Settings\hpglfhgfnhbgpjdenjgmdgoeiappafln' : 'Guarda (Chrome)',
    r'Roaming\Opera Software\Opera Stable\Default\Local Extension Settings\acdamagkdfmpkclpoglgnbddngblgibo': 'Guarda (Opera)',

    r'Roaming\Ledger Live': 'Ledger Live',

    r'Local\Google\Chrome\User Data\Default\Local Extension Settings\nkbihfbeogaeaoehlefnkodbefgpgknn' : 'MetaMask (Chrome)',
    r'Local\Microsoft\Edge\User Data\Default\Local Extension Settings\ejbalbakoplchlghecdalmeeeajnimhm' : 'MetaMask (Edge)',
    r'Local\BraveSoftware\Brave-Browser\User Data\Default\Local Extension Settings\nkbihfbeogaeaoehlefnkodbefgpgknn' : 'MetaMask (Brave)',

    r'Roaming\Opera Software\Opera Stable\Local Extension Settings\gojhcdgcpbpfigcaejpfhfegekdgiblk' : 'Opera Browser Wallet',

    r'Local\Google\Chrome\User Data\Default\Local Extension Settings\bfnaelmomeimhlpmgjnjophhpkkoljpa' : 'Phantom (Chrome)',
    r'Local\BraveSoftware\Brave-Browser\User Data\Default\Local Extension Settings\bfnaelmomeimhlpmgjnjophhpkkoljpa' : 'Phantom (Brave)',

    r'Roaming\Exodus\Partitions\main\Cache\Cache_Data': 'Exodus Wallet',

    r'Roaming\WalletWasabi\Client\Wallets':'Wallet Wasabi',

    r'Roaming\Litecoin\wallets': 'Litecoin Core',

    r'Roaming\Bitcoin\wallets': 'Bitcoin Core',

    r'Local\Google\Chrome\User Data\Default\Local Extension Settings\hnfanknocfeofbddgcijnmhnfnkdnaad' : 'Coinbase Wallet (Chrome)',
}


def wallet_scan():
    try:

        appdata_dir = controller.config.APPDATA

        directory_paths = {name: os.path.join(appdata_dir, path) for path, name in paths.items()}

        directory_results = {}

        for name, directory_path in directory_paths.items():
            if os.path.exists(directory_path) and os.path.isdir(directory_path):
                directory_results[name] = 'exists'
            else:
                pass
            
        identified_wallets = "\n".join(directory_results)

        response = messagebox.askquestion('Wallet Detector', 'Identified Wallets:\n' + identified_wallets + '\n\nDo you wish to save these results?\n', icon = 'info')

        if response == 'yes':
            file_path = save_output()
            if file_path:
                with open(file_path, 'a') as file:
                    file.write(identified_wallets)

            if response == 'no':
                pass

    except Exception:
        messagebox.showerror('Error', "You must select an 'Appdata' directory first!")


def save_output():
    file_path  = filedialog.asksaveasfilename(defaultextension='.txt', initialfile='WS_Scan_Results.txt')

    if file_path:
        with open(file_path, 'w') as file:
            file.write('+-----------------------------------------------------------------------------------------+\n')
            file.write('|----------------------------------- IDENTIFIED WALLETS ----------------------------------|\n')
            file.write('+-----------------------------------------------------------------------------------------+\n')


        return file_path
    else:
        pass