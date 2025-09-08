# 1) open an image and rotate it by 45 degrees
# 2) write a program to convert a color  image to black & white (binary)
# 3) take an image and flip it horizontaly and verticaly
# 4) crop the center portion of an image and save it as a new File
# 5) load an image and draw a rectanglr, circle, and line on it
# 6) convert an image into HSV color space and display it.
# 7) apply Gaussian blur and compare it with the original.
# 8) use the canny edge Dectator to Highlight edges.
# simple_imaging_tasks.py
# simple_imaging_tasks.py
import cv2
import os

# make a folder to save all outputs
outdir = "q5/outputs"
os.makedirs(outdir, exist_ok=True)

# load an image
img = cv2.imread("media/Screenshot 2025-03-17 141503.png")
if img is None:
    print("Image not found!")
    exit()

h, w = img.shape[:2]

# 1) Rotate image by 45 degrees
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, 45, 1)
rotated = cv2.warpAffine(img, M, (w, h))
cv2.imwrite(f"{outdir}/rotated_45.jpg", rotated)

# 2) Convert to black & white (binary)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
cv2.imwrite(f"{outdir}/binary.jpg", binary)

# 3) Flip horizontally and vertically
flip_h = cv2.flip(img, 1)
flip_v = cv2.flip(img, 0)
cv2.imwrite(f"{outdir}/flip_horizontal.jpg", flip_h)
cv2.imwrite(f"{outdir}/flip_vertical.jpg", flip_v)

# 4) Crop center portion (middle half)
y1, y2 = h // 4, 3 * h // 4
x1, x2 = w // 4, 3 * w // 4
crop = img[y1:y2, x1:x2]
cv2.imwrite(f"{outdir}/center_crop.jpg", crop)

# 5) Draw rectangle, circle, line
draw = img.copy()
cv2.rectangle(draw, (50, 50), (200, 200), (0, 255, 0), 2)
cv2.circle(draw, (w // 2, h // 2), 50, (255, 0, 0), 2)
cv2.line(draw, (0, h - 1), (w - 1, 0), (0, 0, 255), 2)
cv2.imwrite(f"{outdir}/shapes.jpg", draw)

# 6) Convert to HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
cv2.imwrite(f"{outdir}/hsv.jpg", hsv)

# 7) Gaussian blur
blur = cv2.GaussianBlur(img, (7, 7), 0)
cv2.imwrite(f"{outdir}/blurred.jpg", blur)

# 8) Canny edge detector
edges = cv2.Canny(gray, 100, 200)
cv2.imwrite(f"{outdir}/edges.jpg", edges)

print("All tasks completed! Images saved inside 'outputs/' folder.")
