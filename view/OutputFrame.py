import tkinter as tk
from tkinter import ttk, constants
from tkinter import DISABLED, Frame

# Tutorial used: https://www.pythontutorial.net/tkinter/tkinter-object-oriented-frame/
class OutputFrame(Frame):
    def __init__(self, container) -> None:
        super().__init__(container)
        
        # Address Output Table

        scrollbarx = tk.Scrollbar(self, orient=constants.HORIZONTAL)
        scrollbary = tk.Scrollbar(self, orient=constants.VERTICAL)
        
        self.tree = ttk.Treeview(
            self, 
            columns=("Currency", "Address", "Wallet", "Path"), 
            height=400, 
            selectmode="extended", 
            yscrollcommand=scrollbary.set, 
            xscrollcommand=scrollbarx.set)
        
        scrollbary.config(command=self.tree.yview)
        scrollbary.pack(side=constants.RIGHT, fill=constants.Y)
        scrollbarx.config(command=self.tree.xview)
        scrollbarx.pack(side=constants.BOTTOM, fill=constants.X)
        
        self.tree.heading('Currency', text="Currency", anchor=constants.W)
        self.tree.heading('Address', text="Address", anchor=constants.W)
        self.tree.heading('Wallet', text="Wallet", anchor=constants.W)
        self.tree.heading('Path', text='Path', anchor=constants.W)
        self.tree.column('#0', stretch=constants.NO, minwidth=0, width=0)
        self.tree.column('#1', stretch=constants.NO, minwidth=0, width=200)
        self.tree.column('#2', stretch=constants.NO, minwidth=0, width=200)
        self.tree.column('#3', stretch=constants.NO, minwidth=0, width=200)
        self.tree.column('#4', stretch=constants.NO, minwidth=0, width=800)
        self.tree.pack()
    
    def reset(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
            # address_identifier_output.update
