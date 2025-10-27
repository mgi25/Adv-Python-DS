# Q3. Combine OpenCV and Pillow in a single program to:
# • Read an image using OpenCV and display it.
# • Convert the same image to grayscale using Pillow.
# • Compare both image formats (OpenCV and PIL).

import cv2
from PIL import Image
from tkinter import Tk, filedialog
import numpy as np
import os

# Hide Tkinter main window
root = Tk()
root.withdraw()

print("📂 Please select an image file...")
file_path = filedialog.askopenfilename(
    title="Select an Image",
    filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.tiff *.webp")]
)

if not file_path:
    print("❌ No file selected. Exiting program.")
    exit()

print(f"✅ Selected file: {file_path}")

# ----------------------------------------------------------------
# 1️⃣ Read and display the image using OpenCV
# ----------------------------------------------------------------
img_cv = cv2.imread(file_path)
if img_cv is None:
    print("❌ Error: Unable to read image.")
    exit()

cv2.imshow("OpenCV Image (BGR)", img_cv)
cv2.waitKey(1000)  # show for 1 second
cv2.destroyAllWindows()

# ----------------------------------------------------------------
# 2️⃣ Convert the same image to grayscale using Pillow
# ----------------------------------------------------------------
# Load image with Pillow
img_pil = Image.open(file_path)
gray_pil = img_pil.convert("L")  # convert to grayscale
gray_pil.show(title="Pillow Grayscale")  # open in default viewer

# ----------------------------------------------------------------
# 3️⃣ Compare both formats
# ----------------------------------------------------------------
print("\n=== Comparison of OpenCV vs Pillow ===")
print("📘 OpenCV format:")
print(f"   - Type: {type(img_cv)}")
print(f"   - Shape: {img_cv.shape}")
print(f"   - Color order: BGR (Blue, Green, Red)")

print("\n📙 Pillow format:")
print(f"   - Type: {type(img_pil)}")
print(f"   - Mode before grayscale: {img_pil.mode}")
print(f"   - Mode after grayscale: {gray_pil.mode}")
print(f"   - Size: {img_pil.size}")
print("======================================")

# ----------------------------------------------------------------
# 4️⃣ Save Pillow grayscale result in assignment folder
# ----------------------------------------------------------------
save_folder = r"C:\Users\mgial\OneDrive\Documents\Adv Python sem 5\calss 1\assignments\oct_22"
os.makedirs(save_folder, exist_ok=True)
save_path = os.path.join(save_folder, "result_q3_pillow_gray.jpg")
gray_pil.save(save_path)
print(f"💾 Grayscale image saved as: {save_path}")
