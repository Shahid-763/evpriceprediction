
import pandas as pd
import os

os.makedirs("data", exist_ok=True)


variants = pd.read_parquet(
    "data/tco_raw/car/variants.parquet"
)

prices = pd.read_parquet(
    "data/tco_raw/car/prices.parquet"
)


electric_variants = variants[
    variants["fuel_type_name"].eq("Electric")
].copy()


electric_ids = electric_variants[
    "model_source_id"
].dropna().unique()

new_ev = prices[
    prices["model_source_id"].isin(electric_ids)
].copy()

new_ev = new_ev[
    [
        "model_name",
        "variant_name",
        "city_name",
        "ex_showroom_inr",
        "on_road_inr"
    ]
]


new_ev = new_ev.rename(columns={
    "model_name": "model",
    "variant_name": "variant",
    "city_name": "city",
    "ex_showroom_inr": "ex_showroom",
    "on_road_inr": "onroad"
})


new_ev = new_ev.dropna(
    subset=["model", "variant", "city", "ex_showroom", "onroad"]
)

new_ev = new_ev.drop_duplicates()# Save
new_ev.to_csv("data/newPrices.csv", index=False)

used = pd.read_parquet(
    "data/tco_raw/car/used_listings.parquet"
)

used_ev = used[
    used["fuel_type"].eq("Electric")
].copy()

listing_dates = pd.to_datetime(
    used_ev["price_date"], errors="coerce"
)

used_ev["listing_year"] = listing_dates.dt.year
used_ev["listing_year"] = (
    used_ev["listing_year"].fillna(2026)
)

used_ev["age"] = (
    used_ev["listing_year"] - used_ev["model_year"]
).clip(lower=0)

used_ev = used_ev[
    [
        "make",
        "model",
        "variant",
        "city_name",
        "age",
        "km",
        "price_inr"
    ]
]

used_ev = used_ev.rename(columns={
    "make": "brand",
    "city_name": "city",
    "price_inr": "resale"
})

used_ev = used_ev.dropna(
    subset=[
        "brand",
        "model",
        "variant",
        "city",
        "age",
        "km",
        "resale"
    ]
)

used_ev = used_ev.drop_duplicates()

used_ev.to_csv("data/usedPrices.csv", index=False)

print("EV DATA PREPARATION COMPLETED")

print("\nNEW EV DATA:")
print("Records:", len(new_ev))
print("Models:", new_ev["model"].nunique())
print("Variants:", new_ev["variant"].nunique())
print("Cities:", new_ev["city"].nunique())

print("\nUSED EV DATA:")
print("Records:", len(used_ev))
print("Models:", used_ev["model"].nunique())
print("Cities:", used_ev["city"].nunique())

print("\nCSV FILES CREATED:")
print("data/newPrices.csv")
print("data/usedPrices.csv")
