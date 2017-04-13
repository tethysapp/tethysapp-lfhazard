/**
 * Elements that make up the popup.
 */
var LS;
var LT_Nreq;
var LT_CSR;
var SSD_Cetin;
var SSD_IY;
var SSD_RandS;
var SSD_BandT;
var map;
var overlay;
var container = document.getElementById('popup');
var content = document.getElementById('popup-content');
var closer = document.getElementById('popup-closer');


function parseResponse_LT_CSR(json){
    console.log(json);
    // parse the json obj and display the value here
    var test = json.features[0].properties.GRAY_INDEX.toString();
    content.innerHTML += '<p><i><b>CSR(%)<sup>ref</sup></b>:  ' + test + '</i></p>';
  }

  function parseResponse_LT_Nreq(json){
    console.log(json);
    // parse the json obj and display the value here
    var test = json.features[0].properties.GRAY_INDEX.toString();
    content.innerHTML += '<p><i><b>N<sub>req</sub><sup>ref</sup></b>:  ' + test + '</i></p>';
  }

  function parseResponse_LS(json){
    console.log(json);
    // parse the json obj and display the value here
    var test = json.features[0].properties.GRAY_INDEX.toString();
    content.innerHTML += '<p><i><b>Log D<sub>h</sub><sup>ref</sup></b>:  ' + test + '</i></p>';
  }

  function parseResponse_SSD_RandS(json){
    console.log(json);
    // parse the json obj and display the value here
    var test = json.features[0].properties.GRAY_INDEX.toString();
    content.innerHTML += '<p><i><b>D<sub>R&S</sub><sup>ref</sup></b>:  ' + test + '</i></p>';
  }

  function parseResponse_SSD_BandT(json){
    console.log(json);
    // parse the json obj and display the value here
    var test = json.features[0].properties.GRAY_INDEX.toString();
    content.innerHTML += '<p><i><b>D<sub>B&T</sub><sup>ref</sup></b>:  ' + test + '</i></p>';
  }

  function parseResponse_SSD_Cetin(json){
    console.log(json);
    // parse the json obj and display the value here
    var test = json.features[0].properties.GRAY_INDEX.toString();
    content.innerHTML += '<p><i><b>&epsilon;<sub>v,Cetin</sub>(%)<sup>ref</sup></b>:  ' + test + '</i></p>';
  }

  function parseResponse_SSD_IY(json){
    console.log(json);
    // parse the json obj and display the value here
    var test = json.features[0].properties.GRAY_INDEX.toString();
    content.innerHTML += '<p><i><b>&epsilon;<sub>v,I&Y%</sub>(%)<sup>ref</sup></b>:  ' + test + '</i></p>';
  }

function submitButton() {
  var lat = document.getElementById('lat-input').value;
  var lon = document.getElementById('lon-input').value;


  var coordinate = [Number(lat), Number(lon)];
  console.log("Submit click 1: " + coordinate);

  var newcoor = ol.proj.transform([Number(lat), Number(lon)], 'EPSG:4326','EPSG:3857');
  console.log("Submit click 2: " + newcoor); //This changes lat and long into EPSG:3857

  getPopup(newcoor);
  }


