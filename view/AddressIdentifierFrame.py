from pathlib import Path
from typing import Callable

import tkinter as tk
from tkinter import ttk, constants
from tkinter import Frame
from model.Browser import Browser

from model.Wallet import Wallet

class WalletSelection:
    def __init__(self, wallet: Wallet):
        self.wallet = wallet
        
        self._checked_value: tk.IntVar =  tk.IntVar()
        self._dropdown_value: tk.StringVar = tk.StringVar()

        self.default_dropdown_value = "Select Browser "
        self._dropdown_value.set(self.default_dropdown_value)
    
    @property
    def is_selected(self) -> bool:
        return self._checked_value.get() == 1
    
    @property
    def selected_browser_value(self) -> str:
        return self._dropdown_value.get()
    
    @property
    def selected_browser(self) -> Browser:
        if self.selected_browser_value == self.default_dropdown_value:
            return None

        for browser in self.wallet.browsers:
            if browser.name == self.selected_browser_value:
                return browser

        return None

    def get_dumper(self) -> Callable[[str, str], None]:
        if self.selected_browser is not None:
            return self.selected_browser.dumper

        return self.wallet.dumper

    def __str__(self):
        checkmark = "X" if self.is_selected else " "
        browser_options = f": {self.selected_browser.name}" if self.selected_browser is not None else ""
        return f"[{checkmark}] {self.wallet.name}{browser_options}"


# Tutorial used: https://www.pythontutorial.net/tkinter/tkinter-object-oriented-frame/
class AddressIdentifierFrame(Frame):
    def __init__(self, container, wallets: dict[str, Wallet]) -> None:
        super().__init__(container)

        self._output_path = None
        self._appdata_path = None
        self._log_file_path = None

        self.run_button: tk.Button = None
        self.select_output_button: tk.Button = None
        self.open_appdata_button: tk.Button = None

        self.output_label: ttk.Label = None
        self.appdata_label: ttk.Label = None

        self.wallets = { key: WalletSelection(wallet) for (key, wallet) in wallets.items() }
        self.__build_ui()

    def get_wallets(self) -> list[WalletSelection]:
        return [ws for ws in self.wallets.values()]

    def get_selected_wallets(self) -> list[WalletSelection]:
        return [ws for ws in self.wallets.values() if ws.is_selected]

    def set_output_path_label(self, path: Path) -> None:
        self.output_label.config(text=path)

    def set_appdata_path_label(self, path):
        self.appdata_label.config(text=path)

    def set_log_path(self, path: Path) -> None:
        self._log_file_path = path

    def bind_run_button(self, callback: Callable[[tk.Event], None]) -> None:
        self.run_button.bind("<Button-1>", callback)

    def bind_select_output_button(self, callback: Callable[[tk.Event], None]) -> None:
        self.select_output_button.bind("<Button-1>", callback)

    def bind_open_appdata_button(self, callback: Callable[[tk.Event], None]) -> None:
        self.open_appdata_button.bind("<Button-1>", callback)

    def __build_ui(self):
        self.button_labelframe = ttk.LabelFrame(self)
        self.button_labelframe.pack(fill="both", expand="yes", padx=10, pady =10)

        self.output_label = ttk.Label(self.button_labelframe, text="")
        self.output_label.place(x=450, y=330)
        self.appdata_label = ttk.Label(self.button_labelframe, text="")
        self.appdata_label.place(x=450, y=330)
        
        button_canvas = tk.Canvas(self.button_labelframe, width=300, height=400, bg="#F0F0F0")
        button_canvas.pack(side=constants.LEFT)

        button_canvas_yscrollbar = ttk.Scrollbar(self.button_labelframe, orient=constants.VERTICAL, command=button_canvas.yview)
        button_canvas_yscrollbar.pack(side=constants.LEFT, fill=constants.Y)
        button_canvas.configure(yscrollcommand=button_canvas_yscrollbar.set)
        button_canvas.bind("<Configure>", lambda e: button_canvas.configure(scrollregion=button_canvas.bbox(constants.ALL)))

        button_frame = ttk.Frame(button_canvas)
        button_canvas.create_window((0, 0), window=button_frame, anchor = "nw")

        self.__build_wallet_selections(container=button_frame)
        self.__build_buttons(container=self.button_labelframe)
    
    def __build_wallet_selections(self, container: Frame) -> None:
        """Builds the UI for the wallet checkboxes and dropdowns"""
        wallets = sorted(self.wallets.values(), key=lambda w: w.wallet.name)

        for i, ws in enumerate(wallets):
            checkbox = ttk.Checkbutton(
                container,
                text=ws.wallet.name,
                variable=ws._checked_value,
                onvalue=1,
                offvalue=0,
            )

            checkbox.grid(row=[i + 1], column=[0], sticky=constants.W)

            if not ws.wallet.has_browsers:
                continue

            dropdown = tk.OptionMenu(container, ws._dropdown_value, *[b.name for b in ws.wallet.browsers])
            dropdown.grid(row=i + 1, column=1)
    
    def __build_buttons(self, container: Frame):
        """Builds the Address Identifier buttons"""
        self.open_appdata_button = tk.Button(container, text="Appdata Directory")
        self.open_appdata_button.place(x=325, y=330, height=25, width=120)

        self.select_output_button = tk.Button(container, text="Output Directory")
        self.select_output_button.place(x=325, y=360, height=25, width=120)

        self.run_button = tk.Button(container, text="Run")
        self.run_button.place(x=325, y=390, height=25, width=120)
    