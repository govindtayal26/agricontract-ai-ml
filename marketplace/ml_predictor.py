import os
import joblib
import pandas as pd
from django.conf import settings


MODEL_PATH = os.path.join(
    settings.BASE_DIR,
    "ml",
    "models",
    "crop_price_model.joblib"
)


_model = None


def get_price_model():
    global _model

    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"ML model not found: {MODEL_PATH}. "
                "Run python ml/train_crop_price_model.py first."
            )

        _model = joblib.load(MODEL_PATH)

    return _model


def predict_crop_price(
    crop,
    state,
    month,
    rainfall,
    temperature,
    quantity,
    previous_price
):
    model = get_price_model()

    data = pd.DataFrame([
        {
            "crop": crop,
            "state": state,
            "month": month,
            "rainfall": rainfall,
            "temperature": temperature,
            "quantity": quantity,
            "previous_price": previous_price,
        }
    ])

    prediction = model.predict(data)[0]

    return round(float(prediction), 2)