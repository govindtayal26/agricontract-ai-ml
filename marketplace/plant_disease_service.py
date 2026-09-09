import os
import json
import numpy as np

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input


# Model ka path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "plant_disease",
    "models",
    "potato_disease_model.keras"
)

CLASS_PATH = os.path.join(
    BASE_DIR,
    "plant_disease",
    "models",
    "class_names.json"
)


# Model ko memory mein rakhne ke liye
_model = None
_classes = None


def get_model():

    global _model

    if _model is None:
        _model = load_model(MODEL_PATH)

    return _model


def get_classes():

    global _classes

    if _classes is None:
        with open(CLASS_PATH, "r") as file:
            _classes = json.load(file)

    return _classes


def predict_disease(image_path):

    model = get_model()
    classes = get_classes()

    # Image load
    img = image.load_img(
        image_path,
        target_size=(224, 224)
    )

    # Image → array
    img_array = image.img_to_array(img)

    # MobileNetV2 preprocessing
    img_array = preprocess_input(img_array)

    # Batch dimension
    img_array = np.expand_dims(
        img_array,
        axis=0
    )

    # Prediction
    predictions = model.predict(
        img_array,
        verbose=0
    )[0]

    predicted_index = int(
        np.argmax(predictions)
    )

    confidence = float(
        predictions[predicted_index] * 100
    )

    disease = classes[predicted_index]

    return {
        "disease": disease,
        "confidence": round(confidence, 2)
    }