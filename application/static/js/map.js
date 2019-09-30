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
    //removeMarkerFromMap()
    //marker = L.marker(e.latlng);
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
