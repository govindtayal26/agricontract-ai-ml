import os
import json
import numpy as np
import tensorflow as tf

from sklearn.metrics import (
    classification_report,
    confusion_matrix
)

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input


# =========================
# PATHS
# =========================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATASET_DIR = os.path.join(
    BASE_DIR,
    "dataset"
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "potato_disease_model.keras"
)

CLASS_PATH = os.path.join(
    BASE_DIR,
    "models",
    "class_names.json"
)


# =========================
# LOAD MODEL
# =========================

print("Loading model...")

model = tf.keras.models.load_model(
    MODEL_PATH
)


# =========================
# LOAD CLASS NAMES
# =========================

with open(CLASS_PATH, "r") as f:
    class_names = json.load(f)

print("\nClasses:")
print(class_names)


# =========================
# VALIDATION DATA
# =========================

datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input,
    validation_split=0.2
)

validation_data = datagen.flow_from_directory(
    DATASET_DIR,

    target_size=(224, 224),

    batch_size=32,

    class_mode="categorical",

    subset="validation",

    shuffle=False
)


# =========================
# MODEL EVALUATION
# =========================

print("\nEvaluating model...\n")

loss, accuracy = model.evaluate(
    validation_data,
    verbose=1
)

print("\n==============================")
print("MODEL PERFORMANCE")
print("==============================")

print(f"Validation Loss     : {loss:.4f}")
print(f"Validation Accuracy : {accuracy * 100:.2f}%")


# =========================
# PREDICTIONS
# =========================

print("\nGenerating predictions...")

predictions = model.predict(
    validation_data,
    verbose=1
)

predicted_classes = np.argmax(
    predictions,
    axis=1
)

true_classes = validation_data.classes


# =========================
# CLASSIFICATION REPORT
# =========================

print("\n==============================")
print("CLASSIFICATION REPORT")
print("==============================")

print(
    classification_report(
        true_classes,
        predicted_classes,
        target_names=class_names,
        digits=4
    )
)


# =========================
# CONFUSION MATRIX
# =========================

cm = confusion_matrix(
    true_classes,
    predicted_classes
)

print("\n==============================")
print("CONFUSION MATRIX")
print("==============================")

print(cm)