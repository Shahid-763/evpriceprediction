
from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib

from utils.city_comparison import compare_city_prices
from utils.city_chart import generate_city_chart
from utils.used_city_comparison import compare_used_city_prices


app = Flask(__name__)

new_model = joblib.load("models/new_ev_optimized.pkl")
used_model = joblib.load("models/used_ev_optimized.pkl")

new_data = pd.read_csv("data/newPrices.csv")
used_data = pd.read_csv("data/usedPrices.csv")

for column in ["model", "variant", "city"]:
    new_data[column] = new_data[column].astype(str).str.strip()

for column in ["brand", "model", "variant", "city"]:
    used_data[column] = used_data[column].astype(str).str.strip()


def get_options(data, column, filters=None):

    filtered_data = data.copy()

    if filters:
        for field, value in filters.items():

            if value:
                filtered_data = filtered_data[
                    filtered_data[field].str.lower() == value.lower()
                ]

    options = (
        filtered_data[column]
        .dropna()
        .unique()
        .tolist()
    )

    options = [
        value for value in options
        if value and value.lower() != "nan"
    ]

    return sorted(options, key=str.lower)

@app.route("/api/new-options")
def new_options():

    model = request.args.get("model", "").strip()
    variant = request.args.get("variant", "").strip()

    if not model:

        return jsonify({
            "options": get_options(new_data, "model")
        })

    if not variant:

        return jsonify({
            "options": get_options(
                new_data,
                "variant",
                {"model": model}
            )
        })

    return jsonify({
        "options": get_options(
            new_data,
            "city",
            {
                "model": model,
                "variant": variant
            }
        )
    })

@app.route("/api/used-options")
def used_options():

    brand = request.args.get("brand", "").strip()
    model = request.args.get("model", "").strip()
    variant = request.args.get("variant", "").strip()

    if not brand:

        return jsonify({
            "options": get_options(used_data, "brand")
        })

    if not model:

        return jsonify({
            "options": get_options(
                used_data,
                "model",
                {"brand": brand}
            )
        })

    if not variant:

        return jsonify({
            "options": get_options(
                used_data,
                "variant",
                {
                    "brand": brand,
                    "model": model
                }
            )
        })

    return jsonify({
        "options": get_options(
            used_data,
            "city",
            {
                "brand": brand,
                "model": model,
                "variant": variant
            }
        )
    })

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/prediction")
def prediction_page():
    return render_template("prediction.html")


@app.route("/predict/new", methods=["POST"])
def predict_new():

    try:
        data = request.get_json()

        required_fields = [
            "model", "variant", "city", "ex_showroom"
        ]

        for field in required_fields:
            if field not in data or str(data[field]).strip() == "":
                return jsonify({
                    "error": f"Missing required field: {field}"
                }), 400

        input_data = pd.DataFrame([{
            "model": str(data["model"]).strip(),
            "variant": str(data["variant"]).strip(),
            "city": str(data["city"]).strip(),
            "ex_showroom": float(data["ex_showroom"])
        }])

        if input_data["ex_showroom"].iloc[0] <= 0:
            return jsonify({
                "error": "Ex-showroom price must be greater than zero."
            }), 400

        prediction = new_model.predict(input_data)[0]

        return jsonify({
            "predicted_price": round(float(prediction), 2)
        })

    except (ValueError, TypeError):
        return jsonify({
            "error": "Please enter valid numerical values."
        }), 400

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500
@app.route("/predict/used", methods=["POST"])
def predict_used():

    try:
        data = request.get_json()

        required_fields = [
            "brand", "model", "variant", "city", "age", "km"
        ]

        for field in required_fields:
            if field not in data or str(data[field]).strip() == "":
                return jsonify({
                    "error": f"Missing required field: {field}"
                }), 400

        age = float(data["age"])
        km = float(data["km"])

        if age < 0 or km < 0:
            return jsonify({
                "error": "Age and kilometres cannot be negative."
            }), 400

        input_data = pd.DataFrame([{
            "brand": str(data["brand"]).strip(),
            "model": str(data["model"]).strip(),
            "variant": str(data["variant"]).strip(),
            "city": str(data["city"]).strip(),
            "age": age,
            "km": km
        }])

        prediction = used_model.predict(input_data)[0]

        return jsonify({
            "predicted_resale_price": round(float(prediction), 2)
        })

    except (ValueError, TypeError):
        return jsonify({
            "error": "Please enter valid numerical values."
        }), 400

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

@app.route("/compare/cities", methods=["POST"])
def compare_cities():

    try:
        data = request.get_json()

        comparison = compare_city_prices(
            vehicle_model=data["model"],
            vehicle_variant=data["variant"]
        )

        if comparison.get("error"):
            return jsonify(comparison), 404

        chart_path = generate_city_chart(comparison["results"])

        comparison["chart_url"] = "/" + chart_path.replace("\\", "/")

        return jsonify(comparison)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

@app.route("/compare/used-cities", methods=["POST"])
def compare_used_cities():

    try:
        data = request.get_json()

        comparison = compare_used_city_prices(
            vehicle_brand=data["brand"],
            vehicle_model=data["model"],
            vehicle_variant=data["variant"]
        )

        if comparison.get("error"):
            return jsonify(comparison), 404

        return jsonify(comparison)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


@app.route("/city-comparison")
def city_comparison_page():
    return render_template("city_comparison.html")

@app.route("/used-city-comparison")
def used_city_comparison_page():
    return render_template("used_city_comparison.html")

if __name__ == "__main__":
    app.run(debug=True)
