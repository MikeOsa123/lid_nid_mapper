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
        self.menu_window = OptionMenu(master, self.variable, OPTIONS[0], *OPTIONS)
        self.menu_window.grid(row=1, column=1, sticky=W+E)

        # menu bar
        self.menubar = Menu(master)
        self.filemenu = Menu(master, tearoff=0)
        self.filemenu.add_command(label="New", command=lambda: donothing())
        self.filemenu.add_command(label="Open", command=lambda: donothing())
        self.filemenu.add_command(label="Save", command=lambda: donothing())
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=master.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        # create text box labels
        self.client_label = Label(master, text="Client Name")
        self.client_label.grid(row=0, column=0, sticky=W)
        self.dropdown_label = Label(master, text="Campaign Type")
        self.dropdown_label.grid(row=1, column=0, sticky=W)      
        self.campaign_id_label = Label(master, text="Campaign ID")
        self.campaign_id_label.grid(row=2, column=0, sticky=W)

        # create entry box
        self.client_entry = Entry(master, width=50)
        self.client_entry.grid(row=0, column=1, sticky=W+E)
        self.client_entry.insert(0, "Please enter the Client name: ")

        self.campaign_id_entry = Entry(master, width=50)
        self.campaign_id_entry.grid(row=2, column=1, sticky=W+E)
        self.campaign_id_entry.insert(0, "Please provide list of numbers separated by comma, e.g. 1,2,3: ")
        
        # functions for gui app
        def donothing():
            return 

        # clear entry box
        def clear_textbox(event):
            event.widget.delete(0, END)
            return None

        # create buttons
        self.submit_btn = Button(master, text="Submit Query", width=10, command=lambda: clicked())
        self.submit_btn.grid(row=3, column=0, columnspan=2,  padx=10, pady=5, sticky=N+S+E+W)
        self.query_btn = Button(master, text="Run Query", width=10, command=lambda: run_query(function) )
        self.query_btn.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky=N+S+E+W)

        # event handlers
        self.client_entry.bind("<Button-1>", clear_textbox)
        self.campaign_id_entry.bind("<Button-1>", clear_textbox)

        # Button Functions
        #-------------------------------------------------------------------------------------------------  

        def clicked():

            # disable submit button upon being clicked
            self.submit_btn["state"] = DISABLED

            # set query variables
            self.client_name = self.client_entry.get().lower()
            self.campaign_id = tuple(map(str, self.campaign_id_entry.get().split(',')))
            self.campaign_type = self.variable.get()

            # enable run query button
            self.query_btn["state"] = NORMAL

        def run_query(function):
            return


root = Tk()

lid_nid_gui = LidNidMapperGUI(root)
root.config(menu=lid_nid_gui.menubar)
root.mainloop()