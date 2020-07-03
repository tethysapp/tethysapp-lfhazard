var csrftoken = Cookies.get('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
function getStateBoundaries() {
    $.ajax({
        type: 'GET',
        async: true,
        data: {state: $("#select_state").val()},
        url: URL_getGeoJson,
        success: function (json) {
            state.addData(json);
            map.flyToBounds(state.getBounds())
        },
    })
}
const map = L.map("map", {center: [0 , 0], crs: L.CRS.EPSG4326, zoom: 2 , zoomControl: true, preferCanvas: false});
const osm = new L.TileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
let state = L.geoJSON(false).addTo(map);
getStateBoundaries()
$("#select_state").change(function() {getStateBoundaries()});
$("#select_model").change(function() {
    let sy = $("#select_year");
    if (this.value === 'cpt') {
        $("#spt-table").hide()
        $("#cpt-table").show()
        sy.empty();
        sy.append('<option value="2014" selected>2014</option>');
    } else {
        $("#spt-table").show()
        $("#cpt-table").hide()
        sy.empty();
        sy.append('<option value="2008">2008</option>');
        sy.append('<option value="2014">2014</option>');
    }
})
function query_csv(lon, lat, year, state, returnPeriod, model) {
    let data = {lon: lon, lat: lat, year: year, state: state, returnPeriod: returnPeriod, model: model};
    $.ajax({
        type: 'GET',
        url: URL_querycsv,
        dataType: 'json',
        data: data,
        success: function (results) {
            console.log(results);
            point_value = results.point_value;
            addTableRow(lon, lat, point_value[0], point_value[1], point_value[2], point_value[3], point_value[4], point_value[5], point_value[6])
        },
    });
}
map.on('click', (function(event) {
    query_csv(event.latlng['lng'], event.latlng['lat'], $("#select_year").val(), $("#select_state").val(), $("#select_return_period").val(), $("#select_model").val())
}))


let row_counter = 0
function addTableRow(lon, lat, logDvalue, Nvalue, CSRvalue, Cetinvalue, InYvalue, RnSvalue, BnTvalue) {
    var table = document.getElementById("spt-table");
    row_counter = row_counter + 1;
    var row = table.insertRow(1);
    var cell0 = row.insertCell(0);
    var cell1 = row.insertCell(1);
    var cell2 = row.insertCell(2);
    var cell3 = row.insertCell(3);
    var cell4 = row.insertCell(4);
    var cell5 = row.insertCell(5);
    var cell6 = row.insertCell(6);
    var cell7 = row.insertCell(7);
    var cell8 = row.insertCell(8);
    var cell9 = row.insertCell(9);
    var cell10 = row.insertCell(10);
    var cell11 = row.insertCell(11);
    cell0.innerHTML = $("#select_year").val();
    cell1.innerHTML = $("#select_return_period").val();
    cell2.innerHTML = lon;
    cell3.innerHTML = lat;
    cell4.innerHTML = (parseFloat(CSRvalue).toFixed(2));
    cell5.innerHTML = (parseFloat(Nvalue).toFixed(2));
    cell6.innerHTML = (parseFloat(RnSvalue).toFixed(2));
    cell7.innerHTML = (parseFloat(BnTvalue).toFixed(2));
    cell8.innerHTML = (parseFloat(logDvalue).toFixed(4));
    cell9.innerHTML = (parseFloat(Cetinvalue).toFixed(2));
    cell10.innerHTML = (parseFloat(InYvalue).toFixed(2));
    cell11.innerHTML = '<button id="Delete_row" onclick="Delete_row(this)">Delete Row</button>';
}

function Delete_row(r) {
    var i = r.parentNode.parentNode.rowIndex;
    document.getElementById("myTable").deleteRow(i);
    row_counter = row_counter - 1;
}

function Download_data() {
    let tabledata = [];
    var rows = document.querySelectorAll("table tr");

    for (var i = 0; i < rows.length; i++) {
        var row = [], cols = rows[i].querySelectorAll("td, th");

        for (var j = 0; j < cols.length; j++) {
            if (cols[j].innerText === 'Delete Row' || cols[j].innerText === 'Download Data') {
                continue
            }
            row.push(cols[j].innerText);
        }

        tabledata.push(row.join(","));
    }
    let csv = "data:text/csv;charset=utf-8," + tabledata.join("\n");
    let link = document.createElement('a');
    link.setAttribute('href', encodeURI(csv));
    link.setAttribute('target', '_blank');
    link.setAttribute('download',  'liquifaction_parameters.csv');
    document.body.appendChild(link);
    link.click();
    $("#a").remove();
}
