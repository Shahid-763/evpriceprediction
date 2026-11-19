import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

os.makedirs("models", exist_ok=True)

def train_and_compare(data, features, target, project_name,
                      categorical_columns):

    X = data[features]
    y = data[target]

    numerical_columns = [
        col for col in features
        if col not in categorical_columns
    ]

    preprocessing = ColumnTransformer(
        transformers=[
            (
                "text",
                OneHotEncoder(handle_unknown="ignore"),
                categorical_columns
            ),
            (
                "numbers",
                "passthrough",
                numerical_columns
            )
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    algorithms = {
        "Linear Regression": LinearRegression(),

        "Decision Tree": DecisionTreeRegressor(
            max_depth=10,
            random_state=42
        ),

        "Random Forest": RandomForestRegressor(
            n_estimators=100,
            max_depth=15,
            random_state=42
        )
    }

    results = []
    best_mae = float("inf")
    best_model = None
    best_name = ""
    print("TRAINING:", project_name.upper())
   

    for name, algorithm in algorithms.items():

        model = Pipeline(steps=[
            ("preprocessing", preprocessing),
            ("algorithm", algorithm)
        ])

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        mae = mean_absolute_error(y_test, predictions)

        rmse = mean_squared_error(
            y_test, predictions
        ) ** 0.5

        r2 = r2_score(y_test, predictions)

        print("\nAlgorithm:", name)
        print("MAE (INR):", round(mae, 2))
        print("RMSE (INR):", round(rmse, 2))
        print("R2 Score:", round(r2, 4))

        results.append({
            "Algorithm": name,
            "MAE": mae,
            "RMSE": rmse,
            "R2 Score": r2
        })

        if mae < best_mae:
            best_mae = mae
            best_model = model
            best_name = name

    result_table = pd.DataFrame(results)

    result_table.to_csv(
        f"models/{project_name}_results.csv",
        index=False
    )

  
    best_model.fit(X, y)

    joblib.dump(
        best_model,
        f"models/{project_name}_best.pkl"
    )

    print("\nMODEL COMPARISON:")
    print(result_table.sort_values("MAE").to_string(index=False))

    print("\nBEST ALGORITHM:", best_name)

    return best_name

def tune_random_forest(
    data,
    features,
    target,
    project_name,
    categorical_columns
):

    X = data[features]
    y = data[target]

    numerical_columns = [
        col for col in features
        if col not in categorical_columns
    ]

    preprocessing = ColumnTransformer(
        transformers=[
            (
                "text",
                OneHotEncoder(handle_unknown="ignore"),
                categorical_columns
            ),
            (
                "numbers",
                "passthrough",
                numerical_columns
            )
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    pipeline = Pipeline(steps=[
        ("preprocessing", preprocessing),
        (
            "algorithm",
            RandomForestRegressor(random_state=42)
        )
    ])

    parameters = {
        "algorithm__n_estimators": [100, 200],
        "algorithm__max_depth": [None, 5],
        "algorithm__min_samples_split": [2, 4],
        "algorithm__min_samples_leaf": [1, 2]
    }
    cv_folds = 3 if len(data) < 100 else 5

    search = GridSearchCV(
        pipeline,
        parameters,
        cv=cv_folds,
        scoring="neg_mean_absolute_error",
        n_jobs=-1
    )
    print("OPTIMIZING:", project_name.upper())
 

    search.fit(X_train, y_train)

    optimized_model = search.best_estimator_

    predictions = optimized_model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)

    rmse = mean_squared_error(
        y_test, predictions
    ) ** 0.5

    r2 = r2_score(y_test, predictions)

    print("\nBest Parameters:")
    print(search.best_params_)

    print("\nOptimized MAE (INR):", round(mae, 2))
    print("Optimized RMSE (INR):", round(rmse, 2))
    print("Optimized R2:", round(r2, 4))

    # Retrain optimized model using all available data
    optimized_model.fit(X, y)

    joblib.dump(
        optimized_model,
        f"models/{project_name}_optimized.pkl"
    )

    print("\nOptimized model saved successfully!")


new_data = pd.read_csv("data/newPrices.csv")

new_data = new_data.dropna().drop_duplicates()

new_features = [
    "model",
    "variant",
    "city",
    "ex_showroom"
]

new_categorical = [
    "model",
    "variant",
    "city"
]

new_best = train_and_compare(
    new_data,
    new_features,
    "onroad",
    "new_ev",
    new_categorical
)


used_data = pd.read_csv("data/usedPrices.csv")

used_data = used_data.dropna().drop_duplicates()

used_features = [
    "brand",
    "model",
    "variant",
    "city",
    "age",
    "km"
]

used_categorical = [
    "brand",
    "model",
    "variant",
    "city"
]

used_best = train_and_compare(
    used_data,
    used_features,
    "resale",
    "used_ev",
    used_categorical
)

tune_random_forest(
    new_data,
    new_features,
    "onroad",
    "new_ev",
    new_categorical
)

tune_random_forest(
    used_data,
    used_features,
    "resale",
    "used_ev",
    used_categorical
)
print("ALL MODEL TRAINING COMPLETED!")

print("New EV best algorithm:", new_best)
print("Used EV best algorithm:", used_best)

print("\nSaved model files:")
print("models/new_ev_best.pkl")
print("models/used_ev_best.pkl")
print("models/new_ev_optimized.pkl")
print("models/used_ev_optimized.pkl")
