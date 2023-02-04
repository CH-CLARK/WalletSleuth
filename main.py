from model.Browser import Browser
from model.Wallet import Wallet
from view.WalletSleuthView import WalletSleuthView
from controller.WalletSleuthController import WalletSleuthController

from wallet_scripts.WS_atomic_wallet import atomic_wallet_dump
from wallet_scripts.WS_metamask import metamask_chrome_dump, metamask_edge_dump, metamask_brave_dump
from wallet_scripts.WS_bravebrowser import bravebrowser_dump
from wallet_scripts.WS_bitkeep import bitkeep_chrome_dump, bitkeep_brave_dump
from wallet_scripts.WS_phantom import phantom_chrome_dump, phantom_brave_dump
from wallet_scripts.WS_operabrowser import operabrowser_dump


#add wallets here, will put it in alphabetical also
all_wallets = [
    Wallet(name="Atomic Wallet", dumper=atomic_wallet_dump),

    Wallet("MetaMask", [
        Browser("Brave", metamask_brave_dump), 
        Browser("Chrome", metamask_chrome_dump), 
        Browser("Edge", metamask_edge_dump), 
        Browser("-Firefox"), 
        Browser("-Opera")]
    ),
    Wallet("Brave Browser", dumper=bravebrowser_dump),
    Wallet("Bitkeep", [
        Browser("Brave", bitkeep_brave_dump), 
        Browser("Chrome", bitkeep_chrome_dump), 
        Browser("-Firefox"), 
        Browser("-Opera")]
    ),
    Wallet("Phantom", [
        Browser("Brave", phantom_brave_dump), 
        Browser("Chrome", phantom_chrome_dump), 
        Browser("-Firefox"), 
        Browser("-Opera")]
    ),
    Wallet("Opera Browser", dumper=operabrowser_dump),

    Wallet("Sigered Browser"),
    Wallet("sigs2", [
        Browser("Brave", bitkeep_brave_dump), 
        Browser("Chrome", bitkeep_chrome_dump), 
        Browser("-Firefox"), 
        Browser("-Opera")]
    ),
    Wallet("Sigered Browser1"),
    Wallet("Sigered Browser2"),
    Wallet("Sigered Browser3"),
    Wallet("Sigered Browser4"),
    Wallet("Sigered Browser5"),
    Wallet("Sigered Browser6"),
    Wallet("Sigered Browser7"),
    Wallet("Sigered Browser8"),
    Wallet("Sigered Browser9"),
    Wallet("Sigered Browser399"),
    Wallet("Sigered Browser31"),
    Wallet("Sigered Browser32"),


]

def make_wallets():
    return { wallet.name: wallet for wallet in all_wallets }
#     for wallet in all_wallets:
#         print(wallet.name)
#         for browser in wallet.browsers:
#             print(browser.name)
# make_wallets()


if __name__ == "__main__":
    wallets = make_wallets()
    wallet_sleuth_view = WalletSleuthView(wallets)
    controller = WalletSleuthController(wallet_sleuth_view, wallets)

    controller.mainloop()
