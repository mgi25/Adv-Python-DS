# train_cnn.py
# Train a MobileNetV2-based CNN for face recognition using a directory-structured dataset.

import json
import os

import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Configuration
IMG_SIZE = 160
BATCH_SIZE = 16
EPOCHS = 20
TRAIN_DIR = "dataset_faces/train"
VAL_DIR = "dataset_faces/val"
MODEL_PATH = "face_cnn_mobilenetv2.h5"
CLASS_INDICES_PATH = "class_indices.json"


def build_model(num_classes: int) -> models.Model:
    """Create a MobileNetV2-based classification model."""
    base_model = MobileNetV2(
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
        include_top=False,
        weights="imagenet",
    )
    base_model.trainable = False  # Freeze base for fast transfer learning

    inputs = layers.Input(shape=(IMG_SIZE, IMG_SIZE, 3))
    x = base_model(inputs, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.3)(x)
    x = layers.Dense(128, activation="relu")(x)
    x = layers.Dropout(0.3)(x)
    outputs = layers.Dense(num_classes, activation="softmax")(x)

    model = models.Model(inputs, outputs, name="FaceMobileNetV2")
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


def create_generators():
    """Create training and validation data generators."""
    train_datagen = ImageDataGenerator(
        rescale=1.0 / 255,
        rotation_range=15,
        width_shift_range=0.1,
        height_shift_range=0.1,
        zoom_range=0.1,
        horizontal_flip=True,
    )
    val_datagen = ImageDataGenerator(rescale=1.0 / 255)

    train_gen = train_datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode="categorical",
    )
    val_gen = val_datagen.flow_from_directory(
        VAL_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode="categorical",
    )
    return train_gen, val_gen


def main():
    os.makedirs(os.path.dirname(MODEL_PATH) or ".", exist_ok=True)

    train_gen, val_gen = create_generators()
    num_classes = train_gen.num_classes

    model = build_model(num_classes)
    model.summary()

    callbacks = [
        ModelCheckpoint(
            MODEL_PATH,
            monitor="val_accuracy",
            save_best_only=True,
            mode="max",
            verbose=1,
        ),
        EarlyStopping(
            monitor="val_accuracy",
            patience=5,
            restore_best_weights=True,
            verbose=1,
            mode="max",
        ),
    ]

    history = model.fit(
        train_gen,
        epochs=EPOCHS,
        validation_data=val_gen,
        callbacks=callbacks,
    )

    # Save class indices for inference
    with open(CLASS_INDICES_PATH, "w", encoding="utf-8") as f:
        json.dump(train_gen.class_indices, f, ensure_ascii=False, indent=2)

    final_val_acc = history.history.get("val_accuracy", [None])[-1]
    print(f"Final validation accuracy: {final_val_acc:.4f}" if final_val_acc is not None else "Validation accuracy not available")


if __name__ == "__main__":
    main()
