
import pandas as pd


def compare_city_prices(vehicle_model, vehicle_variant):

    # Load actual new EV price dataset
    city_data = pd.read_csv("data/newPrices.csv")

    # Clean text fields
    city_data["model"] = city_data["model"].astype(str).str.strip()
    city_data["variant"] = city_data["variant"].astype(str).str.strip()
    city_data["city"] = city_data["city"].astype(str).str.strip()

    # Match selected model and variant
    matching_data = city_data[
        (city_data["model"].str.lower() == vehicle_model.strip().lower()) &
        (city_data["variant"].str.lower() == vehicle_variant.strip().lower())
    ].copy()

    if matching_data.empty:
        return {
            "results": [],
            "error": "No city-wise price records found for this model and variant."
        }

    # Keep actual city-wise on-road prices
    matching_data = matching_data.dropna(
        subset=["city", "onroad"]
    )

    # Average prices if multiple records exist for the same city
    city_prices = (
        matching_data.groupby("city")["onroad"]
        .mean()
        .reset_index()
    )

    results = []

    for _, row in city_prices.iterrows():

        results.append({
            "city": row["city"],
            "predicted_price": round(float(row["onroad"]), 2)
        })

    # Sort from cheapest to most expensive
    results.sort(key=lambda x: x["predicted_price"])

    return {
        "results": results,
        "cheapest_city": results[0]["city"],
        "cheapest_price": results[0]["predicted_price"],
        "price_difference": round(
            results[-1]["predicted_price"] - results[0]["predicted_price"], 2
        ),
        "comparison_type": "Actual recorded on-road prices"
    }
