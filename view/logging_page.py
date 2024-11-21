#tkinter imports
import tkinter as tk
import tkinter.ttk as ttk


class Logging_Frame(ttk.Frame):
    def __init__(self, container) -> None:
        super().__init__()
        self.logging_text_win = tk.Text(self, height=500, width = 500)
        self.logging_text_win.pack()
        self.logging_text_win.config(state=tk.DISABLED)