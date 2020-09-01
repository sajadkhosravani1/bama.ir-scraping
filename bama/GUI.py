from tkinter import ttk
import tkinter as tk

from bama.car import Car

root = tk.Tk()
def something():
    print("some thing")
tk.Button(root, text ="Hello", command = something).grid(row=0,column=0)
tk.Button(root, text ="Hello", command = something).grid(row=0,column=1)
tk.Button(root, text ="Hello", command = something).grid(row=1,column=2)
tk.Button(root, text ="Hello", command = something).grid(row=2,column=2)


def table(root, brand=None, model=None):
    panel = tk.PanedWindow(root)
    panel.grid(row=1, column=0, columnspan=2, rowspan=2)
    # window.resizable(width=1, height=1)



    treeView = ttk.Treeview(panel, selectmode='browse')
    treeView.pack(side='right')
    verscrlbar = ttk.Scrollbar(panel,
                               orient="vertical",
                               command=treeView.yview)
    verscrlbar.pack(side='right', fill='x')
    treeView.configure(xscrollcommand=verscrlbar.set)


    treeView["columns"] = ('1', '2', '3', '4', '5', '6')
    treeView['show'] = 'headings'

    # treeView.column("1", width=90, anchor='c')
    # treeView.column("2", width=90, anchor='se')

    i=1
    for colHead in Car.TABLE_HEADERS_PRS:
        treeView.column(str(i), width=90, anchor='se')
        treeView.heading(str(i), text=colHead)
        i+=1

    for row in Car.getAll():
        treeView.insert("", 'end', text="something",
                 values=row)


# Calling mainloop

table(root)
root.mainloop()