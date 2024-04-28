#generic
import os

#controller imports
import controller.config

#tkinter imports
import tkinter as tk
from tkinter import messagebox

#paths to check - Limitation currently is that it only checks the default (NOT PROFILEs) for each wallet
paths = {
    r'Roaming\atomic' : 'Atomic Wallet',
    
    r'Local\Google\Chrome\User Data\Default\Local Extension Settings\jiidiaalihmmhddjgbnbgdfflelocpak' : 'Bitget (Chrome)',
    r'Local\BraveSoftware\Brave-Browser\User Data\Default\Local Extension Settings\jiidiaalihmmhddjgbnbgdfflelocpak' : 'Bitget (Brave)',

    r'Local\BraveSoftware\Brave-Browser\User Data\Default\Local Extension Settings\odbfpeeihdkbihmopkbjmoonfanlbfcl' : 'Brave Browser Legacy',
    r'Local\BraveSoftware\Brave-Browser\User Data\Default\Preferences' : 'Brave Browser Wallet',

    r'Local\Google\Chrome\User Data\Default\Local Extension Settings\hpglfhgfnhbgpjdenjgmdgoeiappafln' : 'Guarda (Chrome)',

    r'Roaming\Ledger Live' : 'Ledger Live',

    r'Local\Google\Chrome\User Data\Default\Local Extension Settings\nkbihfbeogaeaoehlefnkodbefgpgknn' : 'MetaMask (Chrome)',
    r'Local\Microsoft\Edge\User Data\Default\Local Extension Settings\ejbalbakoplchlghecdalmeeeajnimhm' : 'MetaMask (Edge)',
    r'Local\BraveSoftware\Brave-Browser\User Data\Default\Local Extension Settings\nkbihfbeogaeaoehlefnkodbefgpgknn' : 'MetaMask (Brave)',

    r'Roaming\Opera Software\Opera Stable\Local Extension Settings\gojhcdgcpbpfigcaejpfhfegekdgiblk' : 'Opera Browser Wallet',

    r'Local\Google\Chrome\User Data\Default\Local Extension Settings\bfnaelmomeimhlpmgjnjophhpkkoljpa' : 'Phantom (Chrome)',
    r'Local\BraveSoftware\Brave-Browser\User Data\Default\Local Extension Settings\bfnaelmomeimhlpmgjnjophhpkkoljpa' : 'Phantom (Brave)',

    r'Roaming\Exodus\Partitions\main\Cache\Cache_Data': 'Exodus Wallet',

    r'Roaming\WalletWasabi\Client\Wallets':'Wallet Wasabi',

    r'Roaming\Litecoin\wallets': 'Litecoin Core',

    r'Roaming\Bitcoin\wallets': 'Bitcoin Core'
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

        messagebox.showinfo('Wallet Detector', 'Identified Wallets:\n' + identified_wallets)

    except Exception:
        messagebox.showerror('Error', "You must select an 'Appdata' directory first!")