function getPopup(coordinate) {
  var view = map.getView();
  var viewResolution = view.getResolution();

  var hdms = ol.coordinate.toStringHDMS(ol.proj.transform(
    coordinate, 'EPSG:3857', 'EPSG:4326'));

  content.innerHTML = '<p><b>Location:</b><br>'+ hdms + '</p>';


  var source_LS = LS.getSource();
  var source_LT_Nreq = LT_Nreq.getSource();
  var source_LT_CSR = LT_CSR.getSource();
  var source_SSD_Cetin = SSD_Cetin.getSource();
  var source_SSD_IY = SSD_IY.getSource();
  var source_SSD_RandS = SSD_RandS.getSource();
  var source_SSD_BandT = SSD_BandT.getSource();

  var url_LS = source_LS.getGetFeatureInfoUrl(
    coordinate, viewResolution, view.getProjection(),
    {'INFO_FORMAT': 'text/javascript', 'FEATURE_COUNT': 50});
  url_LS = url_LS + "&format_options=callback:parseResponse_LS"
  console.log(url_LS);

  var url_LT_Nreq = source_LT_Nreq.getGetFeatureInfoUrl(
    coordinate, viewResolution, view.getProjection(),
    {'INFO_FORMAT': 'application/json', 'FEATURE_COUNT': 50});
  url_LT_Nreq = url_LT_Nreq + "&format_options=callback:parseResponse_LT_Nreq"

  var url_LT_CSR = source_LT_CSR.getGetFeatureInfoUrl(
    coordinate, viewResolution, view.getProjection(),
    {'INFO_FORMAT': 'application/json', 'FEATURE_COUNT': 50});
  url_LT_CSR = url_LT_CSR + "&format_options=callback:parseResponse_LT_CSR"

  var url_SSD_Cetin = source_SSD_Cetin.getGetFeatureInfoUrl(
    coordinate, viewResolution, view.getProjection(),
    {'INFO_FORMAT': 'application/json', 'FEATURE_COUNT': 50});
  url_SSD_Cetin = url_SSD_Cetin + "&format_options=callback:parseResponse_SSD_Cetin"

  var url_SSD_IY = source_SSD_IY.getGetFeatureInfoUrl(
    coordinate, viewResolution, view.getProjection(),
    {'INFO_FORMAT': 'application/json', 'FEATURE_COUNT': 50});
  url_SSD_IY = url_SSD_IY + "&format_options=callback:parseResponse_SSD_IY"

  var url_SSD_RandS = source_SSD_RandS.getGetFeatureInfoUrl(
    coordinate, viewResolution, view.getProjection(),
    {'INFO_FORMAT': 'application/json', 'FEATURE_COUNT': 50});
  url_SSD_RandS = url_SSD_RandS + "&format_options=callback:parseResponse_SSD_RandS"
  
  var url_SSD_BandT = source_SSD_BandT.getGetFeatureInfoUrl(
    coordinate, viewResolution, view.getProjection(),
    {'INFO_FORMAT': 'application/json', 'FEATURE_COUNT': 50});
  url_SSD_BandT = url_SSD_BandT + "&format_options=callback:parseResponse_SSD_BandT"

  var LSs = "LS";
  var LT_Nreqs = "LT_Nreq";
  var LT_CSRs = "LT_CSR";
  var SSD_Cetins = "SSD_Cetin";
  var SSD_IYs = "SSD_IY";
  var SSD_RandSs = "SSD_RandS";
  var SSD_BandTs = "SSD_BandT";


  $.getJSON(url_LT_CSR, function(data) {var test = data.features[0].properties.GRAY_INDEX.toString();
  content.innerHTML += '<p><i><b>CSR(%)<sup>ref</sup></b>:  ' + test + '</i></p>'});
  $.getJSON(url_LT_Nreq, function(data) {var test = data.features[0].properties.GRAY_INDEX.toString();
  content.innerHTML += '<p><i><b>N<sub>req</sub><sup>ref</sup></b>:  ' + test + '</i></p>'});
  $.getJSON(url_LS, function(data) {var test = data.features[0].properties.GRAY_INDEX.toString();
  content.innerHTML += '<p><i><b>Log D<sub>h</sub><sup>ref</sup></b>:  ' + test + '</i></p>'});
  $.getJSON(url_SSD_RandS, function(data) {var test = data.features[0].properties.GRAY_INDEX.toString();
  content.innerHTML += '<p><i><b>D<sub>R&S</sub><sup>ref</sup></b>:  ' + test + '</i></p>'});
  $.getJSON(url_SSD_BandT, function(data) {var test = data.features[0].properties.GRAY_INDEX.toString();
  content.innerHTML += '<p><i><b>D<sub>B&T</sub><sup>ref</sup></b>:  ' + test + '</i></p>'});
  $.getJSON(url_SSD_Cetin, function(data) {var test = data.features[0].properties.GRAY_INDEX.toString();
  content.innerHTML += '<p><i><b>&epsilon;<sub>v,Cetin</sub>(%)<sup>ref</sup></b>:  ' + test + '</i></p>'});
  $.getJSON(url_SSD_IY, function(data) {var test = data.features[0].properties.GRAY_INDEX.toString();
  content.innerHTML += '<p><i><b>&epsilon;<sub>v,I&Y%</sub>(%)<sup>ref</sup></b>:  ' + test + '</i></p>'});

// change my_url to your variable that contains the real url
  // $.ajax({
  //   url: url_LT_CSR, // change this line
  //   dataType: "jsonp", // do not change this line
  //   jsonpCallback: "parseResponse_LT_CSR" //do not change this line
  // });
  // $.ajax({
  //   url: url_LT_Nreq, // change this line
  //   dataType: "jsonp", // do not change this line
  //   jsonpCallback: "parseResponse_LT_Nreq" //do not change this line
  // });
  // $.ajax({
  //   url: url_LS, // change this line
  //   dataType: "jsonp", // do not change this line
  //   jsonpCallback: "parseResponse_LS" //do not change this line
  // });
  // $.ajax({
  //   url: url_SSD_RandS, // change this line
  //   dataType: "jsonp", // do not change this line
  //   jsonpCallback: "parseResponse_SSD_RandS" //do not change this line
  // });
  // $.ajax({
  //   url: url_SSD_BandT, // change this line
  //   dataType: "jsonp", // do not change this line
  //   jsonpCallback: "parseResponse_SSD_BandT" //do not change this line
  // });
  // $.ajax({
  //   url: url_SSD_Cetin, // change this line
  //   dataType: "jsonp", // do not change this line
  //   jsonpCallback: "parseResponse_SSD_Cetin" //do not change this line
  // });
  // $.ajax({
  //   url: url_SSD_IY, // change this line
  //   dataType: "jsonp", // do not change this line
  //   jsonpCallback: "parseResponse_SSD_IY" //do not change this line
  // });

  overlay.setPosition(coordinate);

}

