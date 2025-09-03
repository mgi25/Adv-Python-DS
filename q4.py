# 1. Write a Python program using Pillow to load an image and print its
# format, size, and mode.
# 2. Convert a color image to grayscale using Pillow and save it as
# gray_image.jpg.
# 3. Resize an image to 300×300 pixels and then rotate it by 45°. Save both
# outputs separately.
# 4. Apply BLUR and SHARPEN filters on an image using Pillow and
# display the results.
# 5. Write a program to read an image with OpenCV and print its height,
# width, and number of channels.
# 6. Convert an image into grayscale using OpenCV and save it as
# output_gray.jpg.
# 7. Read an image using OpenCV and use Matplotlib to display the original
# image and grayscale image side by side.
# 8. Resize an image to half its original size. Then, crop a 100×100 region
# from the center of the image and display it.
# 9. Apply the following filters to an image in OpenCV:
# Gaussian Blur
# Edge Detection (Canny)
# Display the results.
# 10. Write a program to:
# Read all images from a folder,
# Convert them into grayscale,
# Resize them to 200×200 pixels,
# Save them into a new folder called processed_images/.

# imaging_tasks.py
# Requires: Pillow, opencv-python, matplotlib
# pip install pillow opencv-python matplotlib

# pillow_simple.py
# pip install pillow

from PIL import Image, ImageFilter

# ---- change this to your file ----
IMAGE_PATH = "media/Screenshot 2025-03-17 141503.png"

# 1) Load and print info
img = Image.open(IMAGE_PATH)
print("[1] Format:", img.format)
print("[1] Size (W,H):", img.size)
print("[1] Mode:", img.mode)

# 2) Color -> Grayscale (save as JPG)
gray = img.convert("L")
gray.save("gray_image.jpg")
print("[2] Saved gray_image.jpg")

# 3) Resize to 300x300 and Rotate 45°
#    If image has alpha, save as PNG to keep it simple.
resized = img.resize((300, 300))
resized.save("resized_300x300.png")
rotated = img.rotate(45, expand=True)
rotated.save("rotated_45.png")
print("[3] Saved resized_300x300.png and rotated_45.png")

# 4) Apply BLUR and SHARPEN and display
blurred = img.filter(ImageFilter.BLUR)
sharpened = img.filter(ImageFilter.SHARPEN)
blurred.show(title="BLUR")     # opens viewer
sharpened.show(title="SHARPEN")
blurred.save("pil_blur.png")
sharpened.save("pil_sharpen.png")
print("[4] Saved pil_blur.png and pil_sharpen.png")


# opencv_simple.py
# pip install opencv-python matplotlib

import cv2
import matplotlib.pyplot as plt
import os
from pathlib import Path

# ---- change these ----
IMAGE_PATH = "media/Screenshot 2025-03-17 141503.png"
INPUT_FOLDER = "media"
OUTPUT_FOLDER = "processed_images"

# Read once
img = cv2.imread(IMAGE_PATH)
if img is None:
    raise FileNotFoundError(f"Cannot read {IMAGE_PATH}")

# 5) Print height, width, channels
h, w = img.shape[:2]
ch = 1 if img.ndim == 2 else img.shape[2]
print("[5] Width:", w, "Height:", h, "Channels:", ch)

# 6) Convert to grayscale and save
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imwrite("output_gray.jpg", gray)
print("[6] Saved output_gray.jpg")

# 7) Show original + gray side by side (Matplotlib needs RGB)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
plt.figure(figsize=(8,4))
plt.subplot(1,2,1); plt.imshow(img_rgb); plt.title("Original"); plt.axis("off")
plt.subplot(1,2,2); plt.imshow(gray, cmap="gray"); plt.title("Grayscale"); plt.axis("off")
plt.tight_layout(); plt.show()

# 8) Half-size, then center crop 100x100 and display
half = cv2.resize(img, (w//2, h//2))
cv2.imwrite("opencv_half.jpg", half)
hh, hw = half.shape[:2]
cy, cx = hh//2, hw//2
crop = half[cy-50:cy+50, cx-50:cx+50]  # 100x100
cv2.imwrite("opencv_center_crop_100x100.jpg", crop)
plt.figure(figsize=(3,3))
plt.imshow(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)); plt.title("Center 100x100"); plt.axis("off")
plt.show()
print("[8] Saved opencv_half.jpg and opencv_center_crop_100x100.jpg")

# 9) Gaussian Blur + Canny edges and display
gauss = cv2.GaussianBlur(img, (5,5), 1.2)
edges = cv2.Canny(gray, 100, 200)
plt.figure(figsize=(12,4))
plt.subplot(1,3,1); plt.imshow(img_rgb); plt.title("Original"); plt.axis("off")
plt.subplot(1,3,2); plt.imshow(cv2.cvtColor(gauss, cv2.COLOR_BGR2RGB)); plt.title("Gaussian Blur"); plt.axis("off")
plt.subplot(1,3,3); plt.imshow(edges, cmap="gray"); plt.title("Canny Edges"); plt.axis("off")
plt.tight_layout(); plt.show()

# 10) Batch: read all images in a folder, gray + resize(200x200), save
Path(OUTPUT_FOLDER).mkdir(exist_ok=True)
exts = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}
count = 0
for name in os.listdir(INPUT_FOLDER):
    p = Path(INPUT_FOLDER) / name
    if p.suffix.lower() not in exts:
        continue
    im = cv2.imread(str(p))
    if im is None:
        continue
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    r = cv2.resize(g, (200, 200))
    out = Path(OUTPUT_FOLDER) / f"{p.stem}_gray_200x200.jpg"
    cv2.imwrite(str(out), r)
    count += 1
print(f"[10] Processed {count} images → {OUTPUT_FOLDER}/")
