document.addEventListener("DOMContentLoaded", function () {
    var map = L.map('map').setView([36.75, 3.06], 5);

    // Ajout des tuiles OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    // Ajout d'un marqueur pour Mostaganem
    // L.marker([36.75, 3.06]).addTo(map)
    //     .bindPopup('<b>Mostaganem, Algérie</b><br>Bienvenue ici !')
    //     .openPopup();
});


// Fonction pour filtrer les voitures en fonction de la recherche
document.getElementById("search-location").addEventListener("input", async function () {
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

        li.addEventListener("click", async () => {
            document.getElementById("search-location").value = place.display_name;
            suggestions.innerHTML = "";
        });

        suggestions.appendChild(li);
    });
});