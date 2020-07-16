from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

class LidNidMapperGUI:
    def __init__(self, master, *args, **kwargs):
        self.master = master
        master.title("LID to NID Mapping Tool")

        # options for campaign type dropdown menu
        OPTIONS = [
        "campaign_id",
        "order_id",
        "ad_id",
        "zone_id"
        ] 

        # create dropdown menu for campaign type
        self.variable = StringVar(master)
        self.variable.set(OPTIONS[0]) # default value for dropdown mmenu
        self.menu_window = OptionMenu(master, variable, OPTIONS[0], *OPTIONS)
        self.menu_window.grid(row=1, column=1, sticky=W+E)

        # menu bar
        self.menubar = Menu(master)
        self.filemenu = Menu(master, tearoff=0)
        self.filemenu.add_command(label="New", command=donothing)
        self.filemenu.add_command(label="Open", command=donothing)
        self.filemenu.add_command(label="Save", command=donothing)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=window.quit)
        self.menubar.add_cascade(label="File", menu=filemenu)

        # create text box labels
        self.client_label = Label(master, text="Client Name")
        self.client_label.grid(row=0, column=0, sticky=W)
        

        # functions for gui app
        def donothing():
            return 
