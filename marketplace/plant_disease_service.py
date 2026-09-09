import os
import json
import numpy as np

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

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

_model = None
_classes = None


def get_model():
    global _model

    if _model is None:
        from tensorflow.keras.models import load_model

        _model = load_model(
            MODEL_PATH,
            compile=False
        )

    return _model


def get_classes():
    global _classes

    if _classes is None:
        with open(CLASS_PATH, "r") as file:
            _classes = json.load(file)

    return _classes


def predict_disease(image_path):

    from tensorflow.keras.preprocessing import image
    from tensorflow.keras.applications.mobilenet_v2 import (
        preprocess_input
    )

    model = get_model()
    classes = get_classes()

    img = image.load_img(
        image_path,
        target_size=(224, 224)
    )

    img_array = image.img_to_array(img)

    img_array = preprocess_input(img_array)

    img_array = np.expand_dims(
        img_array,
        axis=0
    )

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