#generic imports
import csv

#tkinter imports
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import DISABLED

#view imports
from view.address_identifier_frame import Address_Identifier_Frame
from view.output_frame import Output_Frame
from view.logging_frame import Logging_Frame
from view.help_frame import Help_Frame

#controller imports
import controller.config


TITLE = "Wallet Sleuth 2.0"
WIDTH = 750
HEIGHT = 500

def get_center_screen_geometry(width: int, height: int, tk: tk.Tk) -> str:
    x = int(tk.winfo_screenwidth() / 2 - width / 2)
    y = int(tk.winfo_screenheight() / 2 - height /2)

    return f"{width}x{height}+{x}+{y}"

class WS_Main_Window(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        #window config
        self.title(TITLE)
        self.resizable(False, False)
        self.geometry(get_center_screen_geometry(WIDTH, HEIGHT, self))

        #notebook
        self.notebook = ttk.Notebook(self, width=750, height=500)

        self.address_identifer_frame = Address_Identifier_Frame(self.notebook)
        self.output_frame = Output_Frame(self.notebook)
        self.logging_frame = Logging_Frame(self.notebook)
        self.help_frame = Help_Frame(self.notebook)
        
        self.notebook.add(self.address_identifer_frame, text='Address Identifier')
        self.notebook.add(self.output_frame, text='Output')
        self.notebook.add(self.logging_frame, text='Process Log')
        self.notebook.add(self.help_frame,text ='Help')

        self.notebook.pack()

        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_changed)
        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_changed2)

    def on_tab_changed(self, event):
        output_dir = controller.config.OUTPUT

        tab_title = event.widget.tab('current')['text']
        # print(tab_title)

        if tab_title != "Output":
            # Prevent running on other tabs
            return
        
        if not output_dir:
            return

        # Following line test for deleting rows
        self.output_frame.tree.insert("", 0, values=("currency", "address", "wallet", "path"))
        self.output_frame.tree.delete(*self.output_frame.tree.get_children())

        with open(f'{output_dir}/output.csv') as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                currency = row['Currency']
                address = row['Address']
                wallet = row['Wallet']
                path = row['Path']
                self.output_frame.tree.insert("", 0, values=(currency, address, wallet, path))

    def on_tab_changed2(self, event):
        output_dir = controller.config.OUTPUT

        tab_title = event.widget.tab('current')['text']
        # print(tab_title)

        if tab_title != "Process Log":
            # Prevent running on other tabs
            return
        
        if not output_dir:
            return

        with open(output_dir + '/' + 'WalletSleuth_log.txt', 'r') as log_file:
            read_log = log_file.read()

            self.logging_frame.logging_text_win.insert(tk.END, read_log)
            self.logging_frame.logging_text_win.config(state=DISABLED)
