import os
import json
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

# ------------ PATHS (relative to project root) -------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # face_recognition_yolo/

TRAIN_DIR = os.path.join(BASE_DIR, "dataset_faces", "train")
VAL_DIR   = os.path.join(BASE_DIR, "dataset_faces", "val")

MODELS_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODELS_DIR, exist_ok=True)

MODEL_PATH = os.path.join(MODELS_DIR, "face_cnn_mobilenetv2.h5")
CLASS_INDICES_PATH = os.path.join(MODELS_DIR, "class_indices.json")

# ------------ HYPERPARAMETERS ------------------------------
IMG_SIZE = 160
BATCH_SIZE = 16
EPOCHS = 20

def build_model(num_classes: int) -> Model:
    base_model = MobileNetV2(
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
        include_top=False,
        weights="imagenet"
    )
    base_model.trainable = False  # freeze for now (transfer learning)

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dropout(0.3)(x)
    x = Dense(128, activation="relu")(x)
    x = Dropout(0.3)(x)
    outputs = Dense(num_classes, activation="softmax")(x)

    model = Model(inputs=base_model.input, outputs=outputs)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(1e-3),
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )
    return model

def main():
    # --------- DATA GENERATORS ----------
    train_datagen = ImageDataGenerator(
        rescale=1.0 / 255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True
    )

    val_datagen = ImageDataGenerator(rescale=1.0 / 255)

    train_gen = train_datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode="categorical"
    )

    val_gen = val_datagen.flow_from_directory(
        VAL_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode="categorical"
    )

    num_classes = len(train_gen.class_indices)
    print("Classes:", train_gen.class_indices)

    # save mapping for inference
    with open(CLASS_INDICES_PATH, "w") as f:
        json.dump(train_gen.class_indices, f)

    model = build_model(num_classes)

    ckpt = ModelCheckpoint(
        MODEL_PATH,
        monitor="val_accuracy",
        mode="max",
        save_best_only=True,
        verbose=1
    )

    early = EarlyStopping(
        monitor="val_accuracy",
        patience=5,
        restore_best_weights=True
    )

    history = model.fit(
        train_gen,
        epochs=EPOCHS,
        validation_data=val_gen,
        callbacks=[ckpt, early]
    )

    val_loss, val_acc = model.evaluate(val_gen)
    print(f"Final validation accuracy: {val_acc:.4f}")

if __name__ == "__main__":
    main()
import os
import json
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

# ------------ PATHS (relative to project root) -------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # face_recognition_yolo/

TRAIN_DIR = os.path.join(BASE_DIR, "dataset_faces", "train")
VAL_DIR   = os.path.join(BASE_DIR, "dataset_faces", "val")

MODELS_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODELS_DIR, exist_ok=True)

MODEL_PATH = os.path.join(MODELS_DIR, "face_cnn_mobilenetv2.h5")
CLASS_INDICES_PATH = os.path.join(MODELS_DIR, "class_indices.json")

# ------------ HYPERPARAMETERS ------------------------------
IMG_SIZE = 160
BATCH_SIZE = 16
EPOCHS = 25

def build_model(num_classes: int) -> Model:
    base_model = MobileNetV2(
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
        include_top=False,
        weights="imagenet"
    )

    # First stage: keep base frozen
    base_model.trainable = False

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dropout(0.3)(x)
    x = Dense(128, activation="relu")(x)
    x = Dropout(0.3)(x)
    outputs = Dense(num_classes, activation="softmax")(x)

    model = Model(inputs=base_model.input, outputs=outputs)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(1e-3),
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )
    return model


def main():
    # --------- DATA GENERATORS ----------
    train_datagen = ImageDataGenerator(
        rescale=1.0 / 255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True
    )

    val_datagen = ImageDataGenerator(rescale=1.0 / 255)

    train_gen = train_datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode="categorical"
    )

    val_gen = val_datagen.flow_from_directory(
        VAL_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode="categorical"
    )

    num_classes = len(train_gen.class_indices)
    print("Classes:", train_gen.class_indices)

    # save mapping for inference
    with open(CLASS_INDICES_PATH, "w") as f:
        json.dump(train_gen.class_indices, f)

    model = build_model(num_classes)

    ckpt = ModelCheckpoint(
        MODEL_PATH,
        monitor="val_accuracy",
        mode="max",
        save_best_only=True,
        verbose=1
    )

    early = EarlyStopping(
        monitor="val_accuracy",
        patience=7,
        restore_best_weights=True
    )

    history = model.fit(
        train_gen,
        epochs=EPOCHS,
        validation_data=val_gen,
        callbacks=[ckpt, early]
    )

    val_loss, val_acc = model.evaluate(val_gen)
    print(f"Final validation accuracy: {val_acc:.4f}")


if __name__ == "__main__":
    main()
