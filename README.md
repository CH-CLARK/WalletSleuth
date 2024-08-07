# WalletSleuth
Wallet Sleuth is a triage tool that aims to quickly identify user cryptocurrency addresses and transactions from a variety of wallet applications!

<p float="center">
  <img src="https://github.com/CH-CLARK/WalletSleuth/assets/117690646/067a1942-caf5-4c37-b366-ff32e154ecfa" width="45%" />
  <img src="https://github.com/CH-CLARK/WalletSleuth/assets/117690646/3dd518af-8aef-415f-acf9-fa80a0d664b3" width="45%" />
</p>

## Usage
Wallet Sleuth requires three main inputs: Appdata, Output and Wallet Selection.

Appdata - The AppData directory of the user.

Output - The Output directory for CSV files containing identified addresses and log files.

Wallet Selection - Wallet applications to search for cryptocurrency addresses through.

After running, an information box will notify you when the search is complete. Any identified cryptocurrency addresses are displayed in the output window and a log file details actions and errors in the search.

### Other Functions
Connected Hardware Wallet Detector - Check for previously connected Hardware Wallets such as Trezor or Ledger, amoung others.

Wallet Detector - Determine what wallets to scan for addresses on by identifying currently installed wallets.

<p float="center">
  <img src="https://github.com/CH-CLARK/WalletSleuth/assets/117690646/2c687e42-59dc-4745-9950-296248ca7632" width="45%" />
  <img src="https://github.com/CH-CLARK/WalletSleuth/assets/117690646/0900f067-005f-4c4f-9a31-2bc1221ed9d8" width="45%" />
  
</p>

## Supported Wallets
- Atomic Wallet
- Bitcoin Core
- Bitget (Brave, Chrome) (Formerly Bitkeep)
- Brave Browser Wallet
- Coinbase Wallet (Brave, Chrome)
- Crypto.com Wallet (Chrome)
- Exodus Wallet
- Guarda (Chrome, Opera)
- Ledger Live
- Litecoin Core
- MetaMask (Brave, Chrome, Edge)
- Opera Browser Wallet
- Phantom (Brave, Chrome)
- Wasabi Wallet

## Limitations
- Currently the wallet finder function is limited to wallets in the 'Default' browser user profile, but the address finder will check all profiles for the selected browser.
- Support for Windows OS only.
- Requires Python 3.8 or higher
- To parse Transaction IDs from the Exodus cache, the brotli extension is required.



<p align="center">
  <strong><span style="font-size: 36px;">REMEMBER TO CONFIRM YOU OWN FINDINGS!</span></strong>
</p>
