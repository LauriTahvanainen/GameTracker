function defaultDate() {
    document.getElementById('date_observed').valueAsDate = new Date();
    maxDateToday();
}
function maxDateToday() {
    document.getElementById('date_observed').setAttribute('max',new Date().toISOString().split('T')[0]);
}