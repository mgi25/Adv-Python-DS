# write an python program using pillow library to 
# 1) load an image file using pillow and print format,size,mode
# 2) Resize an image to 200 x 200 usig OpenV & pillow
# 3) Convert a color image to grayscale and save
# 4) apply BLUR and SHARPEN filters using pillow
# 5) Display original and processed images side by side

from PIL import Image, ImageFilter
import cv2
from matplotlib import pyplot as plt

# 1) Load image using Pillow
img = Image.open("media/Screenshot 2025-03-17 141503.png")
print("Format:", img.format)
print("Size:", img.size)
print("Mode:", img.mode)

# 2) Resize to 200x200 (OpenCV & Pillow)
# Using Pillow
img_pillow_resized = img.resize((200, 200))
# Using OpenCV
cv_img = cv2.imread("media/Screenshot 2025-03-17 141503.png")
cv_img_resized = cv2.resize(cv_img, (200, 200))

# 3) Convert to grayscale and save
gray_img = img.convert("L")
gray_img.save("gray_output.png")

# 4) Apply Blur & Sharpen
blur_img = img.filter(ImageFilter.BLUR)
sharp_img = img.filter(ImageFilter.SHARPEN)

# 5) Display original and processed images side by side
plt.subplot(1, 4, 1)
plt.title("Original")
plt.imshow(img)
plt.axis("off")

plt.subplot(1, 4, 2)
plt.title("Gray")
plt.imshow(gray_img, cmap="gray")
plt.axis("off")

plt.subplot(1, 4, 3)
plt.title("Blur")
plt.imshow(blur_img)
plt.axis("off")

plt.subplot(1, 4, 4)
plt.title("Sharpen")
plt.imshow(sharp_img)
plt.axis("off")

plt.show()


