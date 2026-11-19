
document.addEventListener("DOMContentLoaded", function () {

    // Read prediction type from the URL
    const params = new URLSearchParams(window.location.search);
    const type = params.get("type");

    const pageTitle = document.getElementById("page-title");
    const pageDescription = document.getElementById("page-description");
    const formTitle = document.getElementById("form-title");
    const calculateButton = document.querySelector(".calculate-btn");

    // Default to New EV prediction
    if (type === "used") {

        showForm("used");

        pageTitle.textContent = "Used EV Resale Price Prediction";
        pageDescription.textContent =
            "Enter vehicle age, kilometres driven and battery health to estimate resale value.";

        formTitle.textContent = "Used Electric Vehicle Details";
        calculateButton.textContent = "Calculate Resale Price →";

    } else {

        showForm("new");

        pageTitle.textContent = "New EV Price Prediction";
        pageDescription.textContent =
            "Enter vehicle specifications to estimate the on-road price.";

        formTitle.textContent = "New Electric Vehicle Details";
        calculateButton.textContent = "Calculate On-Road Price →";

    }

});
