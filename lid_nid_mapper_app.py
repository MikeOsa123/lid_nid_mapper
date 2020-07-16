from tkinter import *
from tkinter.ttk import *
from lid_nid_gui_app import LidNidMapperGUI

root = Tk()

lid_nid_gui = LidNidMapperGUI(root)
root.config(menu=lid_nid_gui.menubar)
root.mainloop()