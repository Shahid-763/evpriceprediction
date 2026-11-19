
document.getElementById("used-comparison-form").addEventListener(
    "submit",
    async function(event) {

        event.preventDefault();

        const result = document.getElementById(
            "used-comparison-result"
        );

        const inputData = {
            brand: document.getElementById("used-brand").value.trim(),
            model: document.getElementById("used-model").value.trim(),
            variant: document.getElementById("used-variant").value.trim()
        };

        result.innerText = "Comparing actual used EV listing prices...";

        try {

            const response = await fetch("/compare/used-cities", {
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
                throw new Error("No used EV listings found.");
            }

            const formatPrice = price =>
                "₹" + Number(price).toLocaleString("en-IN", {
                    maximumFractionDigits: 0
                });

            const maxPrice = Math.max(
                ...data.results.map(item => item.average_listing_price)
            );

            let html = `
                <h2>Used EV City-wise Listing Results</h2>

                <h3>Highest Asking Price City: ${data.best_city}</h3>
                <h3>Average Asking Price: ${formatPrice(data.best_price)}</h3>

                <h3>Lowest Asking Price City: ${data.lowest_city}</h3>
                <h3>Average Asking Price: ${formatPrice(data.lowest_price)}</h3>

                <p><strong>Source:</strong> ${data.comparison_type}</p>

                <h2>City-wise Listing Price Chart</h2>
            `;

            data.results.forEach(item => {

                const percentage = maxPrice > 0
                    ? (item.average_listing_price / maxPrice) * 100
                    : 0;

                html += `
                    <div style="margin:15px 0;">

                        <strong>${item.city}</strong>

                        <span style="float:right;">
                            ${formatPrice(item.average_listing_price)}
                        </span>

                        <div style="
                            background:#e5e7eb;
                            height:20px;
                            border-radius:5px;
                            overflow:hidden;
                            margin-top:5px;
                        ">
                            <div style="
                                background:#16a34a;
                                width:${percentage}%;
                                height:20px;
                            "></div>
                        </div>

                        <small>
                            ${item.listing_count} listing(s)
                        </small>

                    </div>
                `;
            });

            html += `
                <h2>City-wise Ranking</h2>

                <table border="1" cellpadding="10"
                       style="width:100%; border-collapse:collapse;">

                    <tr>
                        <th>Rank</th>
                        <th>City</th>
                        <th>Average Asking Price</th>
                        <th>Number of Listings</th>
                    </tr>
            `;

            data.results.forEach((item, index) => {

                html += `
                    <tr>
                        <td>${index + 1}</td>
                        <td>${item.city}</td>
                        <td>${formatPrice(item.average_listing_price)}</td>
                        <td>${item.listing_count}</td>
                    </tr>
                `;
            });

            html += "</table>";

            result.innerHTML = html;

        } catch (error) {

            console.error("Used city comparison error:", error);
            result.innerText = "Error: " + error.message;

        }
    }
);
