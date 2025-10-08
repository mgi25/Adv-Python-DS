import tkinter as tk

def add():
    a = float(entry1.get())
    b = float(entry2.get())
    result.config(text="Result: " + str(a + b))

def subtract():
    a = float(entry1.get())
    b = float(entry2.get())
    result.config(text="Result: " + str(a - b))

def multiply():
    a = float(entry1.get())
    b = float(entry2.get())
    result.config(text="Result: " + str(a * b))

def divide():
    a = float(entry1.get())
    b = float(entry2.get())
    result.config(text="Result: " + str(a / b))

root = tk.Tk()
root.title("Simple Calculator")

entry1 = tk.Entry(root)
entry2 = tk.Entry(root)
entry1.pack()
entry2.pack()

tk.Button(root, text="+", command=add).pack()
tk.Button(root, text="-", command=subtract).pack()
tk.Button(root, text="×", command=multiply).pack()
tk.Button(root, text="÷", command=divide).pack()

result = tk.Label(root, text="Result:")
result.pack()

root.mainloop()
