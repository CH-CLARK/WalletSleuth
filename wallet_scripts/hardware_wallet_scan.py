'''
See the Interpol Innovation Centre Hardware Wallet list below:

https://github.com/INTERPOL-Innovation-Centre/HardwareWallets_DF_List

This list was taken from that repo and should be slowly updated along with it.
CONFIRM YOUR OWN FINDINGS!
'''

#generic imports
import winreg

#tkinter imports
import tkinter as tk
from tkinter import messagebox


def hardware_wallet_scan():
    access_registry = winreg.ConnectRegistry(None,winreg.HKEY_LOCAL_MACHINE)
    access_key = winreg.OpenKey(access_registry,r'SYSTEM\ControlSet001\Enum\USB')
    
    connected_devices = []
    wallet_devices = []

    for n in range(1000):
        try:
            x = winreg.EnumKey(access_key,n)
            connected_devices.append(x)
            
        except:
            break

    #BitBox
    if any('VID_03EB&PID_2402' in s for s in connected_devices):
        wallet_devices.append('ShiftCrypto - BitBox01 (DigitalBitBox)')

    if any('VID_03EB&PID_2403' in s for s in connected_devices):
        wallet_devices.append('Shift Crypto - BitBox02')

    #JuBiter Blade
    if any('VID_096E&PID_0891' in s for s in connected_devices):
        wallet_devices.append('Feitian Tech - JuBiter Blade')

    #Optimum
    if any('VID_1209&PID_AAAA' in s for s in connected_devices):
        wallet_devices.append('Prokey - Optimum')

    #SafeWISE CoinSafe
    if any('VID_1209&PID_ABBA' in s for s in connected_devices):
        wallet_devices.append('SafeWISE - CoinSafe')

    #Trezor
    if 'VID_1209&PID_53C0' in connected_devices or 'VID_1209&PID_53C1' in connected_devices:
        wallet_devices.append('SatoshiLabs - Trezor Model 2 (Model T)')

    if any('VID_534C&PID_0001' in s for s in connected_devices):
        wallet_devices.append('SatoshiLabs - Trezor Model 1')


    '''
    ## This device is listed by the Interpol Hardware Wallets list, but the repo only details the VID&PID. I have struggled to find images or any other information, so decided to omit it for now.
    ## https://github.com/INTERPOL-Innovation-Centre/HardwareWallets_DF_List
      
    if 'VID_1209&PID_B0B0' in connected_devices or 'VID_1209&PID_C0DA' in connected_devices or 'VID1209&PID_D00D' in connected_devices:
        print(' - Monero Hardware Wallet')
        wallet_devices.append('Monero')
    
    '''

    #Secalot
    if 'VID_1209&PID_7000' in connected_devices or 'VID_1209&PID_7001' in connected_devices:
        wallet_devices.append('Secalot - Hardware Dongle')

    #OpenDime
    if any('VID_1209&PID_7551' in s for s in connected_devices):
        wallet_devices.append('Coinkite - OpenDime')

    #CoinKite
    if any('VID_D13E&PID_CC10' in s for s in connected_devices):
        wallet_devices.append('CoinKite - Coldcard')

    #Opolo
    if 'VID_1209&PID_9998' in connected_devices or 'VID_1209&PID_9999' in connected_devices:
        wallet_devices.append('Opolo - Cosmos')
    
    #BitLox
    if 'VID_2341&PID_003D' in connected_devices or 'VID_2341&PID_003E' in connected_devices:
        wallet_devices.append('BitLox - Ultimate')

    #Ledger
    if 'VID_2581&PID_1807' in connected_devices or 'VID_2581&PID_1808' in connected_devices or 'VID_2581&PID_1B7C' in connected_devices or 'VID_258&PID_1B7C' in connected_devices or 'VID_2581&PID_2B7C' in connected_devices or 'VID_2581&PID_3B7C' in connected_devices or 'VID_2581&PID_4B7C' in connected_devices:
        wallet_devices.append('Ledger - HW1')

    if any('VID_2581&PID_F1D1' in s for s in connected_devices):
        wallet_devices.append('Ledger - HW or Nano S Plus')
    
    if any('VID_2C97' in s for s in connected_devices):
        wallet_devices.append('Ledger - HW2, X, Blue or Nano S')

    #KeepKey
    if any('VID_2B24' in s for s in connected_devices):
        wallet_devices.append('ShapeShift - KeepKey')
    
    #D'CENT
    if any('VID_2F48&PID_2130' in s for s in connected_devices):
        wallet_devices.append("D'CENT - Biometric Wallet")
    
    if not wallet_devices:
        messagebox.showinfo('Connect Hardware Wallet Detector', "No previously connected hardware wallet devices identified!")

    if wallet_devices:
        items_text = "\n".join(wallet_devices)
        messagebox.showinfo('Connect Hardware Wallet Detector', "Previously connected hardware wallet devices:\n" + items_text)