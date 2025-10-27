# Q1. Write a Python program using Pillow (PIL) to:
# • Load an image.
# • Convert it to grayscale.
# • Rotate it by 45° and resize it to 300×300.
# • Save the final output as ‘result_pillow.jpg’.

from PIL import Image
from tkinter import Tk, filedialog
import os

# Hide the Tkinter root window
root = Tk()
root.withdraw()

print("📂 Please select an image file...")
file_path = filedialog.askopenfilename(
    title="Select an Image",
    filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.tiff *.webp")]
)

if not file_path:
    print("❌ No file selected. Exiting program.")
else:
    print(f"✅ Selected file: {file_path}")

    # Step 1: Load image
    img = Image.open(file_path)
    print("✅ Image loaded successfully!")

    # Step 2: Convert to grayscale
    gray_img = img.convert("L")
    print("✅ Converted to grayscale.")

    # Step 3: Rotate by 45 degrees
    rotated_img = gray_img.rotate(45, expand=True)
    print("✅ Rotated by 45°.")

    # Step 4: Resize to 300×300 pixels
    final_img = rotated_img.resize((300, 300))
    print("✅ Resized to 300×300.")

    # Step 5: Save output as 'result_pillow.jpg' in your assignment folder
    save_folder = r"C:\Users\mgial\OneDrive\Documents\Adv Python sem 5\calss 1\assignments\oct_22"
    os.makedirs(save_folder, exist_ok=True)
    save_path = os.path.join(save_folder, "result_pillow.jpg")

    final_img.save(save_path)
    print(f"🎉 Done! Saved as {save_path}")

    # Optional: Open the image automatically
    final_img.show()
