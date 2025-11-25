import os
import json
from datetime import datetime

import cv2
import numpy as np
import tensorflow as tf

# -------------------------------------------------
# PATHS (relative to project root)
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # face_recognition_yolo/

MODELS_DIR = os.path.join(BASE_DIR, "models")
LOG_DIR = os.path.join(BASE_DIR, "logs", "unknown_faces")
SCREENSHOT_DIR = os.path.join(BASE_DIR, "screenshots")

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

MODEL_PATH = os.path.join(MODELS_DIR, "face_cnn_mobilenetv2.h5")
CLASS_INDICES_PATH = os.path.join(MODELS_DIR, "class_indices.json")

# -------------------------------------------------
# MODEL / DETECTOR SETTINGS
# -------------------------------------------------
IMG_SIZE = 160
UNKNOWN_THRESHOLD = 0.7  # below this prob => Unknown

# OpenCV built-in Haar cascade (comes with opencv-python)
HAAR_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(HAAR_PATH)

# -------------------------------------------------
# LOAD CNN MODEL + CLASS MAPPING
# -------------------------------------------------
print("[INFO] Loading CNN face recognition model...")
cnn_model = tf.keras.models.load_model(MODEL_PATH)

with open(CLASS_INDICES_PATH, "r") as f:
    class_indices = json.load(f)

idx2class = {v: k for k, v in class_indices.items()}
print("[INFO] Known classes:", idx2class)


# -------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------
def preprocess_face(face_img):
    """Resize and normalize cropped face for CNN."""
    face_resized = cv2.resize(face_img, (IMG_SIZE, IMG_SIZE))
    face_resized = face_resized.astype("float32") / 255.0
    face_resized = np.expand_dims(face_resized, axis=0)  # (1, H, W, 3)
    return face_resized


def predict_identity(face_img):
    """
    Return (label, confidence) where label is a person name or 'Unknown'.
    """
    inp = preprocess_face(face_img)
    preds = cnn_model.predict(inp, verbose=0)[0]  # shape (num_classes,)
    max_idx = int(np.argmax(preds))
    max_prob = float(preds[max_idx])

    if max_prob < UNKNOWN_THRESHOLD:
        return "Unknown", max_prob
    else:
        return idx2class[max_idx], max_prob


def log_unknown_face(face_img, prob):
    """Save unknown face and append to log file."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    img_path = os.path.join(LOG_DIR, f"unknown_{ts}.jpg")
    cv2.imwrite(img_path, face_img)

    log_file = os.path.join(LOG_DIR, "unknown_log.txt")
    with open(log_file, "a") as f:
        f.write(f"{ts}, prob={prob:.4f}, file={img_path}\n")


# -------------------------------------------------
# MAIN LOOP
# -------------------------------------------------
def main():
    cap = cv2.VideoCapture(0)  # default webcam

    if not cap.isOpened():
        print("[ERROR] Cannot open webcam.")
        return

    print("[INFO] Press 'q' to quit, 's' to save screenshot.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert to grayscale for Haar, but we draw on color frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detectMultiScale: returns (x, y, w, h) for each detected face
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(60, 60),
        )

        for (x, y, w, h) in faces:
            x1 = x
            y1 = y
            x2 = x + w
            y2 = y + h

            # Crop from original color frame
            face_color = frame[y1:y2, x1:x2]
            if face_color.size == 0:
                continue

            label, conf = predict_identity(face_color)

            # Choose color: green for known, red for unknown
            color = (0, 255, 0) if label != "Unknown" else (0, 0, 255)

            # Draw rectangle and label
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            text = f"{label} ({conf:.2f})"
            cv2.putText(
                frame,
                text,
                (x1, max(0, y1 - 10)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                color,
                2,
            )

            # Log unknown faces
            if label == "Unknown":
                log_unknown_face(face_color, conf)

        cv2.imshow("Real-Time Face Recognition (Haar + CNN)", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break
        elif key == ord("s"):
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = os.path.join(SCREENSHOT_DIR, f"screenshot_{ts}.jpg")
            cv2.imwrite(path, frame)
            print("[INFO] Screenshot saved:", path)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
