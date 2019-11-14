var map;
var ajaxRequest;
var plotlist;
var plotlayers = [];
var marker = L.marker([60, 60]);

map = new L.Map('addMap');

// create the tile layer with correct attribution
var osmUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
var osmAttrib = 'Map data © <a href="https://openstreetmap.org">OpenStreetMap</a> contributors';
var osm = new L.TileLayer(osmUrl, { minZoom: 6, maxZoom: 20, attribution: osmAttrib });

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

map.on('click', onMapClick);

// TODO cache the results, so they can just be switched on and off
function sendObsRequest() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
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
                        observationArray.push(L.marker([observations[i].observation.latitude, observations[i].observation.longitude])
                            .bindPopup("<h4><a target='_blank' href='" + observations[i].animal.info + "'>" + observations[i].animal.name + "<a></h4>"
                                + "<h5> " + observations[i].observation.observ_type + "</h5>"
                                + "<br>Päivämäärä: " + observations[i].observation.date_observed.substring(0, 14)
                                + "<br>Kellonaika: " + observations[i].observation.date_observed.substring(15, 20)
                                + "<br>Kunta: " + observations[i].observation.city
                                + "<br>Paino: " + observations[i].observation.weight
                                + "<br>Sukupuoli: " + observations[i].observation.sex
                                + "<br>Väline: " + observations[i].equipment
                                + "<br>Lisätietoja: " + observations[i].observation.info.substring(0, 20) + infoCutDots, { autoPan: false }));
                    }
                }
                observationLayer = L.layerGroup(observationArray);
                observationOverlay = {
                    "Näytä omat havainnot": observationLayer
                };
                layersControl = L.control.layers(null, observationOverlay, {"collapsed":false});
                layersControl.addTo(map);
            } else {
                alert('An error happened while fetching data for mapping the observations!');
            }
        }
    };
    xhttp.open("POST", "/observations/listuser?page=0", true);
    xhttp.send();
};