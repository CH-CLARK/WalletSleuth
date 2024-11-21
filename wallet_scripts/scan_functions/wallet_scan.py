#generic imports
import os

#controller imports
import controller.config

#tkitner imports
import tkinter as tk
from tkinter import messagebox, filedialog


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
    r'Local\BraveSoftware\Brave-Browser\User Data\Default\Local Extension Settings\hnfanknocfeofbddgcijnmhnfnkdnaad' : 'Coinbase Wallet (Brave)',

    r'Local\Google\Chrome\User Data\Default\Local Extension Settings\hifafgmccdpekplomjjkcfgodnhcellj' : 'Crypto.com Wallet (Chrome)',

    r'Roaming\@trezor\suite-desktop\IndexedDB': 'Trezor Suite',
}

profile_directories = [f'Profile {i}' for i in range(1, 101)] + ['Default'] #if a user has more than 100 browser profiles i want to see it.

def wallet_scan():
    try:
        appdata_dir = controller.config.APPDATA
        directory_results = {}
        
        for relative_path, name in paths.items():
            profiles_found = []
            is_browser_extension = 'Default\\Local Extension Settings' in relative_path
            
            default_path = os.path.join(appdata_dir, relative_path)
            if os.path.exists(default_path) and os.path.isdir(default_path):
                profiles_found.append('Default')
            
            if is_browser_extension:
                for profile in profile_directories:
                    if profile != 'Default':
                        directory_path = os.path.join(appdata_dir, relative_path.replace('Default', profile))
                        if os.path.exists(directory_path) and os.path.isdir(directory_path):
                            profiles_found.append(profile)

            if profiles_found:
                if is_browser_extension:
                    if 'Default' in profiles_found and len(profiles_found) == 1:
                        result = 'Default User Identified'
                    elif len(profiles_found) > 1 and 'Default' in profiles_found:
                        result = 'Default and Profile Users Identified'
                    else:
                        result = 'Profile Users Identified'

                else:
                    result = 'Identified'
                
                directory_results[name] = result

        identified_wallets = "\n".join(f'{key} - {value}' for key, value in directory_results.items())
        
        if identified_wallets:
            response = messagebox.askquestion('Wallet Detector', 'Identified Wallets:\n' + identified_wallets + '\n\nDo you wish to save these results?\n', icon='info')

            if response == 'yes':
                file_path = save_output()
                if file_path:
                    with open(file_path, 'a') as file:
                        file.write(identified_wallets)
        else:
            messagebox.showinfo('Wallet Detector', 'No wallets identified.')

    except Exception as e:
        messagebox.showerror('Error', "You must select an 'Appdata' directory first!")


def save_output():
    file_path = filedialog.asksaveasfilename(defaultextension='.txt', initialfile='WS_Scan_Results.txt')

    if file_path:
        with open(file_path, 'w') as file:
            file.write('+-----------------------------------------------------------------------------------------+\n')
            file.write('|----------------------------------- IDENTIFIED WALLETS ----------------------------------|\n')
            file.write('+-----------------------------------------------------------------------------------------+\n')

        return file_path
    else:
        pass
