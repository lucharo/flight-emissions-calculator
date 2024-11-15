function getSuggestions(inputId) {
    let inputElem = document.getElementById(inputId);
    let suggestionElem = document.getElementById(inputId + "-suggestions");
    let query = inputElem.value;

    if (query.length > 1) {
        // Fetching suggestions from Flask
        fetch(`/suggest?q=${query}`)
            .then(response => response.json())
            .then(data => {
                // Clear previous suggestions
                suggestionElem.innerHTML = '';

                // Populate suggestions
                for (let entry of data.suggestions) {
                    let pElem = document.createElement('p');
                    pElem.textContent = `${entry.name} (${entry.city}, ${entry.country})`;
                    pElem.onclick = function() {
                        inputElem.value = pElem.textContent;
                        suggestionElem.style.display = 'none';  // Hide suggestions after selecting one
                    };
                    suggestionElem.appendChild(pElem);
                }

                // Show suggestion container if there are suggestions
                suggestionElem.style.display = data.suggestions.length > 0 ? 'block' : 'none';
            });
    } else {
        suggestionElem.style.display = 'none';  // Hide suggestions if the query is too short
    }
}

let map;

function initMap() {
    // Initialize the map
    map = L.map('globe').setView([51.505, -0.09], 13);

    // Add a tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
}

initMap();

function fetchAirportCoordinates(query) {
    return fetch(`/get-coordinates?q=${query}`)
        .then(response => response.json())
        .then(data => {
            return [data.latitude, data.longitude];
        });
}

async function drawCurvedLine() {
    let origin = document.getElementById('origin').value;
    let destination = document.getElementById('destination').value;

    let originCoords = await fetchAirportCoordinates(origin);
    let destinationCoords = await fetchAirportCoordinates(destination);

    // Draw a curved line
    let curvedPath = L.curve(
        [
            'M', originCoords,
            'Q', [originCoords[0], destinationCoords[1]], destinationCoords
        ], 
        {
            color: 'blue',
            weight: 4
        }
    ).addTo(map);
}

document.getElementById('calculate-emissions').addEventListener('click', drawCurvedLine);




