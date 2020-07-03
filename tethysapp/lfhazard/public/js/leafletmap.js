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
const basemaps = {
    "ESRI Topographic": L.esri.basemapLayer('Topographic').addTo(map),
    "ESRI Terrain": L.layerGroup([L.esri.basemapLayer('Terrain'), L.esri.basemapLayer('TerrainLabels')]),
    "ESRI Grey": L.esri.basemapLayer('Gray'),
}
let state = L.geoJSON(false).addTo(map);
getStateBoundaries()
L.control.layers(basemaps, {'Selected State': state}, {'collapsed': false}).addTo(map);
$("#select_state").change(function() {getStateBoundaries()});
$("#select_model").change(function() {
    if (this.value === 'cpt') {

    }
})