$( document ).ready(function() {
  /**
   * Create an overlay to anchor the popup to the map.
   */
  overlay = new ol.Overlay(/** @type {olx.OverlayOptions} */ ({
    element: container,
    autoPan: true,
    autoPanAnimation: {
      duration: 250
    }
  }));


  /**
   * Add a click handler to hide the popup.
   * @return {boolean} Don't follow the href.
   */
  closer.onclick = function() {
    overlay.setPosition(undefined);
    closer.blur();
    return false;
  };


  /**
   * Create the map.
   */
  map = new ol.Map({
    layers: [
      new ol.layer.Tile({
        source: new ol.source.TileJSON({
          url: 'https://api.tiles.mapbox.com/v3/mapbox.natural-earth-hypso-bathy.json?secure',
          crossOrigin: 'anonymous'
        })
      }),
    ],
    overlays: [overlay],
    target: 'map',
    view: new ol.View({
      center: [-11000000, 4600000], //This sets the center of map to center of states
      zoom: 4
    })
  });

  var format = 'image/png';

  var returnPeriod = document.getElementById('select_returnPeriod').value;
  var state = document.getElementById('select_state').value;
  var modelYear = document.getElementById('select_modelYear').value;

  LS = new ol.layer.Tile({
    visible: false,
    source: new ol.source.TileWMS({
      url: 'http://127.0.0.1:8181/geoserver/lfhazard/wms',
      params: {'FORMAT': format, 
               'VERSION': '1.1.1',
               tiled: true,
            LAYERS: 'lfhazard:Kriging_LS-' + returnPeriod + '_' + state + modelYear,
            STYLES: '',
      }
    })
  });

  LT_Nreq = new ol.layer.Tile({
          visible: false,
          source: new ol.source.TileWMS({
            url: 'http://127.0.0.1:8181/geoserver/lfhazard/wms',
            params: {'FORMAT': format, 
                     'VERSION': '1.1.1',
                     tiled: true,
                  LAYERS: 'lfhazard:Kriging_LT-' + returnPeriod + '_' + state + '_PB_Nreq_Cetin' + modelYear,
                  STYLES: '',
            }
          })
        });

  LT_CSR = new ol.layer.Tile({
          visible: false,
          source: new ol.source.TileWMS({
            url: 'http://127.0.0.1:8181/geoserver/lfhazard/wms',
            params: {'FORMAT': format, 
                     'VERSION': '1.1.1',
                     tiled: true,
                  LAYERS: 'lfhazard:Kriging_LT-' + returnPeriod + '_' + state + '_PB_CSR_' + modelYear,
                  STYLES: '',
            }
          })
        });

  SSD_Cetin = new ol.layer.Tile({
          visible: false,
          source: new ol.source.TileWMS({
            url: 'http://127.0.0.1:8181/geoserver/lfhazard/wms',
            params: {'FORMAT': format, 
                     'VERSION': '1.1.1',
                     tiled: true,
                  LAYERS: 'lfhazard:Kriging_SSD-' + returnPeriod + '_' + state + '_Cetin_percent' + modelYear,
                  STYLES: '',
            }
          })
        });

  SSD_IY = new ol.layer.Tile({
          visible: false,
          source: new ol.source.TileWMS({
            url: 'http://127.0.0.1:8181/geoserver/lfhazard/wms',
            params: {'FORMAT': format, 
                     'VERSION': '1.1.1',
                     tiled: true,
                  LAYERS: 'lfhazard:Kriging_SSD-' + returnPeriod + '_' + state + '_IandY_percent' + modelYear,
                  STYLES: '',
            }
          })
        });

  SSD_RandS = new ol.layer.Tile({
          visible: false,
          source: new ol.source.TileWMS({
            url: 'http://127.0.0.1:8181/geoserver/lfhazard/wms',
            params: {'FORMAT': format, 
                     'VERSION': '1.1.1',
                     tiled: true,
                  LAYERS: 'lfhazard:Kriging_SSD-' + returnPeriod + '_' + state + '_PB_Seismic_Slope_Disp_RandS' + modelYear,
                  STYLES: '',
            }
          })
        });

  SSD_BandT = new ol.layer.Tile({
          visible: false,
          source: new ol.source.TileWMS({
            url: 'http://127.0.0.1:8181/geoserver/lfhazard/wms',
            params: {'FORMAT': format, 
                     'VERSION': '1.1.1',
                     tiled: true,
                  LAYERS: 'Kriging_SSD-' + returnPeriod + '_' + state + '_PB_Seismic_Slope_Disp_BandT' + modelYear,
                  STYLES: '',
            }
          })
        });

  map.on('singleclick', function(evt) {
    if (returnPeriod != "" && state != "" && modelYear != "") {
      var coordinate = evt.coordinate;
      console.log("On click: " + coordinate);
      getPopup(coordinate);
    }
    else {
      alert("No parameters provided");
    }    
  });
});