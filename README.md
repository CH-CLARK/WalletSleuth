# Wallet Sleuth
Wallet Sleuth is a cryptocurrency discovery and triage tool, that aims to quickly identify user cryptocurrency addresses and transactions from a variety of popular wallet applications!

## Usage 👩🏻‍💻
Wallet Sleuth can be used via a simple web-based user interface or a command line interface (CLI). Command line interface (CLI) instructions can be found further within this README.

To start the web-based user interface, run "wallet_sleuth.py" or the packaged "wallet_sleuth.exe", and visit [127.0.0.1:5000](127.0.0.1:5000).

<img src="docs/WS_GIF2.gif"/>


### Identify 🔍
Wallet Sleuth requires three inputs: User Directory, Output Directory and Wallet Selection.

Any identified cryptocurrency addresses and transactions are immediatly displayed in the 'Output' tab directly within the 'Identify' page, a log is also produced and can be viewed on the same page under the 'Process Log' tab. A CSV of the identified data and a log file is produced to the output directory.

##### Supported Wallets
|Type                   |Wallet 	                 |Supported Operating Systems |Supported Browsers
|-----------------------|----------------------------|----------------------------|-------------------|
|💻 Desktop             |Atomic Wallet		         |Windows, Macintosh 	      |N/A
|💻 Desktop             |Bitcoin Core		         |Windows, Macintosh          |N/A
|🧩 Browser Extension   |Bitget				         |Windows, Macintosh          |Brave, Chrome
|🧩 Browser Extension   |Coinbase Wallet	         |Windows, Macintosh          |Brave, Chrome
|🧩 Browser Extension   |Crypto.com Wallet		     |Windows, Macintosh   	      |Brave, Chrome
|💻 Desktop             |Dogecoin Core		         |Windows, Macintosh	      |N/A
|💻 Desktop             |Exodus     		         |Windows, Macintosh          |N/A
|🧩 Browser Extension   |Guarda				         |Windows, Macintosh  	      |Brave, Chrome
|💻 Desktop             |Guarda     		         |Windows                     |N/A
|💻 Desktop             |Ledger Live		         |Windows, Macintosh          |N/A
|💻 Desktop             |Litecoin Core		         |Windows, Macintosh          |N/A
|🧩 Browser Extension   |MetaMask Development Build  |Windows                     |Chrome
|🧩 Browser Extension   |MetaMask			         |Windows, Macintosh	      |Brave, Chrome, Edge
|🧩 Browser Extension   |Phantom			         |Windows, Macintosh          |Brave, Chrome, Edge
|🧩 Browser Extension   |Rainbow			         |Windows, Macintosh          |Chrome
|🧩 Browser Extension   |Solflare Wallet	         |Windows         		      |Chrome
|🧩 Browser Extension   |Tonkeeper      	         |Windows         		      |Chrome
|💻 Desktop             |Trezor Suite		         |Windows, Macintosh	      |N/A
|🧩 Browser Extension   |Trust Wallet		         |Windows         		      |Chrome
|💻 Desktop             |Wasabi Wallet		         |Windows, Macintosh          |N/A


#### Address Lookup
Quick and simple address lookup with direct links to the most popular and powerful blockexplorers!

<img src="docs/third_party_icons/blockchair.logo.onwhite.png" width=200>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="docs/third_party_icons/etherscan-logo.png" width=200/>


## CLI Usage
### Using the CLI
Wallet Sleuth can be operated via a command line interface (CLI). Below is an example command:

```
wallet_sleuth_cli.py -p 'C:/Users/USER.PROFILE' -o 'A:/output/path' -os WIN --all_wallets
```

The `-os` flag is required and must be either `WIN` or `MAC`. Exactly one wallet flag must be specified — `--all_wallets`, `--browser_wallets`, or  `--desktop_wallets`.

Run `wallet_sleuth_cli.py -h` for full usage information.

## Limitations 🚩
- Requires Python 3.8 or above.
- To parse Transaction IDs from the Exodus and Guarda cache, the brotli extension is required.
- Macintosh support is currently untested!

