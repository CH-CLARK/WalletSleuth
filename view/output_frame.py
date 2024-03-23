#generic imports
import csv

#tkinter imports
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import TOP, HORIZONTAL, VERTICAL, RIGHT, BOTTOM, Y, X, NO, W

#controller imports
import controller.config


class Output_Frame(ttk.Frame):

    def __init__(self, container) -> None:
        super().__init__()
        self.table_margin = tk.Frame(self, width=500)
        self.table_margin.pack(side=TOP)

        self.scrollbar_x = tk.Scrollbar(self.table_margin, orient=HORIZONTAL)
        self.scrollbar_y = tk.Scrollbar(self.table_margin, orient=VERTICAL)

        self.tree = ttk.Treeview(self.table_margin, columns=("Type", "Currency", "Address", "Wallet", "Path"), height=400, selectmode="extended", yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)
        
        self.scrollbar_y.config(command=self.tree.yview)
        self.scrollbar_y.pack(side=RIGHT, fill=Y)
        self.scrollbar_x.config(command=self.tree.xview)
        self.scrollbar_x.pack(side=BOTTOM, fill=X)

        self.tree.heading('Type', text="Type", anchor=W)
        self.tree.heading('Currency', text="Currency", anchor=W)
        self.tree.heading('Address', text="Address/ Transaction", anchor=W)
        self.tree.heading('Wallet', text="Wallet", anchor=W)
        self.tree.heading('Path', text='Path', anchor=W)
        
        self.tree.column('#0', stretch=NO, minwidth=0, width=0)
        self.tree.column('#1', stretch=NO, minwidth=0, width=100)
        self.tree.column('#2', stretch=NO, minwidth=0, width=75)
        self.tree.column('#3', stretch=NO, minwidth=0, width=200)
        self.tree.column('#4', stretch=NO, minwidth=0, width=100)
        self.tree.column('#5', stretch=NO, minwidth=0, width=800)
        self.tree.pack()

    #Something for a laterdate maybe...
    # def color_code_btc_rows(self):
    #     for item in self.tree.get_children():
    #         values = self.tree.item(item, 'values')
    #         if values and 'Roaming/Ledger Live' in values[4]:
    #             self.tree.item(item, tags=('btc_row',))

    #     self.tree.tag_configure('btc_row', background='orange')