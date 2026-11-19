
import pandas as pd


def compare_used_city_prices(vehicle_brand, vehicle_model, vehicle_variant):

    # Load actual used EV listing dataset
    city_data = pd.read_csv("data/usedPrices.csv")

    # Clean text fields
    text_columns = ["brand", "model", "variant", "city"]

    for column in text_columns:
        city_data[column] = city_data[column].astype(str).str.strip()

    # Match brand, model and variant
    matching_data = city_data[
        (city_data["brand"].str.lower() == vehicle_brand.strip().lower()) &
        (city_data["model"].str.lower() == vehicle_model.strip().lower()) &
        (city_data["variant"].str.lower() == vehicle_variant.strip().lower())
    ].copy()

    if matching_data.empty:
        return {
            "results": [],
            "error": "No used EV listings found for this brand, model and variant."
        }

    # Keep valid listing prices
    matching_data = matching_data.dropna(
        subset=["city", "resale"]
    )

    # Calculate average asking price for each city
    city_prices = (
        matching_data.groupby("city")
        .agg(
            average_listing_price=("resale", "mean"),
            listing_count=("resale", "count")
        )
        .reset_index()
    )

    results = []

    for _, row in city_prices.iterrows():

        results.append({
            "city": row["city"],
            "average_listing_price": round(
                float(row["average_listing_price"]), 2
            ),
            "listing_count": int(row["listing_count"])
        })

    # Sort from highest to lowest asking price
    results.sort(
        key=lambda x: x["average_listing_price"],
        reverse=True
    )

    return {
        "results": results,
        "best_city": results[0]["city"],
        "best_price": results[0]["average_listing_price"],
        "lowest_city": results[-1]["city"],
        "lowest_price": results[-1]["average_listing_price"],
        "comparison_type": "Actual used EV advertised listing prices"
    }
