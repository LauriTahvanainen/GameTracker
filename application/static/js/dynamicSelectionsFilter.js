var equipment_field = document.getElementById("equipment")
var equipments;
var catch_equipments = [];
var sighting_equipments = [];
var capture_equipments = [];
var road_accident_equipments = [];
var accident_equipments = [];
var all_equipments = [];
var options = [];

document.getElementById("observ_type").onchange = changePossibleEquipmentFilterForm;

function fetchEquipments(user_id) {
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
                    var option = {name: name, id: id, default_val: default_val, selected_val: selected_val}
                    if (equipments[i].accident_type_allowed) {
                        accident_equipments.push(option);
                    } if (equipments[i].capture_type_allowed) {
                        capture_equipments.push(option);
                    } if (equipments[i].catch_type_allowed) {
                        catch_equipments.push(option);
                    } if (equipments[i].road_accident_type_allowed) {
                        road_accident_equipments.push(option);
                    } if (equipments[i].sighting_type_allowed) {
                        sighting_equipments.push(option);
                    };
                    all_equipments.push(option);
                    i = i + 1;
                };
                options.push(catch_equipments, sighting_equipments, capture_equipments, road_accident_equipments, accident_equipments);
                changePossibleEquipmentFilterForm();
            };
        };
    };
    if (user_id >= 0) {
        xhttp.open("GET", "/equipments/fetchUser/" + user_id + "?" + Math.round((new Date().getTime()) / (60 * 1000)), true);
    } else if (user_id == -1) {
        xhttp.open("GET", "/equipments/fetchCurrentUser?" + Math.round((new Date().getTime()) / (60 * 1000)), true);
    } else {
        xhttp.open("GET", "/equipments/fetchAll?" + Math.round((new Date().getTime()) / (60 * 1000)), true);
    };
    xhttp.send();
};

function changePossibleEquipmentFilterForm() {
    equipment_field.options.length = 0;
    var list_of_option_lists = [];
    // Select the lists of options to show by observation type
    for (option of document.getElementById('observ_type').options) {
        if (option.selected) {
            list_of_option_lists.push(options[option.value]);
        };
    };
    // Fill in the options to use from the lists of options
    if (list_of_option_lists.length == 0) {
        fillOptionsWithAllEquipments();
    } else {
        //HTMLOptionsCollection acts like a set
        options_set = new Set()
        for (var equip_options of list_of_option_lists) {
            for (var option of equip_options) {
                options_set.add(option);
            };
        };
        options_array = sortOptionsArray(Array.from(options_set));
        for (option of options_array) {
            equipment_field.options.add(new Option(option.name, option.id, option.selected_val, option.default_val));
        };
    };
};

function fillOptionsWithAllEquipments() {
    for (var option of all_equipments) {
        equipment_field.options.add(new Option(option.name, option.id, option.selected_val, option.default_val));
    };
};

function sortOptionsArray(options_array) {
    options_array.sort(function(a,b) {
        if (a.name > b.name) {
            return 1;
        };
        if (a.name < b.name) {
            return -1;
        };
        return 0;
    });
    return options_array
};