
let selectedType = "";


// ----------------------------------
// Common dropdown functions
// ----------------------------------

async function loadOptions(api, params = {}) {

    const query = new URLSearchParams(params);

    const response = await fetch(`${api}?${query.toString()}`);

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


// ----------------------------------
// New EV dropdown initialization
// ----------------------------------

async function initializeNewDropdowns() {

    const model = document.getElementById("new-model");
    const variant = document.getElementById("new-variant");
    const city = document.getElementById("new-city");

    try {

        const models = await loadOptions("/api/new-options");

        populateDropdown(
            model,
            models,
            "Select Vehicle Model"
        );

    } catch (error) {

        console.error("New EV dropdown error:", error);

        populateDropdown(model, [], "Unable to load models");
    }


    // Model selection
    model.addEventListener("change", async function() {

        populateDropdown(variant, [], "Loading variants...");

        populateDropdown(city, [], "Select a variant first");

        if (!this.value) {
            populateDropdown(variant, [], "Select a model first");
            return;
        }

        try {

            const variants = await loadOptions(
                "/api/new-options",
                { model: this.value }
            );

            populateDropdown(
                variant,
                variants,
                "Select Vehicle Variant"
            );

        } catch (error) {

            console.error(error);
        }
    });


    // Variant selection
    variant.addEventListener("change", async function() {

        populateDropdown(city, [], "Loading cities...");

        if (!this.value) {
            populateDropdown(city, [], "Select a variant first");
            return;
        }

        try {

            const cities = await loadOptions(
                "/api/new-options",
                {
                    model: model.value,
                    variant: this.value
                }
            );

            populateDropdown(
                city,
                cities,
                "Select City"
            );

        } catch (error) {

            console.error(error);
        }
    });
}


// ----------------------------------
// Used EV dropdown initialization
// ----------------------------------

async function initializeUsedDropdowns() {

    const brand = document.getElementById("used-brand");
    const model = document.getElementById("used-model");
    const variant = document.getElementById("used-variant");
    const city = document.getElementById("used-city");

    try {

        const brands = await loadOptions("/api/used-options");

        populateDropdown(
            brand,
            brands,
            "Select Vehicle Brand"
        );

    } catch (error) {

        console.error("Used EV dropdown error:", error);

        populateDropdown(brand, [], "Unable to load brands");
    }


    // Brand selection
    brand.addEventListener("change", async function() {

        populateDropdown(model, [], "Loading models...");
        populateDropdown(variant, [], "Select a model first");
        populateDropdown(city, [], "Select a variant first");

        if (!this.value) {
            populateDropdown(model, [], "Select a brand first");
            return;
        }

        try {

            const models = await loadOptions(
                "/api/used-options",
                { brand: this.value }
            );

            populateDropdown(
                model,
                models,
                "Select Vehicle Model"
            );

        } catch (error) {

            console.error(error);
        }
    });


    // Model selection
    model.addEventListener("change", async function() {

        populateDropdown(variant, [], "Loading variants...");
        populateDropdown(city, [], "Select a variant first");

        if (!this.value) {
            populateDropdown(variant, [], "Select a model first");
            return;
        }

        try {

            const variants = await loadOptions(
                "/api/used-options",
                {
                    brand: brand.value,
                    model: this.value
                }
            );

            populateDropdown(
                variant,
                variants,
                "Select Vehicle Variant"
            );

        } catch (error) {

            console.error(error);
        }
    });


    // Variant selection
    variant.addEventListener("change", async function() {

        populateDropdown(city, [], "Loading cities...");

        if (!this.value) {
            populateDropdown(city, [], "Select a variant first");
            return;
        }

        try {

            const cities = await loadOptions(
                "/api/used-options",
                {
                    brand: brand.value,
                    model: model.value,
                    variant: this.value
                }
            );

            populateDropdown(
                city,
                cities,
                "Select City"
            );

        } catch (error) {

            console.error(error);
        }
    });
}


// ----------------------------------
// Show correct prediction form
// ----------------------------------

function showForm(type) {

    selectedType = type;

    const newFields = document.getElementById("new-fields");
    const usedFields = document.getElementById("used-fields");

    const newInputs = [
        "new-model",
        "new-variant",
        "new-city",
        "ex_showroom"
    ];

    const usedInputs = [
        "used-brand",
        "used-model",
        "used-variant",
        "used-city",
        "age",
        "km"
    ];

    const setRequired = (ids, required) => {

        ids.forEach(id => {
            document.getElementById(id).required = required;
        });
    };

    document.getElementById("prediction-form").style.display = "block";

    document.getElementById("result").innerHTML = "";

    if (type === "new") {

        newFields.style.display = "block";
        usedFields.style.display = "none";

        setRequired(newInputs, true);
        setRequired(usedInputs, false);

        document.getElementById("form-title").innerText =
            "New EV Price Prediction";

    } else {

        newFields.style.display = "none";
        usedFields.style.display = "block";

        setRequired(newInputs, false);
        setRequired(usedInputs, true);

        document.getElementById("form-title").innerText =
            "Used EV Resale Price Prediction";
    }
}


// ----------------------------------
// Format price in Indian Rupees
// ----------------------------------

function formatPrice(priceInRupees) {

    return "₹" + Number(priceInRupees).toLocaleString("en-IN", {
        maximumFractionDigits: 0
    });
}


// ----------------------------------
// Initialize prediction page
// ----------------------------------

document.addEventListener("DOMContentLoaded", async function() {

    const params = new URLSearchParams(window.location.search);

    const type = params.get("type");

    const form = document.getElementById("ev-form");

    if (!form) return;

    if (type !== "new" && type !== "used") {

        document.getElementById("page-description").innerText =
            "Please select New EV or Used EV prediction from the dashboard.";

        return;
    }

    showForm(type);


    // Page headings
    if (type === "new") {

        document.getElementById("page-title").innerText =
            "New EV Price Prediction";

        document.getElementById("page-description").innerText =
            "Select your vehicle and enter its ex-showroom price to estimate the on-road price.";

        document.querySelector(".calculate-btn").innerText =
            "Calculate On-Road Price →";

        await initializeNewDropdowns();

    } else {

        document.getElementById("page-title").innerText =
            "Used EV Resale Price Prediction";

        document.getElementById("page-description").innerText =
            "Select your vehicle and enter its age and kilometres driven to estimate its used listing value.";

        document.querySelector(".calculate-btn").innerText =
            "Calculate Used EV Price →";

        await initializeUsedDropdowns();
    }


    // ----------------------------------
    // Prediction form submission
    // ----------------------------------

    form.addEventListener("submit", async function(event) {

        event.preventDefault();

        const result = document.getElementById("result");
        const calculateButton = document.querySelector(".calculate-btn");

        let url = "";
        let inputData = {};

        if (selectedType === "new") {

            url = "/predict/new";

            inputData = {
                model: document.getElementById("new-model").value,
                variant: document.getElementById("new-variant").value,
                city: document.getElementById("new-city").value,
                ex_showroom: document.getElementById("ex_showroom").value
            };

        } else {

            url = "/predict/used";

            inputData = {
                brand: document.getElementById("used-brand").value,
                model: document.getElementById("used-model").value,
                variant: document.getElementById("used-variant").value,
                city: document.getElementById("used-city").value,
                age: document.getElementById("age").value,
                km: document.getElementById("km").value
            };
        }

        result.innerText = "Calculating price...";

        calculateButton.disabled = true;

        try {

            const response = await fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(inputData)
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "Prediction failed");
            }

            if (selectedType === "new") {

                result.innerText =
                    "Predicted On-Road Price: " +
                    formatPrice(data.predicted_price);

            } else {

                result.innerText =
                    "Estimated Used EV Listing Value: " +
                    formatPrice(data.predicted_resale_price);
            }

        } catch (error) {

            console.error("Prediction error:", error);

            result.innerText = "Error: " + error.message;

        } finally {

            calculateButton.disabled = false;
        }
    });

});
