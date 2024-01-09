#tkinter imports
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import LEFT, Y, RIGHT, DISABLED
from tkinter.filedialog import askdirectory

#model imports
from model.wallets_list import names

#view imports
import controller.config

#controller imports 
from controller.wallet_selector import Wallet_Selector
from controller.wallet_selection_check import run_func

#wallet imports
from wallet_scripts.hardware_wallet_scan import hardware_wallet_scan
from wallet_scripts.wallet_scan import wallet_scan

class Address_Identifier_Frame(ttk.Frame):
    def __init__(self, container: ttk.Notebook) -> None:
        super().__init__()

        self.button_labelframe = ttk.LabelFrame(self)

        self.right_canvas = tk.Canvas(self.button_labelframe, width=400, height=400)
        self.right_canvas.pack(side=RIGHT)

        self.button_canvas = tk.Canvas(self.button_labelframe, width=300, height=400)
        self.button_canvas.pack(side=LEFT)

        self.button_canvas_yscroll = ttk.Scrollbar(self.button_labelframe, orient='vertical', command=self.button_canvas.yview)
        self.button_canvas_yscroll.pack(side=LEFT, fill=Y)

        self.button_canvas.configure(yscrollcommand=self.button_canvas_yscroll.set)
        self.button_canvas.bind('<Configure>', lambda e: self.button_canvas.configure(scrollregion=self.button_canvas.bbox('all')))

        self.button_frame = ttk.Frame(self.button_canvas)
        self.button_canvas.create_window((0,0), window=self.button_frame, anchor='nw')
        
        self.button_labelframe.pack(fill = 'both', expand = 'yes', padx = 10, pady = 10)

        self.wallet_selector = Wallet_Selector.wallet_selection(self, container, names)


        #wallet Finder Button
        HW_wallet_button = tk.Button(self.right_canvas, text='Connected Hardware Wallet Detector',justify='center', command = hardware_wallet_scan)
        HW_wallet_button.place(x=10, y=200, height=25, width=385)

        wallet_scan_button = tk.Button(self.right_canvas, text='Wallet Detector',justify='center', command = wallet_scan)
        wallet_scan_button.place(x=10, y=230, height=25, width=385)

        #AppData Button
        def select_appdata():
            ask_dir = askdirectory(title='Select AppData Folder')
            entry=ttk.Label(self.right_canvas, text=ask_dir).place(x=135, y=310)
            controller.config.APPDATA = ask_dir
        appdata_button = tk.Button(self.right_canvas, text='Appdata Directory', command=select_appdata)
        appdata_button.place(x=10, y=310, height=25, width=120)
        

        #OutputButton
        def select_output():
            output_dir = askdirectory(title='Select Output Folder')
            entry=ttk.Label(self.right_canvas, text=output_dir).place(x=135, y=340)
            controller.config.OUTPUT = output_dir
        output_button = tk.Button(self.right_canvas, text='Output Directory', command=select_output)
        output_button.place(x=10, y=340, height=25, width=120)

        #Run Button
        run_button = tk.Button(self.right_canvas, text='Run', command=run_func)
        run_button.place(x=10, y=370, height=25, width=120)