from tkinter import *
from tkinter.ttk import *
from lid_nid_gui import LidNidMapperGUI

import os
import time

# PROCESS SETTINGS
#-------------------------------------------------------------------------------------------------
# Calculate process time
start = time.time()
nielsen_insights_path = 'Nielsen Insights/'

# create directory for output file
os.makedirs(nielsen_insights_path, exist_ok=True)

root = Tk()

lid_nid_gui = LidNidMapperGUI(root)
root.config(menu=lid_nid_gui.menubar)
root.mainloop()

# Stop timer of the process and print how long it took to run
end = time.time()
elpased_time = end - start
m, s = divmod(elpased_time, 60)
h, m = divmod(m, 60)
print("\nThe process ran in: {}hour(s), {}minutes(s) and {}second(s)".format(int(h),int(m),round(s,3)))