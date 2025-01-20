from tkinter import messagebox

try:
    import brotli

    names = {
        'Atomic Wallet': None,
        'Bitcoin Core': None,
        'Bitget^': {'Brave', 'Chrome'},
        'Brave Browser Wallet': None,
        'Coinbase^': {'Brave', 'Chrome'},
        'Crypto.com^':{'Brave', 'Chrome'},
        'Dogecoin Core': None,
        'Exodus Wallet': None,
        'Guarda^': {'Chrome', 'Opera'},
        'Ledger Live': None, 
        'Litecoin Core': None,
        'MetaMask^': {'Brave', 'Chrome', 'Edge'},
        'Opera Browser Wallet': None,
        'Phantom^': {'Brave'},
        'Wasabi Wallet': None,
        'Trezor Suite': None
        }

except:
    pass
    names = {
        'Atomic Wallet': None,
        'Bitcoin Core': None,
        'Bitget^': {'Brave', 'Chrome'},
        'Brave Browser Wallet': None,
        'Coinbase^': {'Brave', 'Chrome'},
        'Crypto.com^':{'Brave', 'Chrome'},
        'Dogecoin Core': None,
        'Guarda^': {'Chrome', 'Opera'},
        'Ledger Live': None,
        'Litecoin Core': None,
        'MetaMask^': {'Brave', 'Chrome', 'Edge'},
        'Opera Browser Wallet': None,
        'Phantom^': {'Brave'},
        'Wasabi Wallet': None,
        'Trezor Suite': None
        }
    
    no_brotli = ['Exodus Wallet']

    sep_list = "\n".join(no_brotli)

    warning = f"The Brotli library is required to parse transactions from the following wallets:\n\n{sep_list}\n\nThese wallets will be omitted from the selection.\n\nPlease downlaod the latest release of Wallet Sleuth or intall the Brotli library to parse data from these wallets."

    messagebox.showwarning('Wallet Sleuth', warning)
