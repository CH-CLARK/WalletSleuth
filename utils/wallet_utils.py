# ccl imports
from ccl_scripts.ccl_chromium_reader.storage_formats import ccl_leveldb

# generic imports
import re

windows_browser_dict = {
    'brave': '/Local/BraveSoftware/Brave-Browser/User Data',
    'chrome': '/Local/Google/Chrome/User Data',
    'edge': '/Local/Microsoft/Edge/User Data',
    'opera': '/Roaming/Opera Software/Opera Stable'
}

mac_browser_dict = {
    'brave': '/Application Support/BraveSoftware/Brave-Browser',
    'chrome': '/Application Support/Google/Chrome',
    'edge': '/Application Support/Microsoft/Edge',
    'opera': '/Application Support/Opera Software/Opera Stable'
}

currency_types = {
r"(btc|bitcoin)": "Bitcoin (BTC)",
r"(bch|bitcoin cash)": "Bitcoin Cash (BCH)",
r"(bsv|bitcoin cash)": "Bitcoin SV (BSV)",
r"(ltc|litecoin)": "Litecoin (LTC)",
r"(eth|ethereum)": "Ethereum (ETH)",
r"(doge|dogecoin)": "Dogecoin (DOGE)",
r"(xrp|ripple)": "Ripple (XRP)",
r"(ada|cardano)": "Cardano (ADA)",
r"(sol|solana)": "Solana (SOL)",
r"(xmr|monero)": "Monero (XMR)",
r"(dot|polkadot)": "Polkadot (DOT)",
r"(bnb|binance coin)": "Binance Coin (BNB)",
r"(bsc|binance smart chain)": "Binance Smart Chain (BSC)",
r"(trx|tron)": "Tron (TRX)",
r"(xlm|stellar)": "Stella (XLM)",
r"(matic|polygon)": "Polygon (MATIC)",
r"(apt|aptos)": "Aptos (APT)",
r"(avax|avalanche)": "Avalanche (AVAX)",
r"(ftm|fantom)": "Fantom (FTM)",
r"(cro|cronos)": "Cronos (CRO)",

}


def normalize_type(x):
    for currency_type, normalized in currency_types.items():
        if re.fullmatch(currency_type, x, re.IGNORECASE):
            return normalized
    return x


def extract_leveldb_data(directory_path, data_location):
    encoding = "iso-8859-1"

    leveldb_records = ccl_leveldb.RawLevelDb(f"{directory_path}{data_location}")
    location = f"{directory_path}{data_location}"

    csv_data = []
 
    csv_data.append([
        "key-hex", "key-text", "value-text", "seq"
    ])

    for record in leveldb_records.iterate_records_raw():
        csv_data.append([
            record.user_key.hex(" ", 1),
            record.user_key.decode(encoding, "replace"),
            record.value.decode(encoding, "replace"),
            record.seq
        ])

    return csv_data, location