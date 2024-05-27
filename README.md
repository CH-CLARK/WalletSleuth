# WalletSleuth
Wallet Sleuth is a triage tool that aims to quickly identify user cryptocurrency addresses and transactions from a variety of wallet applications!

<p float="center">
  <img src="https://github.com/CH-CLARK/WalletSleuth/assets/117690646/c0027ccb-a079-4084-b47c-e58112b81821" width="45%" />
  <img src="https://github.com/CH-CLARK/WalletSleuth/assets/117690646/74ff07f6-8d14-4926-ab3b-08cac8eb2971" width="45%" />
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
  <img src="https://github.com/CH-CLARK/WalletSleuth/assets/117690646/e3b3290d-bc57-4465-aafe-6e56054f2452" width="45%" />
  <img src="https://github.com/CH-CLARK/WalletSleuth/assets/117690646/bfc9f6ee-09bf-430a-95a6-da96f3af02da" width="45%" />
  
</p>

## Supported Wallets
- Atomic Wallet
- Bitcoin Core
- Bitget (Brave, Chrome) (Formerly Bitkeep)
- Brave Browser Wallet
- Coinbase Wallet (Chrome)
- Exodus Wallet
- Guarda (Chrome)
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
- To parse Transaction IDs from the cache, the brotli extension is required.



<p align="center">
  <strong><span style="font-size: 36px;">REMEMBER TO CONFIRM YOU OWN FINDINGS!</span></strong>
</p>
