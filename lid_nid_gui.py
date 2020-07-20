from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

from lid_nid_helper_functions import count_element, query_audience, nielsen_insights
from snowflake_utility import SnowflakeApi
from lid_nid_config import snowflake

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

        # options for query audience type dropdown menu
        AUDIENCEOPTIONS = [
        "exposed users",
        "matched users",
        "clientsite users"
        ] 

        # create dropdown menu for campaign type
        self.variable = StringVar(master)
        self.variable.set(OPTIONS[0]) # default value for dropdown mmenu
        self.menu_window = OptionMenu(master, self.variable, OPTIONS[0],*OPTIONS)
        self.menu_window.grid(row=1, column=1, columnspan=2, sticky=W+E)

        # create dropdown menu for query audience type
        self.audience_variable = StringVar(master)
        self.audience_variable.set(AUDIENCEOPTIONS[0]) # default value for dropdown mmenu
        self.audience_menu_window = OptionMenu(master, self.audience_variable, AUDIENCEOPTIONS[0], *AUDIENCEOPTIONS)
        self.audience_menu_window.grid(row=2, column=1, columnspan=2, sticky=W+E)

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
        self.audience_dropdown_label = Label(master, text="Audience Type")
        self.audience_dropdown_label.grid(row=2, column=0, sticky=W)         
        self.campaign_id_label = Label(master, text="Campaign ID")
        self.campaign_id_label.grid(row=3, column=0, sticky=W)
        self.campaign_dates_label = Label(master, text="Campaign Dates")
        self.campaign_dates_label.grid(row=4, column=0, sticky=W)

        # create entry box
        self.client_entry = Entry(master, width=50)
        self.client_entry.grid(row=0, column=1, columnspan=2, sticky=W+E)
        self.client_entry.insert(0, "Please enter the Client name: ")

        self.campaign_id_entry = Entry(master, width=50)
        self.campaign_id_entry.grid(row=3, column=1, columnspan=2, sticky=W+E)
        self.campaign_id_entry.insert(0, "Please provide list of numbers separated by comma, e.g. 1,2,3: ")

        self.campaign_from_dt_entry = Entry(master, width=50)
        self.campaign_from_dt_entry.grid(row=4, column=1, sticky=W+E)
        self.campaign_from_dt_entry.insert(0, "Please provide from Date, e.g. 2020-07-01: ")

        self.campaign_to_dt_entry = Entry(master, width=50)
        self.campaign_to_dt_entry.grid(row=4, column=2, sticky=W+E)
        self.campaign_to_dt_entry.insert(0, "Please provide To Date, e.g. 2020-07-31: ")
        
        # functions for gui app
        def donothing():
            return 

        # clear entry box
        def clear_textbox(event):
            event.widget.delete(0, END)
            return None

        # create buttons
        self.submit_btn = Button(master, text="Submit Query", width=10, command=lambda: clicked())
        self.submit_btn.grid(row=5, column=0, columnspan=3,  padx=10, pady=5, sticky=N+S+E+W)
        self.query_btn = Button(master, text="Run Query", width=10, command=lambda: run_query())
        self.query_btn.grid(row=6, column=0, columnspan=3, padx=10, pady=5, sticky=N+S+E+W)

        # event handlers
        self.client_entry.bind("<Button-1>", clear_textbox)
        self.campaign_id_entry.bind("<Button-1>", clear_textbox)
        self.campaign_from_dt_entry.bind("<Button-1>", clear_textbox)
        self.campaign_to_dt_entry.bind("<Button-1>", clear_textbox)

        # Button Functions
        #-------------------------------------------------------------------------------------------------  

        def clicked():

            # disable submit button upon being clicked
            self.submit_btn["state"] = DISABLED

            # set query variables
            self.client_name = self.client_entry.get().lower()
            self.campaign_id = tuple(map(str, self.campaign_id_entry.get().replace(' ','').split(',')))
            self.campaign_type = self.variable.get()
            self.audience_type = self.audience_variable.get()
            self.campaign_from_dt = self.campaign_from_dt_entry.get()
            self.campaign_to_dt = self.campaign_to_dt_entry.get()

            self.campaign_details = {
                "client_name": self.client_name,
                "campaign_id": self.campaign_id,
                "campaign_type": self.campaign_type,
                "campaign_from_dt": self.campaign_from_dt,
                "campaign_to_dt": self.campaign_to_dt,
                "audience_type": self.audience_type,
                }

            # enable run query button
            self.query_btn["state"] = NORMAL

        def run_query():
            
            # disable button
            self.query_btn["state"] = DISABLED

            # enable submit button
            self.submit_btn["state"] = NORMAL

            # create snowflake object that
            self.snow_obj = SnowflakeApi(**snowflake)

            # establish query to be used for specified audience
            self.queries = query_audience(**self.campaign_details)

            # execute each query in the list provided based on campaign details
            for query in self.queries:
                try:
                    self.snow_obj.return_nitems(query, 1)
                except Exception as e:
                    print(e)
                    print("Query did not run!")

            
            self.dataframe_query = '''
            select * from matched_xd_nielsen_data_view LIMIT 10000
            '''
            try:
                self.data = self.snow_obj.return_all(self.dataframe_query)
            except Exception as e:
                print(e)

            # provide nielsen insights 
            nielsen_insights(self.data, 'Nielsen Insights/', self.campaign_details["client_name"])

            # delete previous query info
            # del campaign_id, campaign_type, client_name

            return messagebox.showinfo("Success!!!", "Query has run")

