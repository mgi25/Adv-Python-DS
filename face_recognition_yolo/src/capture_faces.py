import cv2
import os

PERSON_NAME = "alen"          # change each time
SAVE_DIR = f"../dataset_faces/train/{PERSON_NAME}"  # or val/ for validation
NUM_IMAGES = 60

os.makedirs(SAVE_DIR, exist_ok=True)

cap = cv2.VideoCapture(0)
count = 0

print("Press 'c' to capture, 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Capture Faces", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("c"):
        path = os.path.join(SAVE_DIR, f"{PERSON_NAME}_{count:03d}.jpg")
        cv2.imwrite(path, frame)
        print("Saved:", path)
        count += 1
        if count >= NUM_IMAGES:
            print("Done.")
            break
    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
