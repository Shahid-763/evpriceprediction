
const modelSelect = document.getElementById("compare-model");
const variantSelect = document.getElementById("compare-variant");
const result = document.getElementById("comparison-result");
async function loadNewOptions(params = {}) {

    const query = new URLSearchParams(params);

    const response = await fetch(
        `/api/new-options?${query.toString()}`
    );

    if (!response.ok) {
        throw new Error("Unable to load vehicle options.");
    }

    const data = await response.json();

    return data.options || [];
}
function populateDropdown(select, options, placeholder) {

    select.innerHTML = "";

    const defaultOption = document.createElement("option");
    defaultOption.value = "";
    defaultOption.textContent = placeholder;

    select.appendChild(defaultOption);

    options.forEach(value => {

        const option = document.createElement("option");

        option.value = value;
        option.textContent = value;

        select.appendChild(option);

    });

    select.disabled = options.length === 0;
}

async function initializeDropdowns() {

    try {

        const models = await loadNewOptions();

        populateDropdown(
            modelSelect,
            models,
            "Select Vehicle Model"
        );

    } catch (error) {

        console.error(error);

        populateDropdown(
            modelSelect,
            [],
            "Unable to load models"
        );

        result.innerText = error.message;

    }
}
modelSelect.addEventListener("change", async function() {

    const model = this.value;

    populateDropdown(
        variantSelect,
        [],
        "Loading variants..."
    );

    result.innerHTML = "";

    if (!model) {

        populateDropdown(
            variantSelect,
            [],
            "Select a model first"
        );

        return;
    }

    try {

        const variants = await loadNewOptions({ model });

        populateDropdown(
            variantSelect,
            variants,
            "Select Vehicle Variant"
        );

    } catch (error) {

        result.innerText = error.message;

    }

});
document.getElementById("comparison-form").addEventListener(
    "submit",
    async function(event) {

        event.preventDefault();

        const inputData = {
            model: modelSelect.value,
            variant: variantSelect.value
        };

        result.innerText = "Comparing actual city-wise prices...";

        try {

            const response = await fetch("/compare/cities", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(inputData)
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "Comparison failed");
            }

            if (!data.results || data.results.length === 0) {
                throw new Error("No city price records found.");
            }

            const formatPrice = price =>
                "₹" + Number(price).toLocaleString("en-IN", {
                    maximumFractionDigits: 0
                });

            let html = `
                <h2>Actual City-wise Price Results</h2>

                <h3>Cheapest City: ${data.cheapest_city}</h3>

                <h3>Price: ${formatPrice(data.cheapest_price)}</h3>

                <p>
                    Maximum price difference:
                    <strong>${formatPrice(data.price_difference)}</strong>
                </p>

                <p><strong>Source:</strong> ${data.comparison_type}</p>

                <table border="1" cellpadding="10">
                    <tr>
                        <th>Rank</th>
                        <th>City</th>
                        <th>Actual On-Road Price</th>
                    </tr>
            `;

            data.results.forEach((item, index) => {

                html += `
                    <tr>
                        <td>${index + 1}</td>
                        <td>${item.city}</td>
                        <td>${formatPrice(item.predicted_price)}</td>
                    </tr>
                `;

            });

            html += "</table>";

            if (data.chart_url) {

                html += `
                    <h2>City Price Comparison Chart</h2>

                    <img
                        src="${data.chart_url}?t=${Date.now()}"
                        alt="EV price comparison across cities"
                        style="max-width:100%; height:auto;"
                    >
                `;

            }

            result.innerHTML = html;

        } catch (error) {

            console.error("City comparison error:", error);
            result.innerText = "Error: " + error.message;

        }
    }
);

initializeDropdowns();
