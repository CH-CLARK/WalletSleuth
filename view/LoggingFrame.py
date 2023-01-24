import tkinter as tk
from tkinter import DISABLED, Frame

# Tutorial used: https://www.pythontutorial.net/tkinter/tkinter-object-oriented-frame/
class LoggingFrame(Frame):
    def __init__(self, container) -> None:
        super().__init__(container)
        self.log_textarea = tk.Text(self, height=500, width = 500)
        self.log_textarea.pack()
    
    def update(self, text) -> None:
        self.log_textarea.insert(tk.END, text)
        self.log_textarea.config(state=tk.DISABLED)
