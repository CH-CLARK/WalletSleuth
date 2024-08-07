from tkinter import messagebox

try:
    import brotli

    names = {
        'Atomic Wallet': None,
        'Bitget^': {'Brave', 'Chrome'},
        'Brave Browser Wallet': None,
        'Brave Browser Legacy': None,
        'Guarda^': {'Chrome', 'Opera'},
        'MetaMask^': {'Brave', 'Chrome', 'Edge'},
        'Opera Browser Wallet': None,
        'Phantom^': {'Brave','Chrome'},
        'Ledger Live': None,
        'Exodus Wallet': None,
        'Wasabi Wallet': None,
        'Litecoin Core': None,
        'Bitcoin Core': None,
        'Coinbase Wallet^': {'Chrome', 'Brave'},
        'Crypto.com Wallet^': {'Chrome'}
        }

except Exception as e:
    pass
    names = {
        'Atomic Wallet': None,
        'Bitget^': {'Brave', 'Chrome'},
        'Brave Browser Wallet': None,
        'Brave Browser Legacy': None,
        'Guarda^': {'Chrome', 'Opera'},
        'MetaMask^': {'Brave', 'Chrome', 'Edge'},
        'Opera Browser Wallet': None,
        'Phantom^': {'Brave', 'Chrome'},
        'Ledger Live': None,
        # 'Exodus Wallet': None,
        'Wasabi Wallet': None,
        'Litecoin Core': None,
        'Bitcoin Core': None,
        'Coinbase Wallet^': {'Chrome', 'Brave'},
        'Crypto.com Wallet^': {'Chrome'}
        }
    
    no_brotli = ['Exodus Wallet']

    sep_list = "\n".join(no_brotli)

    warning = f"The Brotli library is required to parse transactions from the following wallets:\n\n{sep_list}\n\nThese wallets will be omitted from the selection.\n\nPlease downlaod the latest release of Wallet Sleuth or intall the Brotli library to parse data from these wallets."

    messagebox.showwarning('Wallet Sleuth', warning)
