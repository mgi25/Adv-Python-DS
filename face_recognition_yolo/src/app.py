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
DATASET_TRAIN_DIR = os.path.join(BASE_DIR, "dataset_faces", "train")
LOG_DIR = os.path.join(BASE_DIR, "logs", "unknown_faces")
SCREENSHOT_DIR = os.path.join(BASE_DIR, "screenshots")

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

MODEL_PATH = os.path.join(MODELS_DIR, "face_cnn_mobilenetv2.h5")
CLASS_INDICES_PATH = os.path.join(MODELS_DIR, "class_indices.json")

# -------------------------------------------------
# SETTINGS
# -------------------------------------------------
IMG_SIZE = 160

# cosine similarity in [0,1]; closer to 1 → more similar
# STRONGER threshold for unknown handling
SIM_THRESHOLD = 0.85          # if best similarity < this => Unknown
MARGIN_THRESHOLD = 0.10       # best_sim - second_best_sim must be at least this

# OpenCV Haar cascade for face detection
HAAR_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(HAAR_PATH)

# -------------------------------------------------
# LOAD CNN MODEL + CREATE EMBEDDING MODEL
# -------------------------------------------------
print("[INFO] Loading CNN face recognition model...")
base_model = tf.keras.models.load_model(MODEL_PATH)

# Find the 128-unit Dense layer to use as embedding output
embedding_layer = None
for layer in reversed(base_model.layers):
    # In Keras 3, Dense has 'units' instead of reliable 'output_shape' here
    if isinstance(layer, tf.keras.layers.Dense) and getattr(layer, "units", None) == 128:
        embedding_layer = layer
        break

if embedding_layer is None:
    raise RuntimeError(
        "Could not find a 128-unit Dense layer for embeddings. "
        "Make sure train_cnn.py uses Dense(128) before the final output layer."
    )

embedding_model = tf.keras.Model(
    inputs=base_model.input,
    outputs=embedding_layer.output
)

# (Optional) load mapping just for reference / debugging
with open(CLASS_INDICES_PATH, "r") as f:
    class_indices = json.load(f)
idx2class = {v: k for k, v in class_indices.items()}
print("[INFO] Known classes (from training):", idx2class)

# -------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------
def preprocess_face(face_img):
    """Resize and normalize cropped face for embedding model."""
    face_resized = cv2.resize(face_img, (IMG_SIZE, IMG_SIZE))
    face_resized = face_resized.astype("float32") / 255.0
    face_resized = np.expand_dims(face_resized, axis=0)  # (1, H, W, 3)
    return face_resized


def get_embedding(face_img):
    """Get 128-d normalized embedding vector for a face."""
    inp = preprocess_face(face_img)
    emb = embedding_model.predict(inp, verbose=0)[0]  # (128,)
    norm = np.linalg.norm(emb) + 1e-10
    return emb / norm


def cosine_similarity(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10))


def log_unknown_face(face_img, best_sim):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    img_path = os.path.join(LOG_DIR, f"unknown_{ts}.jpg")
    cv2.imwrite(img_path, face_img)

    log_file = os.path.join(LOG_DIR, "unknown_log.txt")
    with open(log_file, "a") as f:
        f.write(f"{ts}, best_sim={best_sim:.4f}, file={img_path}\n")


# -------------------------------------------------
# BUILD FACE DATABASE FROM TRAIN IMAGES
# -------------------------------------------------
def build_face_database():
    """
    For each person folder in dataset_faces/train,
    compute average embedding vector from all images.
    Returns: dict{name: embedding_vector}
    """
    print("[INFO] Building face database from training images...")
    face_db = {}
    exts = (".jpg", ".jpeg", ".png", ".bmp")

    for person_name in sorted(os.listdir(DATASET_TRAIN_DIR)):
        person_dir = os.path.join(DATASET_TRAIN_DIR, person_name)
        if not os.path.isdir(person_dir):
            continue

        embeddings = []
        for fname in os.listdir(person_dir):
            if not fname.lower().endswith(exts):
                continue

            img_path = os.path.join(person_dir, fname)
            img = cv2.imread(img_path)
            if img is None:
                continue

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(60, 60),
            )

            if len(faces) == 0:
                continue

            # Take the largest detected face (if multiple)
            faces_sorted = sorted(faces, key=lambda b: b[2] * b[3], reverse=True)
            (x, y, w, h) = faces_sorted[0]
            face_color = img[y:y + h, x:x + w]

            emb = get_embedding(face_color)
            embeddings.append(emb)

        if len(embeddings) == 0:
            print(f"[WARN] No faces found for person '{person_name}', skipping.")
            continue

        mean_emb = np.mean(embeddings, axis=0)
        # normalize mean embedding too
        mean_emb = mean_emb / (np.linalg.norm(mean_emb) + 1e-10)
        face_db[person_name] = mean_emb
        print(f"[INFO] Added '{person_name}' with {len(embeddings)} samples.")

    if not face_db:
        print("[ERROR] Face database is empty! Check your dataset.")
    else:
        print("[INFO] Face database built with", len(face_db), "persons.")

    return face_db


FACE_DB = build_face_database()


# -------------------------------------------------
# RECOGNITION USING EMBEDDINGS
# -------------------------------------------------
def recognize_face(face_img):
    """
    Compute embedding for face_img and compare with all persons in FACE_DB.
    Returns (label, best_sim).
    Uses:
      - SIM_THRESHOLD       : minimum similarity to be considered known
      - MARGIN_THRESHOLD    : best_sim must be clearly ahead of second_best_sim
    """
    if not FACE_DB:
        return "Unknown", 0.0

    emb = get_embedding(face_img)

    best_name = None
    best_sim = -1.0
    second_best_sim = -1.0

    # find best and second best similarity
    for name, ref_emb in FACE_DB.items():
        sim = cosine_similarity(emb, ref_emb)

        if sim > best_sim:
            second_best_sim = best_sim
            best_sim = sim
            best_name = name
        elif sim > second_best_sim:
            second_best_sim = sim

    # Debug line – keep for tuning, you can comment it later
    print(f"[DEBUG] best={best_name} {best_sim:.3f}, second={second_best_sim:.3f}")

    # Condition 1: absolute similarity must be high enough
    if best_sim < SIM_THRESHOLD:
        return "Unknown", best_sim

    # Condition 2: best must be clearly better than second-best (if second exists)
    if second_best_sim > 0 and (best_sim - second_best_sim) < MARGIN_THRESHOLD:
        return "Unknown", best_sim

    # Otherwise accept as known
    return best_name, best_sim


# -------------------------------------------------
# MAIN LOOP
# -------------------------------------------------
def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("[ERROR] Cannot open webcam.")
        return

    print("[INFO] Press 'q' to quit, 's' to save screenshot.")
    print(f"[INFO] Similarity threshold for known faces: {SIM_THRESHOLD}")
    print(f"[INFO] Margin threshold between best and second: {MARGIN_THRESHOLD}")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(60, 60),
        )

        for (x, y, w, h) in faces:
            x1, y1 = x, y
            x2, y2 = x + w, y + h

            face_color = frame[y1:y2, x1:x2]
            if face_color.size == 0:
                continue

            label, sim = recognize_face(face_color)

            color = (0, 255, 0) if label != "Unknown" else (0, 0, 255)

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            text = f"{label} ({sim:.2f})"
            cv2.putText(
                frame,
                text,
                (x1, max(0, y1 - 10)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                color,
                2,
            )

            if label == "Unknown":
                log_unknown_face(face_color, sim)

        cv2.imshow("Real-Time Face Recognition (Embedding + NN)", frame)
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
