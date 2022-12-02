#Generic Imports
import os
import tkinter as tk
import csv

#Tkinter Imports
from tkinter import DISABLED, LEFT, W, IntVar, W, Y,  Frame, StringVar, ttk, messagebox, RIGHT, TOP, HORIZONTAL, VERTICAL, NO, BOTTOM, X
from tkinter.filedialog import askdirectory

#Wallet Imports


#-----------------------------------------------------------#
#---------------------PRIMARY FUNCTIONS---------------------#
#-----------------------------------------------------------#
def address_finder_run():
    print("TEST FUNC")


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


#===========================================================#
#------------------ADDRESS IDENTIFIER PAGE------------------#
#===========================================================#
#Wallet Selection Frame
button_labelframe= ttk.LabelFrame(address_identifier)

button_canvas = tk.Canvas(button_labelframe, width = 300, height = 400, bg="#F0F0F0")
button_canvas.pack(side=LEFT)

button_canvas_yscrollbar = ttk.Scrollbar(button_labelframe, orient="vertical", command=button_canvas.yview)
button_canvas_yscrollbar.pack(side=LEFT, fill=Y)
button_canvas.configure(yscrollcommand=button_canvas_yscrollbar.set)
button_canvas.bind('<Configure>', lambda e: button_canvas.configure(scrollregion = button_canvas.bbox('all')))

button_frame = ttk.Frame(button_canvas)
button_canvas.create_window((0,0), window=button_frame, anchor = "nw")

button_labelframe.pack(fill="both", expand = "yes", padx = 10, pady =10)


#WSF - Checkbox Selection Varibles
atomic_wallet_var = tk.IntVar()

metamask_var = tk.IntVar()
metamask_dropdown = tk.StringVar()

brave_browser_var = tk.IntVar()

bitkeep_var = tk.IntVar()
bitkeep_dropdown = tk.StringVar()

nami_var = tk.IntVar()
nami_dropdown = tk.StringVar()


#WSF - Checkbox Wallet Selection
atomic_wallet_check = ttk.Checkbutton(button_frame, text = "Atomic Wallet", variable=atomic_wallet_var, onvalue=1, offvalue=0)
atomic_wallet_check.grid(row=[1], column=[0])

metamask_check = ttk.Checkbutton(button_frame, text = "MetaMask", variable=metamask_var, onvalue=1, offvalue =0).grid(row=[2], column=[0], sticky=W)
metamask_dropdown.set("Select Browser ")
metamask_drop = tk.OptionMenu(button_frame, metamask_dropdown, "-Brave", "Chrome", "-Edge", "-Firefox", "-Opera")
metamask_drop.grid(row = 2, column=1)

brave_wallet_check = ttk.Checkbutton(button_frame, text = "Brave Browser", variable = brave_browser_var, onvalue=1, offvalue=0).grid(row=[3], column=[0])

bitkeep_check = ttk.Checkbutton(button_frame, text = "Bitkeep", variable=bitkeep_var, onvalue=1, offvalue =0).grid(row=[4], column=[0], sticky=W)
bitkeep_dropdown.set("Select Browser ")
bitkeep_drop = tk.OptionMenu(button_frame, bitkeep_dropdown, "-Brave", "Chrome", "-Firefox", "-Opera")
bitkeep_drop.grid(row = 4, column=1)

nami_check = ttk.Checkbutton(button_frame, text = "Nami", variable=nami_var, onvalue=1, offvalue =0).grid(row=[5], column=[0], sticky=W)
nami_dropdown.set("Select Browser ")
nami_drop = tk.OptionMenu(button_frame, nami_dropdown, "Brave", "Chrome", "-Firefox", "-Opera")
nami_drop.grid(row = 5, column=1)


#Address Identifier Buttons
run_button = ttk.Button(button_labelframe, text = "Run", command=address_finder_run)
run_button.place(x=325, y=390, height=25, width=120)

def select_output():
    output_dir = askdirectory(title='Select Output Folder') # shows dialog box and returns the path
    entry= ttk.Label(button_labelframe, text= output_dir).place(x=450, y=360)
    global P
    P = output_dir

select_output_button = ttk.Button(button_labelframe, text = "Output Directory", command= select_output)
select_output_button.place(x=325, y=360, height=25, width=120)

def open_appdata():
    ask_dir = askdirectory(title='Select Appdata Folder') # shows dialog box and returns the path
    entry= ttk.Label(button_labelframe, text= ask_dir).place(x=450, y=330)
    global X
    X = ask_dir

open_appdata_button = ttk.Button(button_labelframe, text = "Appdata Directory", command= open_appdata)
open_appdata_button.place(x=325, y=330, height=25, width=120)


#===========================================================#
#------------------------OUTPUT PAGE------------------------#
#===========================================================#
#Address Output Table
TableMargin = tk.Frame(address_identifier_output, width=500)
TableMargin.pack(side=TOP)
scrollbarx = tk.Scrollbar(TableMargin, orient=HORIZONTAL)
scrollbary = tk.Scrollbar(TableMargin, orient=VERTICAL)
tree = ttk.Treeview(TableMargin, columns=("Currency", "Address", "Wallet", "Path"), height=400, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)
tree.heading('Currency', text="Currency", anchor=W)
tree.heading('Address', text="Address", anchor=W)
tree.heading('Wallet', text="Wallet", anchor=W)
tree.heading('Path', text='Path', anchor=W)
tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=200)
tree.column('#2', stretch=NO, minwidth=0, width=200)
tree.column('#3', stretch=NO, minwidth=0, width=200)
tree.column('#4', stretch=NO, minwidth=0, width=800)
tree.pack()












ws_window.mainloop()