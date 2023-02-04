import csv
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

from tkinter.filedialog import askdirectory

from logger import Logger
from model.Wallet import Wallet
from view.WalletSleuthView import WalletSleuthView

class WalletSleuthController:
    def __init__(self, view: WalletSleuthView, wallets: dict[str, Wallet]):
        self.view = view
        self.wallets = wallets

        self.log_path: Path = None
        self.output_path: Path = None
        self.appdata_path: Path = None

        self.log: Logger = None

        self.view.identifier_frame.bind_run_button(self.start_process)
        self.view.identifier_frame.bind_select_output_button(self.select_output)
        self.view.identifier_frame.bind_open_appdata_button(self.select_appdata)

    def mainloop(self):
        self.view.mainloop()

    def select_output(self, event=None):
        self.output_path = Path(askdirectory(title="Select Output Folder")) # shows dialog box and returns the path

        self.log_path = Path(self.output_path, "WalletSleuth_log.txt")
        self.log = Logger(self.log_path)
        self.view.identifier_frame.set_output_path_label(self.output_path)

        self.log.section_divide("WALLET SLEUTH LOG")
    
    def select_appdata(self, event=None):
        self.appdata_path = Path(askdirectory(title="Select Appdata Folder"))
        self.view.identifier_frame.set_output_path_label(self.appdata_path)
    
    def start_process(self, event=None):
        self.log.write("Processing started\n")
        self.view.output_frame.reset()
        
        #
        # Logging the selected items
        #
        # wallet_selection_options = self.view.identifier_frame.get_wallets()        
        # self.log.write("Selections:")
        # for ws in wallet_selection_options:
        #     self.log.write(f"  {ws}")
        # self.log.write("")

        #
        # Iterating through the processed wallets
        #
        selection = []
        selected_wallets = self.view.identifier_frame.get_selected_wallets()

        for ws in selected_wallets:
            self.log.write(f"Processing: {ws}")
            wallet_dumper = ws.get_dumper()

            try:
                normalized_wallet_name = ws.wallet.name.replace(" ", "")
                normalized_browser_name = "" if ws.selected_browser is None else ws.selected_browser.name.replace(" ", "")
                out_file_path = Path(self.output_path, f"{normalized_wallet_name + normalized_browser_name}_addresses.csv")
                selection.append(out_file_path)

                wallet_dumper(self.appdata_path, self.output_path)
            except:
                self.log.write(f"Error: ({ws.wallet.name}) - Wallet not found")

        #
        # TODO: This is broken because I have not wanted to standardize this
        # It would be good to pass the full paths to the processors, rather than have them decide what their
        # paths will be, otherwise you could let them decide and have them return the path upon completion
        #
        # Additionally, could we not have the data returned from these processors, rather than having it
        # written to file?
        #

        # with open(Path(self.output_path, "output.csv"), "w", newline="") as f:
        #     writer = csv.writer(f)
        #     writer.writerow(["Currency", "Address", "Wallet", "Path"])

        #     for file in selection:
        #         with open(file, "r", newline="") as f1:
        #             reader = csv.reader(f1)
        #             new_data = [row for row in reader]
        #             writer.writerows(new_data)
        
        # with open(Path(self.output_path, "output.csv")) as f:
        #     reader = csv.DictReader(f, delimiter=",")
        #     for row in reader:
        #         currency = row["Currency"]
        #         address = row["Address"]
        #         wallet = row["Wallet"]
        #         path = row["Path"]

        #         self.view.output_frame.tree.insert("", 0, values=(currency, address, wallet, path))

        #
        # Update the UI log
        #

        self.view.logging_frame.update(self.log.read())
        messagebox.showinfo(title="Wallet Sleuth", message="Search complete!")
