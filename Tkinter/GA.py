import tkinter as tk

def change_bg(*args):
    color = color_var.get()
    if color:
        root.config(bg=color.lower())

def reset_bg():
    root.config(bg="white")
    color_var.set('')  # Clear selection

root = tk.Tk()
root.title("Color Changer")
root.geometry("300x200")
root.config(bg="white")

tk.Label(root, text="Choose a color:").pack(pady=10)

color_var = tk.StringVar()
color_var.trace('w', change_bg)

colors = ["Red", "Green", "Blue", "Yellow"]
option_menu = tk.OptionMenu(root, color_var, *colors)
option_menu.pack(pady=10)

reset_btn = tk.Button(root, text="Reset", command=reset_bg)
reset_btn.pack(pady=20)

root.mainloop()