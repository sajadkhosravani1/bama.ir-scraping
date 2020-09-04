from tkinter import ttk
import tkinter as tk
from bama.car import Car
Car.createTable()
FONT = ('Lotus', 16)
FONT_BOLD = ('Lotus', 16, 'bold')
root = None
statusVar = None

def brandChanged(brand):
    reload(brand,"None")


def modelChanged(brand,model):
    reload(brand,model)


def fetch():
    global statusVar
    statusVar.set("Processing...")
    try:
        r = Car.fetchFromSite()
        if r != 200:
            statusVar.set("Error code: "+str(r))
        reload()
    except Exception as e:
        statusVar.set(e)


def deleteAll():
    Car.deleteAll()
    reload()


def table(root, brand="None", model="None"):
    panel = tk.PanedWindow(root)
    panel.grid(row=1, column=0, columnspan=4, rowspan=2)

    treeView = ttk.Treeview(panel, selectmode='browse')
    style = ttk.Style()
    style.configure("Treeview.Heading", font=FONT_BOLD)
    style.configure("Treeview", font=FONT,rowheight=30)
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
        treeView.column(str(i), width=Car.TABLE_HEADERS_WEIGHTS[i-1]*70, anchor='se')
        treeView.heading(str(i), text=colHead)
        i+=1

    if brand=="None" and model=="None" :cars = Car.getAll()
    elif model=="None":cars = Car.getAllByBrand(brand)
    else: cars=Car.getAllByModel(brand, model)

    for row in cars:
        treeView.insert("", 'end', text="something",
                 values=row)


def reload(brand="None", model="None"):
    global root
    if root is not None:
        root.quit()
        root.destroy()

    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.resizable(width=1, height=1)

    brandVar = tk.StringVar(root)
    brandVar.set(brand)
    modelVar = tk.StringVar(root)
    modelVar.set(model)

    selectableBrands = ["None"]
    selectableBrands.extend(Car.getBrands())
    ov_brand = tk.OptionMenu(root, brandVar, *selectableBrands, command=brandChanged)
    ov_brand.grid(row=0, column=0)
    ov_brand.config(font=FONT)
    tk.Label(root, text="برند: ", font=FONT).grid(row=0, column=1)

    selectableModels=["None"]
    selectableModels.extend(Car.getBrandModels(brand))
    onChangeModel = lambda input:modelChanged(brandVar.get(),input)
    ov_model = tk.OptionMenu(root, modelVar, *selectableModels , command=onChangeModel)
    ov_model.grid(row=0, column=2)
    ov_model.config(font=FONT)
    tk.Label(root, text="مدل: ", font=FONT).grid(row=0, column=3)
    global statusVar
    statusVar = tk.StringVar(root)
    statusVar.set("OK")
    statusLabel = tk.Label(root, textvariable = statusVar, font=FONT)
    statusLabel.grid(row=0, column=4)
    tk.Button(root, text="بروزرسانی", command=fetch, font=FONT_BOLD).grid(row=1, column=4, sticky=tk.W)
    tk.Button(root, text="حذف همه", command=deleteAll, font=FONT_BOLD,bg='red',fg='white').grid(row=2, column=4, sticky=tk.W)
    table(root,brand,model)
    root.mainloop()

reload()