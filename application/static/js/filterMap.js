var map;
var ajaxRequest;
var plotlist;
var plotlayers = [];

map = new L.Map('filterMap');

// create the tile layer with correct attribution
var osmUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
var osmAttrib = 'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors';
var osm = new L.TileLayer(osmUrl, { minZoom: 2, maxZoom: 20, attribution: osmAttrib });

// draw the map
map.setView([60.192, 24.945], 12);
map.addLayer(osm);

document.getElementById("latitude_low").onchange = onLatLngUpdate;
document.getElementById("latitude_high").onchange = onLatLngUpdate;
document.getElementById("longitude_low").onchange = onLatLngUpdate;
document.getElementById("longitude_high").onchange = onLatLngUpdate;

function onLatLngUpdate() {
    document.getElementById("latitude_low").value = document.getElementById("latitude_low").value.trim();
    document.getElementById("latitude_high").value = document.getElementById("latitude_high").value.trim();
    document.getElementById("longitude_low").value = document.getElementById("longitude_low").value.trim();
    document.getElementById("longitude_high").value = document.getElementById("longitude_high").value.trim();
    var latLow = document.getElementById("latitude_low").value;
    var latHigh = document.getElementById("latitude_high").value;
    var lngLow = document.getElementById("longitude_low").value;
    var lngHigh = document.getElementById("longitude_high").value;
    if (lat != "" && lng != "") {
        try {
            latLow = parseFloat(latLow);
            latHigh = parseFloat(latHigh);
            lngLow = parseFloat(lngLow);
            lngHigh = parseFloat(lngHigh);
            // try add the rectangle
        } catch (err) {

        }
    }
    if (lat == "" && lng == "") {
        marker.remove();
    }
}

function onMapClick(e) {
}

function emptyCoordinateSelection() {
    // document.getElementById("latitude").value = "";
    // document.getElementById("longitude").value = "";
}

map.on('click', onMapClick);


function sendObsRequest(userId) {
    var xhttp = new XMLHttpRequest();
    var form = document.getElementById("filterForm")
    var FD = new FormData(form);
    xhttp.onreadystatechange = function () {
        if (xhttp.readyState === XMLHttpRequest.DONE) {
            if (xhttp.status === 200) {
                var observations = JSON.parse(xhttp.response);
                var observationArray = [];
                for (i = 0; i < observations.length; i++) {
                    var infoCutDots = "";
                    if (observations[i].observation.latitude != "None" && observations[i].observation.longitude != "None") {
                        if (observations[i].observation.info != "Ei annettu!" && observations[i].observation.info.length > 20) {
                            infoCutDots = "...";
                        } else {
                            infoCutDots = "";
                        }
                        if (userId >= -1) {
                            observationArray.push(L.marker([observations[i].observation.latitude, observations[i].observation.longitude])
                                .bindPopup("<h4><a target='_blank' href='" + observations[i].animal.info + "'>" + observations[i].animal.name + "<a></h4>"
                                    + "<h5> " + observations[i].observation.observ_type + "</h5>"
                                    + "<br>Päivämäärä: " + observations[i].observation.date_observed
                                    + "<br>Kellonaika: " + observations[i].observation.time_observed
                                    + "<br>Kunta: " + observations[i].observation.city
                                    + "<br>Paino: " + observations[i].observation.weight
                                    + "<br>Sukupuoli: " + observations[i].observation.sex
                                    + "<br>Väline: " + observations[i].equipment
                                    + "<br>Lisätietoja: " + observations[i].observation.info.substring(0, 20) + infoCutDots, { autoPan: false }));
                        } else if (userId == -2) {
                            observationArray.push(L.marker([observations[i].observation.latitude, observations[i].observation.longitude])
                                .bindPopup("<h4><a target='_blank' href='" + observations[i].animal.info + "'>" + observations[i].animal.name + "<a></h4>"
                                    + "<h5> " + observations[i].observation.observ_type + "</h5>"
                                    + "<h5>Käyttäjä: <a href='/observations/list/" + observations[i].observer_id + "'>" + observations[i].observer + "</a></h5>"
                                    + "<br>Päivämäärä: " + observations[i].observation.date_observed
                                    + "<br>Kellonaika: " + observations[i].observation.time_observed
                                    + "<br>Kunta: " + observations[i].observation.city
                                    + "<br>Paino: " + observations[i].observation.weight
                                    + "<br>Sukupuoli: " + observations[i].observation.sex
                                    + "<br>Väline: " + observations[i].equipment
                                    + "<br>Lisätietoja: " + observations[i].observation.info.substring(0, 20) + infoCutDots, { autoPan: false }));
                        }
                    }
                }
                var observationLayer = L.layerGroup(observationArray);
                observationLayer.addTo(map);
            } else {
                alert('An error happened while fetching data for mapping the observations!');
            }
        }
    };
    // Adding timestamp to the end to disable caching of results
    if (userId == -1) {
        xhttp.open("POST", "/observations/list/user?page=0&" + (new Date().getTime()), true);
    } else if (userId == -2) {
        xhttp.open("POST", "/observations/list/all?page=0&" + (new Date().getTime()), true);
    } else {
        xhttp.open("POST", "/observations/list/"+ userId +"?page=0&" + (new Date().getTime()), true);
    }
    xhttp.send(FD);
};