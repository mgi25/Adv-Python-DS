import tkinter as tk
root = tk.Tk()
root.title("Welcome Window !!!")
label = tk.Label(root, text="Hello MGI!")
label.pack()
tk.Button(root, text="Close", command=root.destroy).pack()
# add a space for user name to enter name and submit button
entry = tk.Entry(root)
entry.pack()
tk.Button(root, text="Submit", command=lambda: print(entry.get())).pack()   
root.mainloop()