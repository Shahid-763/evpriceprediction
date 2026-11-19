
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import os


def generate_city_chart(results):

    cities = [item["city"] for item in results]

    prices = [
        item["predicted_price"] * 100000
        for item in results
    ]

    # Create chart
    plt.figure(figsize=(12, 6))

    bars = plt.bar(cities, prices)

    # Highlight cheapest city
    bars[0].set_color("green")

    plt.title("EV Price Comparison Across Indian Cities")
    plt.xlabel("Cities")
    plt.ylabel("Predicted On-Road Price (₹)")

    plt.xticks(rotation=45)

    plt.ticklabel_format(
        style="plain",
        axis="y"
    )

    plt.tight_layout()

    # Save chart
    os.makedirs("static", exist_ok=True)

    chart_path = "static/city_comparison.png"

    plt.savefig(chart_path, dpi=150)
    plt.close()

    return chart_path
