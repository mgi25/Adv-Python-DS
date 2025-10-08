import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageFilter

def open_image():
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff")])
    if file_path:
        try:
            global img, img_display
            img = Image.open(file_path)
            show_image(img)
        except Exception as e:
            messagebox.showerror("Error", f"Cannot open image: {e}")

def show_image(pil_img):
    # Resize for display if too large
    display_img = pil_img.copy()
    display_img.thumbnail((200, 200))
    global img_display
    img_display = ImageTk.PhotoImage(display_img)
    image_label.config(image=img_display)
    image_label.image = img_display

def to_grayscale():
    if img:
        gray = img.convert('L')
        show_image(gray)

def resize_200():
    if img:
        resized = img.resize((200, 200))
        show_image(resized)

def blur_image():
    if img:
        # Increase radius for stronger blur
        blurred = img.filter(ImageFilter.GaussianBlur(radius=5))
        show_image(blurred)
# --- Main Window ---
root = tk.Tk()
root.title("Simple Photo Editor")
root.geometry("400x450")

img = None
img_display = None

open_btn = tk.Button(root, text="Open Image", command=open_image)
open_btn.pack(pady=10)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

gray_btn = tk.Button(btn_frame, text="Grayscale", command=to_grayscale)
gray_btn.grid(row=0, column=0, padx=5)

resize_btn = tk.Button(btn_frame, text="Resize 200x200", command=resize_200)
resize_btn.grid(row=0, column=1, padx=5)

blur_btn = tk.Button(btn_frame, text="Blur", command=blur_image)
blur_btn.grid(row=0, column=2, padx=5)

image_label = tk.Label(root)
image_label.pack(pady=10)

root.mainloop()