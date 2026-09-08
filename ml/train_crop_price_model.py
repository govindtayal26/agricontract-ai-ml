import os
import pandas as pd
import joblib

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "data",
    "crop_prices.csv"
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "models",
    "crop_price_model.joblib"
)


# -------------------------
# 1. Load dataset
# -------------------------

df = pd.read_csv(DATA_PATH)

print("Dataset shape:", df.shape)
print(df.head())


# -------------------------
# 2. Separate features
# -------------------------

X = df.drop("price", axis=1)
y = df["price"]


# -------------------------
# 3. Feature types
# -------------------------

categorical_features = [
    "crop",
    "state"
]

numerical_features = [
    "month",
    "rainfall",
    "temperature",
    "quantity",
    "previous_price"
]


# -------------------------
# 4. Preprocessing
# -------------------------

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        )
    ],
    remainder="passthrough"
)


# -------------------------
# 5. ML model
# -------------------------

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)


# -------------------------
# 6. Pipeline
# -------------------------

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)


# -------------------------
# 7. Train/test split
# -------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# -------------------------
# 8. Train
# -------------------------

pipeline.fit(X_train, y_train)


# -------------------------
# 9. Evaluate
# -------------------------

predictions = pipeline.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
rmse = mean_squared_error(
    y_test,
    predictions
) ** 0.5

r2 = r2_score(
    y_test,
    predictions
)

print("\nModel Performance")
print("--------------------")
print("MAE :", mae)
print("RMSE:", rmse)
print("R2  :", r2)


# -------------------------
# 10. Save model
# -------------------------

os.makedirs(
    os.path.dirname(MODEL_PATH),
    exist_ok=True
)

joblib.dump(
    pipeline,
    MODEL_PATH
)

print("\nModel saved to:")
print(MODEL_PATH)