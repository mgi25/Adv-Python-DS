# Load the same image in opencv and prirnt its dimentions (height,width,channels)
# convert the opencv image to grayscale and save it.
# diisplay the original and grayscale images side by side using matplotlib
# write a program to resize an image in opencv to half its original size.
# compare the file size of an image saved as jpeg vs png. Which one is smaller?why?

# OpenCV tasks: load, print dims, grayscale, show, resize, and JPEG vs PNG size
import cv2
import os
from matplotlib import pyplot as plt

IMAGE_PATH = r"media/Screenshot 2025-03-17 141503.png"   

# 1) Load with OpenCV and print dimensions (H, W, C)
img = cv2.imread(IMAGE_PATH)               
h, w = img.shape[:2]
c = 1 if img.ndim == 2 else img.shape[2]
print("OpenCV image shape -> Height:", h, "Width:", w, "Channels:", c)

# 2) Convert to grayscale and save
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imwrite("opencv_gray.png", gray)

# 3) Display original and grayscale side by side (Matplotlib expects RGB)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

plt.figure(figsize=(8,3))
plt.subplot(1,2,1); plt.title("Original"); plt.imshow(img_rgb); plt.axis("off")
plt.subplot(1,2,2); plt.title("Grayscale"); plt.imshow(gray, cmap="gray"); plt.axis("off")
plt.tight_layout()
plt.show()

# 4) Resize to half of the original size and save
half = cv2.resize(img, (w//2, h//2), interpolation=cv2.INTER_AREA)
cv2.imwrite("opencv_half.png", half)

# 5) Compare file size: save as JPEG vs PNG (same image content)
cv2.imwrite("compare.jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 95])  # lossy
cv2.imwrite("compare.png", img)                                   # lossless

size_jpg = os.path.getsize("compare.jpg")
size_png = os.path.getsize("compare.png")
print("JPEG size (bytes):", size_jpg)
print("PNG  size (bytes):", size_png)

if size_jpg < size_png:
    print("Result: JPEG is smaller for this image.")
elif size_png < size_jpg:
    print("Result: PNG is smaller for this image.")
else:
    print("Result: both are the same size.")
