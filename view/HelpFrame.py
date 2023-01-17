import tkinter as tk
from tkinter import DISABLED, Frame

# Tutorial used: https://www.pythontutorial.net/tkinter/tkinter-object-oriented-frame/
class HelpFrame(Frame):
    def __init__(self, container) -> None:
        super().__init__(container)
        self.help_textarea = tk.Text(self, bg='lightgrey', height=500, width=500)
        self.help_textarea.pack()

        self.__set_help_text()
        self.help_textarea.config(state=DISABLED, wrap='word')

    def __set_help_text(self):
        with open("app_files/help_win.txt", "r") as help_text:
            self.help_textarea.insert(0.0, help_text.read())
