import tkinter as tk
from tkinter.messagebox import *

class APP:
    def __init__(self, master):
        frame = tk.Frame(master)
        frame.pack(side = tk.LEFT, padx = 10, pady = 10)

        self.hi_here = tk.Button(frame, text = "你好啊", fg = "black", bg = "white", command = self.say_hi)
        self.hi_here.pack()

    def say_hi(self):
        showinfo(message='hello')

        # 显示标签
        # var = tk.StringVar()
        # label = tk.Message( root, textvariable=var, relief=tk.RAISED )
        # var.set("Hey!? How are you doing?")
        # label.pack()

root = tk.Tk()
app = APP(root)

root.mainloop()