document.addEventListener("DOMContentLoaded", function () {
    const toggleButton = document.getElementById("toggleAnnonce");

    if (toggleButton) {
        const toggleWrapper = toggleButton.nextElementSibling; // Div du toggle
        const toggleCircle = toggleWrapper.querySelector(".toggle-circle");

        function updateToggleUI(isActive) {
            if (isActive) {
                toggleWrapper.classList.remove("bg-gray-300");
                toggleWrapper.classList.add("bg-green-500");
                toggleCircle.classList.add("translate-x-5"); // Déplace le bouton
            } else {
                toggleWrapper.classList.remove("bg-green-500");
                toggleWrapper.classList.add("bg-gray-300");
                toggleCircle.classList.remove("translate-x-5");
            }
        }

        // Initialiser l'état du toggle
        updateToggleUI(toggleButton.checked);

        toggleButton.addEventListener("change", function () {
            const carId = this.dataset.carId;
            console.log("Car ID:", carId);

            fetch(`/users/toggle-annonce/${carId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({})
            })
            .then(response => response.json())
            .then(data => {
                console.log("Réponse du serveur:", data);
                if (data.success) {
                    updateToggleUI(data.is_active);
                } else {
                    alert("Erreur: " + data.message);
                }
            })
            .catch(error => console.error("Erreur :", error));
        });
    }
});

// Fonction pour récupérer le CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
