import tkinter as tk
from tkinter import ttk
from model.Wallet import Wallet

from view.OutputFrame import OutputFrame
from view.HelpFrame import HelpFrame
from view.LoggingFrame import LoggingFrame
from view.AddressIdentifierFrame import AddressIdentifierFrame

# TODO: Maybe have these as globals that can be imported from somewhere
# Could also store them as environment variables, but why 🤷‍♂️
TITLE = "Wallet Sleuth 2.0"
WIDTH = 750
HEIGHT = 500

# TODO: Move this to a helper functions file somewhere
def get_center_screen_geometry(width: int, height: int, tk: tk.Tk) -> str:
    x = int(tk.winfo_screenwidth() / 2 - width / 2)
    y = int(tk.winfo_screenheight() / 2 - height /2)

    return f"{width}x{height}+{x}+{y}"


class WalletSleuthView(tk.Tk):
    def __init__(self, wallets: dict[str, Wallet]) -> None:
        super().__init__()
        self.width = WIDTH
        self.height = HEIGHT
        self.geometry(get_center_screen_geometry(WIDTH, HEIGHT, self))

        self.notebook = None
        
        self.identifier_frame: AddressIdentifierFrame = None
        self.output_frame: OutputFrame = None
        self.logging_frame: LoggingFrame = None
        self.help_frame: HelpFrame = None

        self.__create_ui(wallets)
    
    def __create_ui(self, wallets) -> None:
        self.title(TITLE)

        # Notebook Creation
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=5, padx=5, expand=True)

        self.identifier_frame = AddressIdentifierFrame(self, wallets)
        self.output_frame = OutputFrame(self)
        self.logging_frame = LoggingFrame(self)
        self.help_frame = HelpFrame(self)

        self.notebook.add(self.identifier_frame, text="Address Identifier")
        self.notebook.add(self.output_frame, text="Output")
        self.notebook.add(self.logging_frame, text="Process Log")
        self.notebook.add(self.help_frame, text="Help")
    