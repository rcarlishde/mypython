#TEST
"""
# Python 3.x
import tkinter as tk
import tkinter.font as tkfont

root = tk.Tk()
root.title("All fonts")
scroller = tk.Scrollbar(root)
listbox = tk.Listbox(root,yscrollcommand=scroller.set)
listbox.pack(side=tk.LEFT)
scroller.config(command=listbox.yview)
scroller.pack(side=tk.LEFT,fill=tk.Y)
for font in sorted(tkfont.families()):
    listbox.insert("end",font)
root.mainloop()

"""


import tkinter as tk
import tkinter.ttk as ttk

r = tk.Tk()

def callback():
    r2 = tk.Toplevel()

    c2 = ttk.Combobox(r2, style='ARD.TCombobox')
    c2.pack()

b = tk.Button(r, text = 'Open', command = callback)
b.pack()

combostyle = ttk.Style()
combostyle.configure('ARD.TCombobox', background="#ffcc66", fieldbackground="#ffff99")

c = ttk.Combobox(style='ARD.TCombobox')
c.pack()

r.mainloop()