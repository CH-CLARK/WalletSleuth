#tkinter imports
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import LEFT, W


class Wallet_Selector(ttk.Frame):
    selection = []
    checkbuttons = []
    drink_menus = []

    def __init__(self) -> None:
        super().__init__()
        pass

    def wallet_selection(self, container, names):
        #creates the checkboxes and dropdowns
        for row, (name, drinks) in enumerate(sorted(names.items())):
            check_value = tk.BooleanVar(value=False)
            checkbutton = tk.Checkbutton(self.button_frame, text=name, variable=check_value)
            Wallet_Selector.checkbuttons.append(checkbutton)
            checkbutton.grid(row=row, column=0, sticky='w')

            if drinks is not None:
                drink_var = tk.StringVar(value=list(drinks)[0])
                drink_menu = tk.OptionMenu(self.button_frame, drink_var, *list(drinks))
                Wallet_Selector.drink_menus.append(drink_menu)
                drink_menu.grid(row=row, column=1, sticky='w')

                drink_var.trace_add('write', lambda *args, check_value=check_value, drink_var=drink_var, name=name, drinks=drinks: on_select(check_value, drink_var, name, drinks))

            else:
                drink_var = None

            checkbutton.config(command=lambda check_value=check_value, drink_var=drink_var, name=name, drinks=drinks: on_select(check_value, drink_var, name, drinks))


        #adds and removes a selection to the 'selection' list                
        def on_select(check_value, drink_var, name, drinks):
            if drinks is None:
                if check_value.get():
                    if name not in [item[0] for item in Wallet_Selector.selection]:
                        Wallet_Selector.selection.append((name, None))
                else:
                    if (name, None) in Wallet_Selector.selection:
                        Wallet_Selector.selection.remove((name, None))
            else:
                if check_value.get():
                    for item in Wallet_Selector.selection:
                        if item[0] == name:
                            Wallet_Selector.selection.remove(item)
                            break
                    Wallet_Selector.selection.append((name, drink_var.get()))
                else:
                    if (name, drink_var.get()) in Wallet_Selector.selection:
                        Wallet_Selector.selection.remove((name, drink_var.get()))

'''
If looking at this code makes you thirsty, that is because during testing it was a drink selector script! When i finally got it working it was copied into WalletSleuth and i
forgot to change the varible names! It must have been a very late night. Im leaving it like this for now because i find it funny. 

You can just assume that 'drinks' and anything related are actually browsers...
'''