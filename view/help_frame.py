#tkinter imports
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import DISABLED


class Help_Frame(ttk.Frame):
    def __init__(self, container) -> None:
        super().__init__()

        self.help_text_win =  tk.Text(self, bg='grey93', height = 500, width = 500)
        self.help_text_win.pack()

        with open ('app_files/help_file.txt') as help_text:
            self.help_text_win.insert(0.0, help_text.read())
            self.help_text_win.config (state=DISABLED, wrap='word')