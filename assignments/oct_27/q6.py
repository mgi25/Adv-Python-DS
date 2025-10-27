# Q6. Create a simple Tkinter Text Editor that:
# • Lets the user type text inside a textbox.
# • Saves the text to a .txt file.
# • Includes ‘Save’ and ‘Exit’ buttons.


import tkinter as tk
from tkinter import filedialog, messagebox

# -------------------- Functions --------------------
def save_text():
    text_data = text_box.get("1.0", tk.END).strip()
    if not text_data:
        messagebox.showinfo("Empty", "There is no text to save.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")],
        title="Save As"
    )
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text_data)
        messagebox.showinfo("Saved", f"✅ File saved successfully:\n{file_path}")

def exit_app():
    confirm = messagebox.askyesno("Exit", "Are you sure you want to exit?")
    if confirm:
        root.destroy()

# -------------------- Window Setup --------------------
root = tk.Tk()
root.title("Simple Text Editor")
root.geometry("700x500")
root.minsize(500, 400)

# -------------------- Text Box --------------------
text_box = tk.Text(root, wrap="word", font=("Consolas", 12), undo=True)
text_box.pack(expand=True, fill="both", padx=10, pady=(10, 0))

# -------------------- Button Frame --------------------
button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.pack(fill="x", pady=10)

save_button = tk.Button(button_frame, text="💾 Save", width=12, bg="#4CAF50", fg="white", command=save_text)
save_button.pack(side="left", padx=20, pady=5)

exit_button = tk.Button(button_frame, text="❌ Exit", width=12, bg="#f44336", fg="white", command=exit_app)
exit_button.pack(side="right", padx=20, pady=5)

# -------------------- Start App --------------------
root.mainloop()
