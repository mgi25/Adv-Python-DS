# realtime_yolo_face_recognition.py
# Run real-time face detection with YOLO and recognition with a trained CNN model.

import json
import os
from datetime import datetime
from typing import List, Tuple

import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Configuration
IMG_SIZE = 160
MODEL_PATH = "face_cnn_mobilenetv2.h5"
CLASS_INDICES_PATH = "class_indices.json"
YOLO_CFG = "yolov3-face.cfg"
YOLO_WEIGHTS = "yolov3-face.weights"
YOLO_CONF_THRESHOLD = 0.5
YOLO_NMS_THRESHOLD = 0.4
UNKNOWN_THRESHOLD = 0.7
UNKNOWN_LOG_DIR = "unknown_logs"

# Globals initialized in main
net = None
cnn_model = None
idx_to_class = None


def load_yolo_model():
    """Load YOLO model from configuration and weights files."""
    global net
    net = cv2.dnn.readNetFromDarknet(YOLO_CFG, YOLO_WEIGHTS)


def load_cnn_model():
    """Load trained CNN model and class indices."""
    global cnn_model, idx_to_class
    cnn_model = load_model(MODEL_PATH)
    with open(CLASS_INDICES_PATH, "r", encoding="utf-8") as f:
        class_indices = json.load(f)
    idx_to_class = {idx: name for name, idx in class_indices.items()}


def detect_faces_yolo(frame: np.ndarray) -> List[List[int]]:
    """Detect faces in a frame using YOLO and return bounding boxes [x, y, w, h]."""
    (H, W) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    ln = net.getLayerNames()
    ln = [ln[i - 1] for i in net.getUnconnectedOutLayers().flatten()]
    layer_outputs = net.forward(ln)

    boxes = []
    confidences = []

    for output in layer_outputs:
        for detection in output:
            scores = detection[5:]
            confidence = float(np.max(scores))
            if confidence > YOLO_CONF_THRESHOLD:
                box = detection[0:4] * np.array([W, H, W, H])
                (center_x, center_y, width, height) = box.astype("int")
                x = int(center_x - (width / 2))
                y = int(center_y - (height / 2))
                boxes.append([x, y, int(width), int(height)])
                confidences.append(confidence)

    idxs = cv2.dnn.NMSBoxes(boxes, confidences, YOLO_CONF_THRESHOLD, YOLO_NMS_THRESHOLD)
    final_boxes = [boxes[i] for i in idxs.flatten()] if len(idxs) > 0 else []
    return final_boxes


def preprocess_face(face_img: np.ndarray) -> np.ndarray:
    """Resize and normalize a face image for CNN prediction."""
    face_resized = cv2.resize(face_img, (IMG_SIZE, IMG_SIZE))
    face_normalized = face_resized.astype("float32") / 255.0
    face_expanded = np.expand_dims(face_normalized, axis=0)
    return face_expanded


def predict_identity(face_img: np.ndarray) -> Tuple[str, float]:
    """Predict face identity using CNN model. Returns label and confidence."""
    preprocessed = preprocess_face(face_img)
    preds = cnn_model.predict(preprocessed, verbose=0)[0]
    max_idx = int(np.argmax(preds))
    max_prob = float(preds[max_idx])
    if max_prob >= UNKNOWN_THRESHOLD:
        label = idx_to_class.get(max_idx, "Unknown")
    else:
        label = "Unknown"
    return label, max_prob


def log_unknown_face(face_img: np.ndarray, prob: float) -> None:
    """Save unknown face images and append a log entry."""
    os.makedirs(UNKNOWN_LOG_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"unknown_{timestamp}.jpg"
    filepath = os.path.join(UNKNOWN_LOG_DIR, filename)
    cv2.imwrite(filepath, face_img)
    log_line = f"{timestamp}\tprob={prob:.4f}\t{filepath}\n"
    with open(os.path.join(UNKNOWN_LOG_DIR, "unknown_log.txt"), "a", encoding="utf-8") as f:
        f.write(log_line)


def main():
    load_yolo_model()
    load_cnn_model()

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print("Press 'q' to quit, 's' to save a screenshot.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to read frame from webcam.")
            break

        boxes = detect_faces_yolo(frame)

        for (x, y, w, h) in boxes:
            x = max(0, x)
            y = max(0, y)
            w = max(1, w)
            h = max(1, h)
            face_crop = frame[y : y + h, x : x + w]
            if face_crop.size == 0:
                continue

            label, prob = predict_identity(face_crop)
            color = (0, 255, 0) if label != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            text = f"{label} ({prob:.2f})"
            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

            if label == "Unknown":
                log_unknown_face(face_crop, prob)

        cv2.imshow("Real-Time Face Recognition (YOLO + CNN)", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        if key == ord("s"):
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"screenshot_{ts}.jpg"
            cv2.imwrite(screenshot_path, frame)
            print(f"Saved screenshot to {screenshot_path}")

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
