#Generic Imports
import os
import tkinter as tk
import csv

#Tkinter Imports
from tkinter import DISABLED, LEFT, W, IntVar, W, Y,  Frame, StringVar, ttk, messagebox, RIGHT, TOP, HORIZONTAL, VERTICAL, NO, BOTTOM, X

#Wallet Imports





#-----------------------------------------------------------#
#----------------------WINDOW SETTINGS----------------------#
#-----------------------------------------------------------#
#Main Window
ws_window = tk.Tk()
ws_window.resizable(False, False)
ws_window.title("Wallet Sleuth")

ws_window_width = 750
ws_window_height = 500

screen_width = ws_window.winfo_screenwidth()
screen_height = ws_window.winfo_screenheight()

center_x = int(screen_width/2 - ws_window_width / 2)
center_y = int(screen_height/2 - ws_window_height /2)

ws_window.geometry(f'{ws_window_width}x{ws_window_height}+{center_x}+{center_y}')


#Notebook Creation
ws_notebook = ttk.Notebook(ws_window)
ws_notebook.pack(pady=5, padx=5, expand=True)


#Frame Settings
address_identifier = ttk.Frame(ws_notebook, width=750, height=500)
address_identifier_output = ttk.Frame(ws_notebook, width=750, height=500)
log_win = ttk.Frame(ws_notebook, width = 750, height=500)
help_win = ttk.Frame(ws_notebook, width=750, height=500)

address_identifier.pack(fill='both', expand=True)
address_identifier_output.pack(fill='both', expand=True)
log_win.pack(fill='both', expand=True)
help_win.pack(fill='both', expand=True)

ws_notebook.add(address_identifier, text='Address Identifier')
ws_notebook.add(address_identifier_output, text='Output')
ws_notebook.add(log_win, text = 'Process Log')
ws_notebook.add(help_win, text='Help')


ws_window.mainloop()