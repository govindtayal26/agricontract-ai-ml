import os
import json
import tensorflow as tf

from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import (
    EarlyStopping,
    ReduceLROnPlateau,
    ModelCheckpoint
)

# =========================
# CONFIG
# =========================

IMG_SIZE = (224, 224)
BATCH_SIZE = 32
SEED = 42

DATASET_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "dataset"
)

MODEL_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "models"
)

os.makedirs(MODEL_DIR, exist_ok=True)

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "potato_disease_model.keras"
)

# =========================
# DATA AUGMENTATION
# =========================

train_datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input,

    rotation_range=20,
    width_shift_range=0.15,
    height_shift_range=0.15,
    zoom_range=0.15,
    horizontal_flip=True,

    validation_split=0.2
)

validation_datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input,
    validation_split=0.2
)

# =========================
# TRAIN DATA
# =========================

train_data = train_datagen.flow_from_directory(
    DATASET_DIR,

    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,

    class_mode="categorical",

    subset="training",
    seed=SEED,

    shuffle=True
)

# =========================
# VALIDATION DATA
# =========================

validation_data = validation_datagen.flow_from_directory(
    DATASET_DIR,

    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,

    class_mode="categorical",

    subset="validation",
    seed=SEED,

    shuffle=False
)

print("\nClass mapping:")
print(train_data.class_indices)

# =========================
# SAVE CLASS NAMES
# =========================

class_names = list(train_data.class_indices.keys())

with open(
    os.path.join(MODEL_DIR, "class_names.json"),
    "w"
) as f:
    json.dump(class_names, f, indent=4)

# =========================
# MOBILE NET V2
# =========================

base_model = MobileNetV2(
    weights="imagenet",
    include_top=False,
    input_shape=(224, 224, 3)
)

# Freeze pretrained layers
base_model.trainable = False

# =========================
# CLASSIFICATION HEAD
# =========================

model = models.Sequential([
    
    base_model,

    layers.GlobalAveragePooling2D(),

    layers.Dense(
        128,
        activation="relu"
    ),

    layers.Dropout(0.4),

    layers.Dense(
        len(class_names),
        activation="softmax"
    )
])

# =========================
# COMPILE
# =========================

model.compile(
    optimizer=tf.keras.optimizers.Adam(
        learning_rate=0.001
    ),

    loss="categorical_crossentropy",

    metrics=["accuracy"]
)

model.summary()

# =========================
# CALLBACKS
# =========================

callbacks = [

    ModelCheckpoint(
        MODEL_PATH,
        monitor="val_accuracy",
        save_best_only=True,
        verbose=1
    ),

    EarlyStopping(
        monitor="val_loss",
        patience=4,
        restore_best_weights=True,
        verbose=1
    ),

    ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.2,
        patience=2,
        verbose=1
    )
]

# =========================
# TRAINING
# =========================

print("\nStarting transfer learning...\n")

history = model.fit(
    train_data,

    validation_data=validation_data,

    epochs=15,

    callbacks=callbacks
)

# =========================
# FINE TUNING
# =========================

print("\nStarting fine tuning...\n")

base_model.trainable = True

# Freeze early MobileNet layers
for layer in base_model.layers[:-30]:
    layer.trainable = False

model.compile(
    optimizer=tf.keras.optimizers.Adam(
        learning_rate=1e-5
    ),

    loss="categorical_crossentropy",

    metrics=["accuracy"]
)

fine_tune_history = model.fit(
    train_data,

    validation_data=validation_data,

    epochs=10,

    callbacks=callbacks
)

# =========================
# FINAL SAVE
# =========================

model.save(MODEL_PATH)

print("\n================================")
print("Training completed successfully!")
print("================================")

print(f"\nModel saved at:")
print(MODEL_PATH)