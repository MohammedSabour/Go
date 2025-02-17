// Gestion du dropdown
function toggleDropdown() {
    const dropdown = document.getElementById('dropdown');
    dropdown.classList.toggle('hidden');
}

// Close dropdown when clicking outside
document.addEventListener('click', function(event) {
    const dropdown = document.getElementById('dropdown');
    const button = event.target.closest('button');
    if (!button && !dropdown.classList.contains('hidden')) {
        dropdown.classList.add('hidden');
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const startDateInput = document.querySelector('input[name="start_date"]');
    const endDateInput = document.querySelector('input[name="end_date"]');

    if (startDateInput && endDateInput) {
        const today = new Date();
        const startDate = new Date(today);
        startDate.setDate(today.getDate() + 1);
        
        const endDate = new Date(startDate);
        endDate.setDate(startDate.getDate() + 3);

        const formatDate = (date) => date.toISOString().split("T")[0];

        startDateInput.value = formatDate(startDate);
        endDateInput.value = formatDate(endDate);
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const locationInput = document.getElementById("locationCar");
    
    if (!locationInput) {
        console.error("L'élément #locationCar n'existe pas !");
        return;
    }

    locationInput.addEventListener("input", async function () {
        const query = this.value;
        if (query.length < 3) return;

        const response = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${query}`);
        const results = await response.json();

        const suggestions = document.getElementById("suggestions");
        suggestions.innerHTML = "";

        results.forEach((place) => {
            const li = document.createElement("li");
            li.textContent = place.display_name;
            li.classList.add("p-2", "cursor-pointer", "hover:bg-gray-200");

            li.addEventListener("click", () => {
                document.getElementById("locationCar").value = place.display_name;
                document.getElementById("latitude").value = place.lat;
                document.getElementById("longitude").value = place.lon;
                suggestions.innerHTML = "";
            });

            suggestions.appendChild(li);
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const priceRange = document.getElementById("priceRange");
    const priceValue = document.getElementById("priceValue");

    // Mettre à jour la valeur affichée quand l'utilisateur bouge le curseur
    priceRange.addEventListener("input", function () {
        priceValue.textContent = priceRange.value;
    });
});