var equipment_field = document.getElementById("equipment")
var equipments;
var catch_equipments = [];
var sighting_equipments = [];
var capture_equipments = [];
var road_accident_equipments = [];
var accident_equipments = [];
var options = [];


document.getElementById("observ_type").onchange = changePossibleEquipment

function fetchEquipments(userId) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (xhttp.readyState === XMLHttpRequest.DONE) {
            if (xhttp.status === 200) {
                equipments = JSON.parse(xhttp.response);
                var i = 0
                while (i < equipments.length) {
                    var name = equipments[i].name;
                    var id = equipments[i].equipment_id;
                    var default_val = false;
                    var selected_val = false;
                    if (id == 1) {
                        default_val = true;
                        selected_val = true;
                    }
                    if (equipments[i].accident_type_allowed) {
                        accident_equipments.push(new Option(name, id, default_val, selected_val));
                    } if (equipments[i].capture_type_allowed) {
                        capture_equipments.push(new Option(name, id, default_val, selected_val));
                    } if (equipments[i].catch_type_allowed) {
                        catch_equipments.push(new Option(name, id, default_val, selected_val));
                    } if (equipments[i].road_accident_type_allowed) {
                        road_accident_equipments.push(new Option(name, id, default_val, selected_val));
                    } if (equipments[i].sighting_type_allowed) {
                        sighting_equipments.push(new Option(name, id, default_val, selected_val));
                    };
                    i = i + 1
                }
                options.push(catch_equipments, sighting_equipments, capture_equipments, road_accident_equipments, accident_equipments)
                changePossibleEquipment()
            };
        };
    };
    xhttp.open("GET", "/equipments/fetchAll?" + Math.round((new Date().getTime()) / (60 * 1000)), true);
    xhttp.send();
};

function changePossibleEquipment() {
    equipment_field.options.length = 0
    var options_to_change = options[document.getElementById('observ_type').value]
    for (var option of options_to_change) {
        equipment_field.options.add(option)
    }
};
