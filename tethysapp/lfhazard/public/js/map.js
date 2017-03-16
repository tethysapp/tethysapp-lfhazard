/**
 * Elements that make up the popup.
 */
$( document ).ready(function() {
  var container = document.getElementById('popup');
  var content = document.getElementById('popup-content');
  var closer = document.getElementById('popup-closer');


  /**
   * Create an overlay to anchor the popup to the map.
   */
  var overlay = new ol.Overlay(/** @type {olx.OverlayOptions} */ ({
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
  var map = new ol.Map({
    layers: [
      new ol.layer.Tile({
        source: new ol.source.TileJSON({
          url: 'https://api.tiles.mapbox.com/v3/mapbox.natural-earth-hypso-bathy.json?secure',
          crossOrigin: 'anonymous'
        })
      })
    ],
    overlays: [overlay],
    target: 'map',
    view: new ol.View({
      center: [0, 0],
      zoom: 2
    })
  });

  var format = 'image/png';

  var LS = new ol.layer.Tile({
    visible: false,
    source: new ol.source.TileWMS({
      url: 'http://127.0.0.1:8181/geoserver/lfhazard/wms',
      params: {'FORMAT': format, 
               'VERSION': '1.1.1',
               tiled: true,
            LAYERS: 'Kriging_LS-' + returnPeriod + '_' + state + modelYear,
            STYLES: '',
      }
    })
  });

  var LT_Nreq = new ol.layer.Tile({
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

  var LT_CSR = new ol.layer.Tile({
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

  var SSD_Cetin = new ol.layer.Tile({
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

  var SSD_IY = new ol.layer.Tile({
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

  var SSD_RandS = new ol.layer.Tile({
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

  var SSD_BandT = new ol.layer.Tile({
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
      var view = map.getView();
      var viewResolution = view.getResolution();

      var coordinate = evt.coordinate;
      var hdms = ol.coordinate.toStringHDMS(ol.proj.transform(
        coordinate, 'EPSG:3857', 'EPSG:4326'));

      content.innerHTML = '<p>Location:</p>'+ hdms + '</br>';

      var source_LS = LS.getSource();
      var source_LT_Nreq = LT_Nreq.getSource();
      var source_LT_CSR = LT_CSR.getSource();
      var source_SSD_Cetin = SSD_Cetin.getSource();
      var source_SSD_IY = SSD_IY.getSource();
      var source_SSD_RandS = SSD_RandS.getSource();
      var source_SSD_BandT = SSD_BandT.getSource();

      var url_LS = source_LS.getGetFeatureInfoUrl(
        evt.coordinate, viewResolution, view.getProjection(),
        {'INFO_FORMAT': 'application/json', 'FEATURE_COUNT': 50});
      var url_LT_Nreq = source_LT_Nreq.getGetFeatureInfoUrl(
        evt.coordinate, viewResolution, view.getProjection(),
        {'INFO_FORMAT': 'application/json', 'FEATURE_COUNT': 50});
      var url_LT_CSR = source_LT_CSR.getGetFeatureInfoUrl(
        evt.coordinate, viewResolution, view.getProjection(),
        {'INFO_FORMAT': 'application/json', 'FEATURE_COUNT': 50});
      var url_SSD_Cetin = source_SSD_Cetin.getGetFeatureInfoUrl(
        evt.coordinate, viewResolution, view.getProjection(),
        {'INFO_FORMAT': 'application/json', 'FEATURE_COUNT': 50});
      var url_SSD_IY = source_SSD_IY.getGetFeatureInfoUrl(
        evt.coordinate, viewResolution, view.getProjection(),
        {'INFO_FORMAT': 'application/json', 'FEATURE_COUNT': 50});
      var url_SSD_RandS = source_SSD_RandS.getGetFeatureInfoUrl(
        evt.coordinate, viewResolution, view.getProjection(),
        {'INFO_FORMAT': 'application/json', 'FEATURE_COUNT': 50});
      var url_SSD_BandT = source_SSD_BandT.getGetFeatureInfoUrl(
        evt.coordinate, viewResolution, view.getProjection(),
        {'INFO_FORMAT': 'application/json', 'FEATURE_COUNT': 50});

      var LSs = "LS";
      var LT_Nreqs = "LT_Nreq";
      var LT_CSRs = "LT_CSR";
      var SSD_Cetins = "SSD_Cetin";
      var SSD_IYs = "SSD_IY";
      var SSD_RandSs = "SSD_RandS";
      var SSD_BandTs = "SSD_BandT";


      $.getJSON(url_LT_CSR, function(data) {var test = data.features[0].properties.GRAY_INDEX.toString()
      content.innerHTML += '<p>CSR%:  ' + test + '</p>'});
      $.getJSON(url_LT_Nreq, function(data) {var test = data.features[0].properties.GRAY_INDEX.toString();
      content.innerHTML += '<p>NReqREf:  ' + test + '</p>'});
      $.getJSON(url_LS, function(data) {var test = data.features[0].properties.GRAY_INDEX.toString();
      content.innerHTML += '<p>DHRef:  ' + test + '</p>'});
      $.getJSON(url_SSD_RandS, function(data) {var test = data.features[0].properties.GRAY_INDEX.toString()
      content.innerHTML += '<p>DREFR&S:  ' + test + '</p>'});
      $.getJSON(url_SSD_BandT, function(data) {var test = data.features[0].properties.GRAY_INDEX.toString()
      content.innerHTML += '<p>DREFB&T:  ' + test + '</p>'});
      $.getJSON(url_SSD_Cetin, function(data) {var test = data.features[0].properties.GRAY_INDEX.toString()
      content.innerHTML += '<p>Cetin:  ' + test + '</p>'});
      $.getJSON(url_SSD_IY, function(data) {var test = data.features[0].properties.GRAY_INDEX.toString()
      content.innerHTML += '<p>I&Y%:  ' + test + '</p>'});

      overlay.setPosition(coordinate);
    }
    else {
      alert("No parameters provided");
    }    
  });
});