#generic imports
import winreg

#tkinter imports
import tkinter as tk
from tkinter import messagebox

wallet_vid_pid = {
    #these devices are listed within the Interpol Hardware Wallet repo, but are omited from the dictionary due to limited other information besides the VID & PID.
    #('VID_1029', 'PID_B0B0'): '??? - Monero Hardware Wallet',
    #('VID_1029', 'PID_C0DA'): '??? - Monero Hardware Wallet',
    #('VID_1029', 'PID_D00D'): '??? - Monero Hardware Wallet',
    ##########################################################
    ('VID_03EB', 'PID_2402'): 'ShiftCrypto - BitBox01 (DigitalBitBox)',
    ('VID_03EB', 'PID_2403'): 'Shift Crypto - BitBox02',
    ('VID_096E', 'PID_0891'): 'Feitian Tech - JuBiter Blade',
    ('VID_1209', 'PID_AAAA'): 'Prokey - Optimum',
    ('VID_1209', 'PID_ABBA'): 'SafeWISE - CoinSafe',
    ('VID_1209', 'PID_53C0'): 'SatoshiLabs - Trezor Model 2 (Model T)',
    ('VID_1209', 'PID_53C1'): 'SatoshiLabs - Trezor Model 2 (Model T)',
    ('VID_534C', 'PID_0001'): 'SatoshiLabs - Trezor Model 1',
    ('VID_1209', 'PID_7000'): 'Secalot - Hardware Dongle',
    ('VID_1209', 'PID_7001'): 'Secalot - Hardware Dongle',
    ('VID_1209', 'PID_7551'): 'Coinkite - OpenDime',
    ('VID_D13E', 'PID_CC10'): 'CoinKite - Coldcard',
    ('VID_1209', 'PID_9998'): 'Opolo - Cosmos',
    ('VID_1209', 'PID_9999'): 'Opolo - Cosmos',
    ('VID_2341', 'PID_003D'): 'BitLox - Ultimate',
    ('VID_2341', 'PID_003E'): 'BitLox - Ultimate',
    ('VID_2581', 'PID_1807'): 'Ledger - HW1',
    ('VID_2581', 'PID_1808'): 'Ledger - HW1',
    ('VID_2581', 'PID_1B7C'): 'Ledger - HW1',
    ('VID_2581', 'PID_F1D1'): 'Ledger - HW1 or Nano S Plus',
    ('VID_2C97', None): 'Ledger - HW2, X, Blue or Nano S',
    ('VID_2B24', None): 'ShapeShift - KeepKey',
    ('VID_2F48', 'PID_2130'): "D'CENT - Biometric Wallet",
}


def fetch_connected_devices():
    connected_devices = []
    try:
        access_registry = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        access_key = winreg.OpenKey(access_registry, r'SYSTEM\ControlSet001\Enum\USB')

        index = 0
        while True:
            try:
                device = winreg.EnumKey(access_key, index)
                connected_devices.append(device)
                index += 1
            except:
                break

    except Exception as e:
        messagebox.showerror("Error", f"Unable to read from registry: {str(e)}")
    return connected_devices


def identify_wallet_devices(connected_devices):
    wallet_devices = []
    for device in connected_devices:
        for (vid, pid), wallet_name in wallet_vid_pid.items():
            if vid in device and (pid is None or pid in device):
                wallet_devices.append(wallet_name)
                break
    return wallet_devices


def hardware_wallet_scan():
    connected_devices = fetch_connected_devices()
    wallet_devices = identify_wallet_devices(connected_devices)

    if not wallet_devices:
        messagebox.showinfo('Connected Hardware Wallet Detector', "No hardware wallets detected.")
    else:
        items_text = "\n".join(wallet_devices)
        messagebox.showinfo('Connected Hardware Wallet Detector', "Detected hardware wallets:\n" + items_text)


'''
This list was taken from the Interpol Innovation Centre Hardware Wallet repo:

https://github.com/INTERPOL-Innovation-Centre/HardwareWallets_DF_List

CONFIRM YOUR OWN FINDINGS!
'''