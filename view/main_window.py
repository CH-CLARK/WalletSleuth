#generic imports
import sys
import os
import csv

#tkinter imports
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import DISABLED

#view imports
from view.selection_page import Selection_Frame
from view.output_page import Output_Frame
from view.logging_page import Logging_Frame
from view.help_page import Help_Frame

#controller imports
import controller.config


TITLE = "Wallet Sleuth"
WIDTH = 750
HEIGHT = 500


def get_center_screen_geometry(width: int, height: int, tk_instance: tk.Tk) -> str:
    x = int(tk_instance.winfo_screenwidth() / 2 - width / 2)
    y = int(tk_instance.winfo_screenheight() / 2 - height / 2)
    return f"{width}x{height}+{x}+{y}"

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Main_Window(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.title(TITLE)
        self.resizable(False, False)
        self.geometry(get_center_screen_geometry(WIDTH, HEIGHT, self))

        icon_path = resource_path('app_files/icon.ico')
        self.iconbitmap(icon_path)

        self.notebook = ttk.Notebook(self, width=WIDTH, height=HEIGHT)

        #notebook
        self.selection_page = Selection_Frame(self.notebook)
        self.output_page = Output_Frame(self.notebook)
        self.logging_page = Logging_Frame(self.notebook)
        self.help_page = Help_Frame(self.notebook)

        self.notebook.add(self.selection_page, text='Wallet Sleuth')
        self.notebook.add(self.output_page, text='Output')
        self.notebook.add(self.logging_page, text='Process Log')
        self.notebook.add(self.help_page, text='Help')

        self.notebook.pack()

        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_changed)
        # self.output_page.tree.bind('<<TreeviewSelect>>', self.on_row_selected)


    # def on_row_selected(self, event): #Prehaps an idea for later
    #     selected_item = self.output_page.tree.focus()
    #     row_data = self.output_page.tree.item(selected_item, 'values')

    #     if row_data:
    #         print(row_data)


    #tab chaneg
    def on_tab_changed(self, event):
        output_dir = controller.config.OUTPUT

        tab_title = event.widget.tab('current')['text']

        if not output_dir:
            return

        self.output_page.tree.delete(*self.output_page.tree.get_children())

        if tab_title == 'Output':
            self.load_output_content(output_dir)
            # self.output_page.color_code_btc_rows()  #apply color to row - soemthign for a later date maybe

        if tab_title == 'Process Log':
            self.load_log_content(output_dir)
            

    def load_output_content(self, output_dir):
        self.output_page.tree.insert("", 0, values=("type", "currency", "address", "wallet", "path"))
        self.output_page.tree.delete(*self.output_page.tree.get_children())
        
        output_file_path = resource_path(os.path.join(output_dir, 'output.csv'))
        with open(output_file_path) as f:
            reader = csv.DictReader(f, delimiter=',')
            for row in reader:
                data_type = row['Type']
                currency = row['Currency']
                address = row['Address']
                wallet = row['Wallet']
                path = row['Path']
                self.output_page.tree.insert("", 0, values=(data_type, currency, address, wallet, path))


    def load_log_content(self, output_dir):
        log_name = controller.config.WS_MAIN_LOG_NAME
        log_file_path = resource_path(os.path.join(output_dir, log_name))

        with open(log_file_path, 'r') as log_file:
            read_log = log_file.read()

            self.logging_page.logging_text_win.config(state=tk.NORMAL)
            self.logging_page.logging_text_win.delete(1.0, tk.END)
            self.logging_page.logging_text_win.insert(tk.END, read_log)
            self.logging_page.logging_text_win.config(state=DISABLED)