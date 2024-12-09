#tkinter imports
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import PhotoImage

#generic imports
import os
import sys


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Help_Frame(ttk.Frame):
    def __init__(self, container: ttk.Notebook) -> None:
        super().__init__()

        help_file_path = resource_path('app_files/help_file.txt')
        try:
            with open(help_file_path, 'r') as help_file:
                help_text = help_file.read()
        except FileNotFoundError:
            help_text = "Help file not found."

        self.help_text_widget = tk.Text(self, wrap='word')
        self.help_text_widget.insert('1.0', help_text)
        self.help_text_widget.pack(expand=True, fill='both')
        self.help_text_widget.config(state=tk.DISABLED)

