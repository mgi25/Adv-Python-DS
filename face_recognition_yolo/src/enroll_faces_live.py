import os
import cv2

# ---------------- PATHS ----------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # face_recognition_yolo/

DATASET_DIR = os.path.join(BASE_DIR, "dataset_faces")
TRAIN_DIR = os.path.join(DATASET_DIR, "train")
VAL_DIR = os.path.join(DATASET_DIR, "val")

os.makedirs(TRAIN_DIR, exist_ok=True)
os.makedirs(VAL_DIR, exist_ok=True)

# Haar cascade for face detection
HAAR_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(HAAR_PATH)


def capture_faces_auto(target_samples=80, person_name="person"):
    """
    Automatically capture face images for one person.
    Camera runs; when a face is detected, it captures every Nth frame.
    Press 'q' to stop early.
    """
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERROR] Cannot open webcam.")
        return []

    captured_faces = []
    frame_counter = 0
    CAPTURE_EVERY_N_FRAMES = 3  # capture every 3rd frame with a face

    print(f"\n[INFO] Starting automatic capture for: {person_name}")
    print("[INFO] Instructions:")
    print("  - Look at the camera and move your head slowly (left/right/up/down).")
    print("  - System auto-captures when a face is detected.")
    print("  - Target samples:", target_samples)
    print("  - Press 'q' to finish early.\n")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_counter += 1
        display = frame.copy()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(60, 60),
        )

        # Draw boxes and status text
        for (x, y, w, h) in faces:
            cv2.rectangle(display, (x, y), (x + w, y + h), (255, 0, 0), 2)

        text_info = f"{person_name}: {len(captured_faces)}/{target_samples}  (press 'q' to finish)"
        cv2.putText(display, text_info, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow("Live Auto Enrollment", display)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            print("[INFO] Stopping capture by user request.")
            break

        # Auto capture every Nth frame with a detected face
        if len(faces) > 0 and (frame_counter % CAPTURE_EVERY_N_FRAMES == 0):
            faces_sorted = sorted(faces, key=lambda b: b[2] * b[3], reverse=True)
            (x, y, w, h) = faces_sorted[0]
            face_img = frame[y:y + h, x:x + w]
            if face_img.size == 0:
                continue

            captured_faces.append(face_img)
            print(f"[INFO] Captured sample #{len(captured_faces)}")

            if len(captured_faces) >= target_samples:
                print("[INFO] Reached target sample count.")
                break

    cap.release()
    cv2.destroyAllWindows()

    print(f"[INFO] Total captured samples for {person_name}: {len(captured_faces)}")
    return captured_faces


def save_faces(person_name, captured_faces):
    """
    Save captured faces into:
        dataset_faces/train/<person_name>/
        dataset_faces/val/<person_name>/
    First 80% → train, last 20% → val.
    """
    if len(captured_faces) == 0:
        print("[WARN] No faces to save for this person.")
        return

    train_person_dir = os.path.join(TRAIN_DIR, person_name)
    val_person_dir = os.path.join(VAL_DIR, person_name)
    os.makedirs(train_person_dir, exist_ok=True)
    os.makedirs(val_person_dir, exist_ok=True)

    total = len(captured_faces)
    n_train = int(0.8 * total)
    n_val = total - n_train

    count_train = 0
    count_val = 0

    for i, img in enumerate(captured_faces):
        if i < n_train:
            filename = os.path.join(
                train_person_dir, f"{person_name}_train_{count_train:03d}.jpg"
            )
            cv2.imwrite(filename, img)
            count_train += 1
        else:
            filename = os.path.join(
                val_person_dir, f"{person_name}_val_{count_val:03d}.jpg"
            )
            cv2.imwrite(filename, img)
            count_val += 1

    print(f"[INFO] Saved {count_train} images to {train_person_dir}")
    print(f"[INFO] Saved {count_val} images to {val_person_dir}\n")


def main():
    print("===========================================")
    print("   LIVE AUTO FACE ENROLLMENT (NAME FIRST)  ")
    print("===========================================\n")
    print("Flow:")
    print("  1) Ask for person's name.")
    print("  2) Automatically capture many face images.")
    print("  3) Save to dataset_faces/train and dataset_faces/val.")
    print("Then you run train_cnn.py to train the model.\n")

    default_target_samples = 80

    while True:
        ans = input("Enroll a NEW person? (y/n): ").strip().lower()
        if ans != "y":
            print("[INFO] Enrollment finished.")
            break

        person_name = input("Enter person's name (no spaces, e.g. 'alen'): ").strip()
        if not person_name:
            print("[WARN] Empty name, skipping.")
            continue

        try:
            user_input = input(
                f"Target samples for {person_name} (default {default_target_samples}): "
            ).strip()
            if user_input == "":
                target_samples = default_target_samples
            else:
                target_samples = int(user_input)
        except ValueError:
            print("[WARN] Invalid number, using default:", default_target_samples)
            target_samples = default_target_samples

        faces = capture_faces_auto(target_samples=target_samples, person_name=person_name)
        save_faces(person_name, faces)

    print("\n[INFO] Now run:  python src/train_cnn.py  to train/update the model.")
    print("[INFO] After that, run your real-time recognition script.")


if __name__ == "__main__":
    main()
