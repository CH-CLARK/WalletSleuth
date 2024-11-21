#genric imports
import os
import sys

#tkinter imports
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import LEFT, Y, RIGHT, DISABLED, PhotoImage
from tkinter.filedialog import askdirectory

#model imports
from model.wallets_list import names

#controller imports
import controller.config
from controller.wallet_selector import Wallet_Selector
from controller.wallet_selection_check import run_func

#wallet scan imports
from wallet_scripts.scan_functions.hardware_wallet_scan import hardware_wallet_scan
from wallet_scripts.scan_functions.wallet_scan import wallet_scan


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Selection_Frame(ttk.Frame):
    def __init__(self, container: ttk.Notebook) -> None:
        super().__init__()

        self.right_canvas = tk.Canvas(self, width=420, height=500)
        self.right_canvas.pack(side=RIGHT)

        self.left_canvas = tk.Canvas(self, width=300, height=460)
        self.left_canvas.pack(side=LEFT)

        self.left_canvas_yscroll = ttk.Scrollbar(self, orient='vertical', command=self.left_canvas.yview)
        self.left_canvas_yscroll.pack(side=LEFT, fill=Y)

        self.left_canvas.configure(yscrollcommand=self.left_canvas_yscroll.set)
        self.left_canvas.bind('<Configure>', lambda e: self.left_canvas.configure(scrollregion=self.left_canvas.bbox('all')))

        self.button_frame = ttk.Frame(self.left_canvas)
        self.left_canvas.create_window((0,0), window=self.button_frame, anchor='nw')
        

        self.wallet_selector = Wallet_Selector.wallet_selection(self, container, names)

        #appdata function
        def select_appdata():
            entry = ttk.Label(self.right_canvas, text='                                                                                                                       ').place(x=135, y=380)
            ask_dir = askdirectory(title='Select AppData Folder')
            entry = ttk.Label(self.right_canvas, text=ask_dir).place(x=135, y=380)
            controller.config.APPDATA = ask_dir

        #output function
        def select_output():
            entry = ttk.Label(self.right_canvas, text='                                                                                                                       ').place(x=135, y=410)
            output_dir = askdirectory(title='Select Output Folder')
            entry = ttk.Label(self.right_canvas, text=output_dir).place(x=135, y=410)
            controller.config.OUTPUT = output_dir

        #buttons
        HW_wallet_button = tk.Button(self.right_canvas, text='Connected Hardware Wallet Detector', justify='center', command=hardware_wallet_scan)
        HW_wallet_button.place(x=10, y=260, height=25, width=405)

        wallet_scan_button = tk.Button(self.right_canvas, text='Wallet Detector', justify='center', command=wallet_scan)
        wallet_scan_button.place(x=10, y=290, height=25, width=405)

        appdata_button = tk.Button(self.right_canvas, text='Appdata Directory', command=select_appdata)
        appdata_button.place(x=10, y=380, height=25, width=120)

        output_button = tk.Button(self.right_canvas, text='Output Directory', command=select_output)
        output_button.place(x=10, y=410, height=25, width=120)

        run_button = tk.Button(self.right_canvas, text='Run', command=run_func)
        run_button.place(x=10, y=440, height=25, width=120)