import os
import json
import numpy as np
import tensorflow as tf

from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input


# =========================
# PATHS
# =========================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
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


# =========================
# PREDICTION FUNCTION
# =========================

def predict_disease(image_path):

    # Load image
    img = image.load_img(
        image_path,
        target_size=(224, 224)
    )

    # Convert image to array
    img_array = image.img_to_array(img)

    # MobileNetV2 preprocessing
    img_array = preprocess_input(
        img_array
    )

    # Add batch dimension
    img_array = np.expand_dims(
        img_array,
        axis=0
    )

    # Prediction
    predictions = model.predict(
        img_array,
        verbose=0
    )

    # Highest probability
    predicted_index = int(
        np.argmax(predictions[0])
    )

    confidence = float(
        np.max(predictions[0]) * 100
    )

    disease = class_names[
        predicted_index
    ]

    return disease, confidence


# =========================
# COMMAND LINE TEST
# =========================

if __name__ == "__main__":

    image_path = input(
        "\nEnter potato leaf image path: "
    ).strip()

    if not os.path.exists(image_path):

        print("\n❌ Image not found.")

    else:

        disease, confidence = predict_disease(
            image_path
        )

        print("\n==============================")
        print("POTATO DISEASE PREDICTION")
        print("==============================")

        print(
            f"Disease    : {disease}"
        )

        print(
            f"Confidence : {confidence:.2f}%"
        )