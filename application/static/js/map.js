var map;
var ajaxRequest;
var plotlist;
var plotlayers = [];
var marker = L.marker([60, 60]);
var reset_lat;
var reset_long;

map = new L.Map('addMap');

// create the tile layer with correct attribution
var osmUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
var osmAttrib = 'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors';
var osm = new L.TileLayer(osmUrl, { minZoom: 2, maxZoom: 20, attribution: osmAttrib });

// draw the map
map.setView([60.192, 24.945], 12);
map.addLayer(osm);

document.getElementById("latitude").onchange = onLatLngUpdate;
document.getElementById("longitude").onchange = onLatLngUpdate;

function onLatLngUpdate() {
    document.getElementById("latitude").value = document.getElementById("latitude").value.trim();
    document.getElementById("longitude").value = document.getElementById("longitude").value.trim();
    var lat = document.getElementById("latitude").value;
    var lng = document.getElementById("longitude").value;
    if (lat != "" && lng != "") {
        try {
            lat = parseFloat(lat);
            lng = parseFloat(lng);
            marker.setLatLng([lat, lng]);
            map.addLayer(marker);
        } catch (err) {
            
        }
    }
    if (lat == "" && lng == "") {
        marker.remove();
    }
}

function setMarker(lat, lng) {
    //removeMarkerFromMap()
}

function onMapClick(e) {
    marker.setLatLng(e.latlng);
    map.addLayer(marker);
    document.getElementById("latitude").value = e.latlng.lat.toFixed(6);
    document.getElementById("longitude").value = e.latlng.lng.toFixed(6);

}

function emptyCoordinateSelection() {
    marker.remove();
    document.getElementById("latitude").value = "";
    document.getElementById("longitude").value = "";
}

function revertCoordinates() {
    document.getElementById("latitude").value = reset_lat.toFixed(6);
    document.getElementById("longitude").value = reset_long.toFixed(6);
    map.setView([reset_lat, reset_long], 12);
    marker.setLatLng([reset_lat, reset_long]);
}

map.on('click', onMapClick);

// TODO cache the results, so they can just be switched on and off
function sendObsRequest() {
    var xhttp = new XMLHttpRequest();
    var path = window.location.pathname;
    var obs_id = path.split("/").pop();
    xhttp.onreadystatechange = function() {
        if (obs_id == 'add') {
            fetchObservationsOnAdd(this);
        } else {
            fetchObservationsOnEdit(this, obs_id);
        }
    }
    if (obs_id == 'add') {
        xhttp.open("GET", "/observations/listuser?page=0", true);
    } else {
        var user_id = document.getElementById("acc_id").innerHTML
        xhttp.open("GET", "/observations/list/" + user_id + "?page=0", true);
    }
    xhttp.send();
};

function fetchObservationsOnAdd(xhttp) {
    if (xhttp.readyState === XMLHttpRequest.DONE) {
        if (xhttp.status === 200) {
            var observations = JSON.parse(xhttp.response);
            var observationArray = [];
            for (i = 0; i < observations.length; i++) {
                observation = observations[i]
                var infoCutDots = "";
                if (observation.observation.latitude != "None" && observation.observation.longitude != "None") {
                    if (observation.observation.info != "Ei annettu!" && observation.observation.info.length > 20) {
                        infoCutDots = "...";
                    } else {
                        infoCutDots = "";
                    }
                    observationArray.push(L.marker([observation.observation.latitude, observation.observation.longitude])
                        .bindPopup("<h4><a target='_blank' href='" + observation.animal.info + "'>" + observation.animal.name + "<a></h4>"
                            + "<h5> " + observation.observation.observ_type + "</h5>"
                            + "<br>Päivämäärä: " + observation.observation.date_observed
                            + "<br>Kellonaika: " + observation.observation.time_observed
                            + "<br>Kunta: " + observation.observation.city
                            + "<br>Paino: " + observation.observation.weight
                            + "<br>Sukupuoli: " + observation.observation.sex
                            + "<br>Väline: " + observation.equipment
                            + "<br>Lisätietoja: " + observation.observation.info.substring(0, 20) + infoCutDots, { autoPan: false }));
                }
            }
            observationLayer = L.layerGroup(observationArray);
            observationOverlay = {
                "Näytä muut omat havainnot": observationLayer
            };
            layersControl = L.control.layers(null, observationOverlay, {"collapsed":false});
            layersControl.addTo(map);
        } else {
            alert('An error happened while fetching data for mapping the observations!');
        }
    }
};

function fetchObservationsOnEdit(xhttp, obs_to_edit_id) {
    if (xhttp.readyState === XMLHttpRequest.DONE) {
        if (xhttp.status === 200) {
            var observations = JSON.parse(xhttp.response);
            var observationArray = [];
            for (i = 0; i < observations.length; i++) {
                var infoCutDots = "";
                var observation = observations[i]
                if (observation.observation.latitude != "None" && observation.observation.longitude != "None") {
                    if (observation.observation.info != "Ei annettu!" && observation.observation.info.length > 20) {
                        infoCutDots = "...";
                    } else {
                        infoCutDots = "";
                    }
                    if ( observation.observation.observation_id == obs_to_edit_id) {
                        map.setView([observation.observation.latitude, observation.observation.longitude], 12);
                        reset_lat = parseFloat(observation.observation.latitude );
                        reset_long = parseFloat(observation.observation.longitude);
                        marker.setLatLng([observation.observation.latitude, observation.observation.longitude]);
                        map.addLayer(marker);
                    } else {
                        observationArray.push(L.marker([observation.observation.latitude, observation.observation.longitude])
                            .bindPopup("<h4><a target='_blank' href='" + observation.animal.info + "'>" + observation.animal.name + "<a></h4>"
                                + "<h5> " + observation.observation.observ_type + "</h5>"
                                + "<br>Päivämäärä: " + observation.observation.date_observed
                                + "<br>Kellonaika: " + observation.observation.time_observed
                                + "<br>Kunta: " + observation.observation.city
                                + "<br>Paino: " + observation.observation.weight
                                + "<br>Sukupuoli: " + observation.observation.sex
                                + "<br>Väline: " + observation.equipment
                                + "<br>Lisätietoja: " + observation.observation.info.substring(0, 20) + infoCutDots, { autoPan: false }));
                    }
                }
            }
            observationLayer = L.layerGroup(observationArray);
            observationOverlay = {
                "Näytä käyttäjän muut havainnot": observationLayer
            };
            layersControl = L.control.layers(null, observationOverlay, {"collapsed":false});
            layersControl.addTo(map);
        } else {
            alert('An error happened while fetching data for mapping the observations!');
        }
    }
};