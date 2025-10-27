# Q5. Develop a Tkinter GUI that:
# • Allows users to enter their name and age.
# • Displays a greeting message when a button is clicked.
# • Includes a ‘Clear’ button to reset the inputs.


import tkinter as tk
from tkinter import messagebox

def say_hello():
    name = entry_name.get().strip()
    age = entry_age.get().strip()

    if name == "" or age == "":
        messagebox.showwarning("Missing Info", "Please enter both name and age.")
        return

    # Show greeting message
    greeting = f"Hello {name}, you are {age} years old!"
    label_result.config(text=greeting)

def clear_all():
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    label_result.config(text="")  # clear result label too

# Create main window
root = tk.Tk()
root.title("Greeting App")

# ---------- Name input ----------
label_name = tk.Label(root, text="Name:")
label_name.grid(row=0, column=0, padx=10, pady=10, sticky="e")

entry_name = tk.Entry(root, width=30)
entry_name.grid(row=0, column=1, padx=10, pady=10)

# ---------- Age input ----------
label_age = tk.Label(root, text="Age:")
label_age.grid(row=1, column=0, padx=10, pady=10, sticky="e")

entry_age = tk.Entry(root, width=30)
entry_age.grid(row=1, column=1, padx=10, pady=10)

# ---------- Buttons ----------
button_greet = tk.Button(root, text="Greet", command=say_hello)
button_greet.grid(row=2, column=0, padx=10, pady=10)

button_clear = tk.Button(root, text="Clear", command=clear_all)
button_clear.grid(row=2, column=1, padx=10, pady=10, sticky="w")

# ---------- Result label ----------
label_result = tk.Label(root, text="", fg="blue", font=("Arial", 12, "bold"))
label_result.grid(row=3, column=0, columnspan=2, padx=10, pady=20)

# Start the app
root.mainloop()
