# Q2. Using OpenCV, perform the following operations on an image:
# • Display original, blurred, and edge-detected (Canny) versions side by side.
# • Print the image size, color channels, and file format.


import cv2
import numpy as np
from tkinter import Tk, filedialog
import os

# Hide Tkinter root window
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
else:
    print(f"✅ Selected file: {file_path}")

# 1. Load the image
img = cv2.imread(file_path)
if img is None:
    print("❌ Could not read the image. Exiting.")
    exit()

# 2. Get and print image details
height, width, channels = img.shape
file_format = os.path.splitext(file_path)[1]
print("\n=== Image Info ===")
print(f"📏 Image Size      : {width} x {height}")
print(f"🎨 Color Channels  : {channels}")
print(f"🗂️ File Format     : {file_format}")
print("==================\n")

# 3. Apply filters
blurred = cv2.GaussianBlur(img, (9, 9), 0)
edges = cv2.Canny(img, 100, 200)

# 4. Convert edges to color (3 channels)
edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

# 5. Resize all to the same dimensions
fixed_width = 400
fixed_height = 300
img_resized = cv2.resize(img, (fixed_width, fixed_height))
blurred_resized = cv2.resize(blurred, (fixed_width, fixed_height))
edges_resized = cv2.resize(edges_colored, (fixed_width, fixed_height))

# 6. Add text labels for clarity
cv2.putText(img_resized, "Original", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
cv2.putText(blurred_resized, "Blurred", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
cv2.putText(edges_resized, "Edges", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

# 7. Combine all three horizontally
combined = np.hstack((img_resized, blurred_resized, edges_resized))

# 8. Display neatly aligned result
cv2.imshow("Original | Blurred | Edges", combined)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 9. Save the combined image in your assignment folder
save_folder = r"C:\Users\mgial\OneDrive\Documents\Adv Python sem 5\calss 1\assignments\oct_22"
os.makedirs(save_folder, exist_ok=True)
save_path = os.path.join(save_folder, "result_opencv.jpg")
cv2.imwrite(save_path, combined)

print(f"💾 Saved combined output as: {save_path}")
