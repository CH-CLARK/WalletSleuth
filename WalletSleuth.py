#Generic Imports
import os
import csv

#Tkinter Imports
import tkinter as tk
from tkinter import DISABLED, LEFT, W, IntVar, W, Y,  Frame, StringVar, ttk, messagebox, RIGHT, TOP, HORIZONTAL, VERTICAL, NO, BOTTOM, X
from tkinter.filedialog import askdirectory

#Wallet Imports
from wallet_scripts.WS_atomic_wallet import atomic_wallet_dump
from wallet_scripts.WS_metamask import metamask_chrome_dump, metamask_edge_dump, metamask_brave_dump
from wallet_scripts.WS_bravebrowser import bravebrowser_dump

selection = []

#-----------------------------------------------------------#
#---------------------PRIMARY FUNCTIONS---------------------#
#-----------------------------------------------------------#
'''
'address_finder_run' function puts the program all together. Doing the following:
    - Logging page setup (1)
    - Tree Management (2)
    - Wallet selection management(3)
'''
def address_finder_run():
    #(1) - Logging page setup
    with open(P + '/' + 'WalletSleuth_log.txt', 'w') as log_file:
        log_file.write('+-----------------------------------------------------------------------------------------+\n')
        log_file.write('|----------------------------------- WALLET SLEUTH LOG -----------------------------------|\n')
        log_file.write('+-----------------------------------------------------------------------------------------+\n')

    #(2) - Resets the table when 'Run' is selected
    for i in tree.get_children():
        tree.delete(i)
        address_identifier_output.update

    #(3) - Wallet selction management
    #-------------------------------------# 
    #-----------WALLET SELCTION-----------#
    #-------------------------------------# 
    #Atomic Wallet
    if atomic_wallet_var.get() == 1:
        try:
            atomic_wallet_dump(X, P)
            selection.append(P + '/' + 'atomic_wallet_addresses.csv')
        except:
            with open(P + '/' + 'WalletSleuth_log.txt', 'a') as log_file:
                log_file.write("ERROR: (ATOMIC WALLET) - Wallet not found!\n")
    
    #MetaMask
    if metamask_var.get() == 1 and metamask_dropdown.get() == "Chrome":
        try:
            metamask_chrome_dump(X, P)
            selection.append(P + '/' + 'MM_chrome_addresses.csv')
        except:
            with open(P + '/' + 'WalletSleuth_log.txt', 'a') as log_file:
                log_file.write("ERROR: (METAMASK - CHROME) - Wallet not found!\n")

    if metamask_var.get() == 1 and metamask_dropdown.get() == "Edge":
        try:
            metamask_edge_dump(X, P)
            selection.append(P + '/' + 'MM_edge_addresses.csv')
        except:
            with open(P + '/' + 'WalletSleuth_log.txt', 'a') as log_file:
                log_file.write("ERROR: (METAMASK - EDGE) - Wallet not found!\n")

    if metamask_var.get() == 1 and metamask_dropdown.get() == "Brave":
        try:
            metamask_brave_dump(X, P)
            selection.append(P + '/' + 'MM_brave_addresses.csv')
        except:
            with open(P + '/' + 'WalletSleuth_log.txt', 'a') as log_file:
                log_file.write("ERROR: (METAMASK - EDGE) - Wallet not found!\n")

    #Brave Browser Wallet
    if brave_browser_var.get() == 1:
        try:
            bravebrowser_dump(X, P)
            selection.append(P + '/' + 'bravebrowser_addresses.csv')
        except:
            with open(P + '/' + 'WalletSleuth_log.txt', 'a') as log_file:
                log_file.write("ERROR: (BRAVE BROWSER) - Wallet not found!\n")

    #Bitkeep

    #-------------------------------------# 
    #-------------------------------------# 

    with open(P + '/' + 'output.csv','w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Currency', 'Address', 'Wallet', 'Path'])
        for file in selection:
            with open(file,'r', newline='') as f1:
                reader = csv.reader(f1)
                new_data = [row for row in reader]
                writer.writerows(new_data)
    
    with open(P + '/' + 'output.csv') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            currency = row['Currency']
            address = row['Address']
            wallet = row['Wallet']
            path = row['Path']
            tree.insert("", 0, values=(currency, address, wallet, path))

    selection.clear()

    with open(P + '/' + 'WalletSleuth_log.txt', 'r') as log_file:
        read_log = log_file.read()

    logging_text_win.insert(tk.END, read_log)
    logging_text_win.config(state=DISABLED)


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

phantom_var = tk.IntVar()
phantom_drop = tk.StringVar()


#WS - Checkbox Wallet Selection
atomic_wallet_check = ttk.Checkbutton(button_frame, text = "Atomic Wallet", variable=atomic_wallet_var, onvalue=1, offvalue=0)
atomic_wallet_check.grid(row=[1], column=[0])

metamask_check = ttk.Checkbutton(button_frame, text = "MetaMask", variable=metamask_var, onvalue=1, offvalue =0).grid(row=[2], column=[0], sticky=W)
metamask_dropdown.set("Select Browser ")
metamask_drop = tk.OptionMenu(button_frame, metamask_dropdown, "Brave", "Chrome", "Edge", "-Firefox", "-Opera")
metamask_drop.grid(row = 2, column=1)

brave_wallet_check = ttk.Checkbutton(button_frame, text = "Brave Browser", variable = brave_browser_var, onvalue=1, offvalue=0).grid(row=[3], column=[0])

bitkeep_check = ttk.Checkbutton(button_frame, text = "Bitkeep", variable=bitkeep_var, onvalue=1, offvalue =0).grid(row=[4], column=[0], sticky=W)
bitkeep_dropdown.set("Select Browser ")
bitkeep_drop = tk.OptionMenu(button_frame, bitkeep_dropdown, "-Brave", "Chrome", "-Firefox", "-Opera")
bitkeep_drop.grid(row = 4, column=1)

nami_check = ttk.Checkbutton(button_frame, text = "Nami", variable=nami_var, onvalue=1, offvalue =0).grid(row=[5], column=[0], sticky=W)
nami_dropdown.set("Select Browser ")
nami_drop = tk.OptionMenu(button_frame, nami_dropdown, "-Brave", "Chrome", "-Firefox", "-Opera")
nami_drop.grid(row = 5, column=1)

phantom_check = ttk.Checkbutton(button_frame, text = "Phantom", variable=phantom_var, onvalue=1, offvalue=0).grid(row=[6], column=[0], sticky=W)
phantom_drop.set("Select Browser ")
phantom_drop = tk.OptionMenu(button_frame, phantom_drop, "-Brave", "Chrome", "-Firefox", "-Opera")
phantom_drop.grid(row = 6, column=1)

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


#===========================================================#
#------------------------LOGGING PAGE-----------------------#
#===========================================================#
#Logging Text Window
logging_text_win = tk.Text(log_win, height=500, width = 500)
logging_text_win.pack()


ws_window.mainloop()