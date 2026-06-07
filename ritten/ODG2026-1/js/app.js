let map;
let userMarker;
let waypointMarker;

let route = [];
let roadbook = [];
let track = [];

let current = 0;
let lastPosition;

Promise.all([
    fetch("route.json").then(r => r.json()),
    fetch("roadbook.json").then(r => r.json()),
    fetch("track.json").then(r => r.json())
])
.then(([routeData, roadbookData, trackData]) => {

    route = routeData;
    roadbook = roadbookData;
    track = trackData;

    map = L.map('map').setView(
        [route[0].lat, route[0].lon],
        13
    );

    L.tileLayer(
        'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
        {
            maxZoom: 19
        }
    ).addTo(map);

    const routeLine = L.polyline(
        track,
        {
            weight: 4
        }
    ).addTo(map);

    map.fitBounds(routeLine.getBounds());

    showWaypoint();

    navigator.geolocation.getCurrentPosition(
        pos => {

            document.getElementById("gps").textContent =
                "GPS OK";

            updatePosition(pos);

        },
        err => {

            document.getElementById("gps").textContent =
                "GPS fout: " + err.message;

        }
    );

    navigator.geolocation.watchPosition(
        updatePosition,
        err => {
            document.getElementById("gps").textContent =
                "GPS fout: " + err.message;
        },
        {
            enableHighAccuracy: true
        }
    );
});

function showWaypoint() {

    document.getElementById("wp").textContent =
        `WP ${current + 1} / ${route.length}`;

    const rb = roadbook[current];

    document.getElementById("info").textContent =
        rb?.info || "";

    document.getElementById("symbol").src =
        `symbols/${String(current + 1).padStart(3, "0")}.png`;

    if (waypointMarker) {
        map.removeLayer(waypointMarker);
    }

    waypointMarker = L.marker([
        route[current].lat,
        route[current].lon
    ]).addTo(map);

    map.panTo([
        route[current].lat,
        route[current].lon
    ]);
}

function nextWaypoint() {

    if (current < route.length - 1) {

        current++;

        showWaypoint();

        if (lastPosition) {
            calculateDistance(lastPosition);
        }
    }
}

function updatePosition(pos) {

    lastPosition = pos;

    let lat = pos.coords.latitude;
    let lon = pos.coords.longitude;

    let wp = route[current];

    let distance =
        getDistance(
            lat,
            lon,
            wp.lat,
            wp.lon
        );

    if (!userMarker) {

        userMarker = L.marker([
            lat,
            lon
        ]).addTo(map);

    } else {

        userMarker.setLatLng([
            lat,
            lon
        ]);
    }

    document.getElementById("distance").textContent =
        Math.round(distance) + " m";

    document.getElementById("gps").textContent =
        `GPS nauwkeurigheid: ${Math.round(pos.coords.accuracy)} m`;

    if (distance < 30) {

        if (current < route.length - 1) {

            current++;

            showWaypoint();

            navigator.vibrate?.(200);
        }
    }
}

function getDistance(lat1, lon1, lat2, lon2) {

    const R = 6371000;

    const dLat =
        (lat2 - lat1) * Math.PI / 180;

    const dLon =
        (lon2 - lon1) * Math.PI / 180;

    const a =
        Math.sin(dLat / 2) ** 2 +
        Math.cos(lat1 * Math.PI / 180) *
        Math.cos(lat2 * Math.PI / 180) *
        Math.sin(dLon / 2) ** 2;

    return R * 2 *
        Math.atan2(
            Math.sqrt(a),
            Math.sqrt(1 - a)
        );
}

function calculateDistance(pos) {

    let lat = pos.coords.latitude;
    let lon = pos.coords.longitude;

    let wp = route[current];

    let distance =
        getDistance(
            lat,
            lon,
            wp.lat,
            wp.lon
        );

    document.getElementById("distance").textContent =
        Math.round(distance) + " m";
}