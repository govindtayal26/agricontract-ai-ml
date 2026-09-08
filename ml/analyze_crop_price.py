import os
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# =========================================================
# 1. PATH
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATA_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "data",
    "crop_prices.csv"
)


# =========================================================
# 2. LOAD DATA
# =========================================================

df = pd.read_csv(DATA_PATH)

print("\n========== DATASET ==========")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\nFirst 5 rows:")
print(df.head())


# =========================================================
# 3. BASIC DATA ANALYSIS
# =========================================================

print("\n========== DATA TYPES ==========")
print(df.dtypes)

print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())

print("\n========== DUPLICATES ==========")
print(df.duplicated().sum())

print("\n========== STATISTICS ==========")
print(df.describe())


# =========================================================
# 4. CATEGORICAL ANALYSIS
# =========================================================

print("\n========== CROPS ==========")
print(df["crop"].value_counts())

print("\n========== STATES ==========")
print(df["state"].value_counts())


# =========================================================
# 5. FEATURE ENGINEERING
# =========================================================

# Create a simple climate index
df["climate_index"] = (
    df["rainfall"] / (df["temperature"] + 1)
)

# Price change from previous price
df["price_change"] = (
    df["previous_price"] - df["price"]
)

print("\n========== ENGINEERED FEATURES ==========")
print(
    df[
        [
            "climate_index",
            "price_change"
        ]
    ].head()
)


# =========================================================
# 6. FEATURES / TARGET
# =========================================================

X = df.drop("price", axis=1)
y = df["price"]


categorical_features = [
    "crop",
    "state"
]

numerical_features = [
    "month",
    "rainfall",
    "temperature",
    "quantity",
    "previous_price",
    "climate_index",
    "price_change"
]


# =========================================================
# 7. PREPROCESSING
# =========================================================

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


# =========================================================
# 8. MODELS
# =========================================================

models = {

    "Linear Regression":
        LinearRegression(),

    "Random Forest":
        RandomForestRegressor(
            n_estimators=200,
            random_state=42
        ),

    "Gradient Boosting":
        GradientBoostingRegressor(
            random_state=42
        )
}


# =========================================================
# 9. TRAIN / TEST SPLIT
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# =========================================================
# 10. MODEL COMPARISON
# =========================================================

results = []

for name, model in models.items():

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model)
        ]
    )

    pipeline.fit(
        X_train,
        y_train
    )

    predictions = pipeline.predict(
        X_test
    )

    mae = mean_absolute_error(
        y_test,
        predictions
    )

    rmse = mean_squared_error(
        y_test,
        predictions
    ) ** 0.5

    r2 = r2_score(
        y_test,
        predictions
    )

    results.append({
        "Model": name,
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2
    })


# =========================================================
# 11. RESULTS
# =========================================================

results_df = pd.DataFrame(results)

print("\n========== MODEL COMPARISON ==========")

print(
    results_df.to_string(
        index=False
    )
)


# =========================================================
# 12. VISUALIZATION
# =========================================================

plt.figure(figsize=(10, 6))

plt.bar(
    results_df["Model"],
    results_df["R2"]
)

plt.ylabel("R² Score")
plt.xlabel("Model")
plt.title("Crop Price Prediction - Model Comparison")

plt.xticks(
    rotation=20
)

plt.tight_layout()

plt.show()