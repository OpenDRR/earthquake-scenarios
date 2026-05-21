---
authorName: Natural Resources Canada
authorUrl:
dateModified: 2024-02-21
noContentTitle: true
pageclass: wb-prettify all-pre
subject:
  en: [GV Government and Politics, Government services]
  fr: [GV Gouvernement et vie politique, Services gouvernementaux]
title: Earthquake Scenario Map
lang: en
altLangPage: ../fr/dsra_scenario_map.html
nositesearch: true
nomenu: true
nofooter: true
breadcrumbs:
  - title: "OpenDRR"
    link: "https://www.github.com/OpenDRR/"
  - title: "OpenDRR Downloads"
    link: "../downloads/en"
  - title: "Earthquake Scenarios"
    link: "/en"
  - title: "Earthquake Scenario Map"
---
<!-- Load Leaflet from CDN -->
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css"
integrity="sha512-xodZBNTC5n17Xt2atTPuE1HxjVMSvLVW9ocqUKLsCC5CXdbqCmblAshOMAS6/keqq/sMZMZ19scR4PsZChSR7A=="
crossorigin=""/>

<script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"
integrity="sha512-XQoYMqMTK8LvdxXYG3nZ448hOEQiglfqkJs1NOQV44cWnUrBc8PkAOcXy20w0vlaXaVUearIOBhiXZ5V3ynxwA=="
crossorigin=""></script>

<!-- Load Esri Leaflet from CDN -->
<script src="https://unpkg.com/esri-leaflet@3.0.2/dist/esri-leaflet.js"
integrity="sha512-myckXhaJsP7Q7MZva03Tfme/MSF5a6HC2xryjAM4FxPLHGqlh5VALCbywHnzs2uPoF/4G/QVXyYDDSkp5nPfig=="
crossorigin=""></script>

<!-- Load Esri Leaflet Renderers plugin to use feature service symbology -->
<script src="https://unpkg.com/esri-leaflet-renderers@2.1.2" crossorigin=""></script>

<script src='https://api.mapbox.com/mapbox.js/plugins/leaflet-fullscreen/v1.0.1/Leaflet.fullscreen.min.js'></script>
<link href='https://api.mapbox.com/mapbox.js/plugins/leaflet-fullscreen/v1.0.1/leaflet.fullscreen.css' rel='stylesheet'/>
<script src="https://unpkg.com/leaflet.vectorgrid@latest/dist/Leaflet.VectorGrid.bundled.js"></script>

<script src="https://code.jquery.com/jquery-3.6.0.min.js" integrity="sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4=" crossorigin="anonymous"></script>

<link href='../assets/css/app.css' rel='stylesheet'/>

<div id="map"></div>
<div id="sidebar"></div>

<div id="alert">{% if page.lang == 'en' %}Unable to load scenario{% else %}Impossible de charger le scénario{% endif %}</div>
<div id="scenarios">
  <h5>{% if page.lang == 'en' %}Available scenarios:{% else %}Scénarios disponibles:{% endif %}</h5>
  <ul>
    {% for scenario in site.data.dsra.scenarios %}
      <li><a href="{{ context.environments.first["page"]["url"] }}?scenario={{scenario.name}}"><small>{{ scenario.title[page.lang] }}</small></a></li>
    {% endfor %}
  </ul>
</div>

{% assign variables = '' %}
{% for attribute in site.data.dsra_attributes.attributes %}
  {% capture variable %}
  window['{{attribute.name}}' + 'Desc'] = '{{attribute.description[page.lang]}}';
  window['{{attribute.name}}' + 'Detail'] = '{{attribute.detailed[page.lang]}}';
  window['{{attribute.name}}' + 'Format'] = Number('{{attribute.format}}');
  {% endcapture %}
  {% assign variables = variables | append: variable %}
{% endfor %}

<script>

  {{ variables }}

  var map = L.map( 'map', {
      fullscreenControl: true,
      crs: L.CRS.EPSG4326,
      center: [ 57, -100 ],
      maxZoom: 13,
      minZoom: 6,
      zoom: 6}),
      bounds, // Bounds for the tileset, set according to scenario
      legend = L.control( { position: 'bottomright' } ),
      params = new URLSearchParams( window.location.search ), // Get query paramaters
      // baseUrl = "https://riskprofiler.ca/dsra_",
      baseUrl = "https://riskprofiler-ca.github.io/dsra_",
      shakeBaseUrl = "https://geo-api.stage.riskprofiler.ca/collections/opendrr_dsra_",
      eqScenario = params.get( 'scenario' ), // Scenario name
      shakemapProp = 'sH_PGA_max', // Property for shakemap popup
      scenarioProp = 'sCt_Res90_b0', // Property for popup and feature colour
      shakeCurrent = true,
      epicentre,
      selection = 0; // Id of a selected feature


  L.tileLayer( 'https://osm-{s}.gs.mil/tiles/default_pc/{z}/{x}/{y}.png', {
      subdomains: '1234',
      attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      detectRetina: true
	}).addTo( map );


  if ( eqScenario ) {

    $( "#scenarios" ).hide(); // Hide list of available scenarios

    lcScenario = eqScenario.toLowerCase();
    setBounds();

    var vectorTileOptions = {
      rendererFactory: L.canvas.tile,
      interactive: true,
      getFeatureId: function( feature ) {
        return feature.properties[ "Sauid" ];
      },
      bounds: bounds,
      vectorTileLayerStyles: setTileLayerStyles()
    }

    function shakeTileOptions( z ) {
      return {
      rendererFactory: L.canvas.tile,
      interactive: true,
      getFeatureId: function( feature ) {
        return feature.properties[ "gridid_5" ];
      },
      bounds: bounds,
      vectorTileLayerStyles: setShakeLayerStyles( z )
      }
    }

    // Turn scenario name into a title
    end = eqScenario.split( '_' )[ 1 ];
    title = '';
    for ( let char of end ) {
      // Add space before uppercase letters
      if ( char == char.toUpperCase() ) {
        title += ' ' + char;
      }
      // Leave lowercase as is
      else {
        title += char;
      }
    }
    const mag = eqScenario[ 3 ] + '.' + eqScenario[ 5 ],
          full_name = title + ' - Magnitude ' + mag;
    // Replace generic title with scenario name
    // $( '#wb-cont' ).html( full_name );
    {% for scenario in site.data.dsra.scenarios %}
      if ( eqScenario === '{{ scenario.name }}' ) {
        $( '#wb-cont' ).html( '{{ scenario.title[page.lang] }}' );
      }
    {% endfor %}

    var vectorUrl = baseUrl + lcScenario + "_indicators_s/EPSG_4326/{z}/{x}/{y}.pbf",
        shakemapUrl1 = baseUrl + lcScenario + "_shakemap_hexgrid_1km/EPSG_4326/{z}/{x}/{y}.pbf",
        shakemapUrl5 = baseUrl + lcScenario + "_shakemap_hexgrid_5km/EPSG_4326/{z}/{x}/{y}.pbf";

    var sauidLayer = L.vectorGrid.protobuf( vectorUrl, vectorTileOptions )
        .on( 'add', function () {
        shakeCurrent = false;
        map.removeLayer( shakeLayer5km );
        map.removeLayer( shakeLayer1km );
        // Add loading modal
        $( '#map' ).before( '<div id="modal"></div>' );
      }).on( 'load', function () {
        // Remove loading modal
        $( '#modal' ).remove();
        epicentre.bringToFront();
      });

    var shakeLayer1km = L.vectorGrid.protobuf( shakemapUrl1, shakeTileOptions( 1 ) )
        .on( 'add', function () {
        shakeCurrent = true;
        // Add loading modal
        $( '#map' ).before( '<div id="modal"></div>' );
      }).on( 'load', function () {
        // Remove loading modal
        $( '#modal' ).remove();
        epicentre.bringToFront();
      }).on( 'click', function ( e ) {
    	  L.popup().setContent( "<strong>{% if page.lang == 'en' %}PGA: {% else %}AMS: {% endif %}</strong>" + e.layer.properties.sH_PGA_max.toLocaleString( undefined, { maximumFractionDigits: 2 }) )
          .setLatLng( e.latlng )
          .openOn( map );
      });

    var shakeLayer5km = L.vectorGrid.protobuf( shakemapUrl5, shakeTileOptions( 5 ) )
        .on( 'add', function () {
        shakeCurrent = true;
        // Add loading modal
        $( '#map' ).before( '<div id="modal"></div>' );
      }).on( 'load', function () {
        // Remove loading modal
        $( '#modal' ).remove();
        epicentre.bringToFront();
      }).on( 'click', function ( e ) {
    	  L.popup().setContent( "<strong>{% if page.lang == 'en' %}PGA: {% else %}AMS: {% endif %}</strong>" + e.layer.properties.sH_PGA_max.toLocaleString( undefined, { maximumFractionDigits: 2 }) )
          .setLatLng( e.latlng )
          .openOn( map );
      });

    var overlays = {
      {% if page.lang == 'en' %}'ShakeMap (5km grid)'{% else %}'ShakeMap (5km grille)'{% endif %}: shakeLayer5km,
      {% if page.lang == 'en' %}'ShakeMap (1km grid)'{% else %}'ShakeMap (1km grille)'{% endif %}: shakeLayer1km,
      {% if page.lang == 'en' %}'Features'{% else %}'Caractéristiques'{% endif %}: sauidLayer,
    };

    // Add shakemap, legend and layer toggle to map
    shakeLayer5km.addTo( map );
    buildLegend();
    L.control.layers( overlays, null, { collapsed: false } ).addTo( map );

    map.on( 'fullscreenchange', function () {
      map.invalidateSize();
    }).on( 'zoomend dragend', function ( e ) {
      map.closePopup();
      // Reset layers if zoomed in or zooming out to new feature
      var zoom = e.target.getZoom();
      map.removeLayer( shakeLayer5km );
      map.removeLayer( shakeLayer1km );
      if ( shakeCurrent ) {
        if ( zoom < 10 ) {
          shakeLayer5km.addTo( map );
        }
        else {
          shakeLayer1km.addTo( map );
        }
      }
    }).on( 'baselayerchange', function () {
      $( '#sidebar' ).html( '' );
      map.closePopup();
      // If we have a selected feature reset the style
      if ( selection != 0 ) {
        sauidLayer.resetFeatureStyle( selection );
      }

      // Remove old legend and add new legend
      map.removeControl( legend );
      buildLegend();
    });

    sauidLayer.on( 'click', function ( e ) {
      // If we have a selected feature reset the style
      if ( selection != 0 ) {
        sauidLayer.resetFeatureStyle( selection );
      }

      // Set the selected feature id
      selection = e.layer.properties[ 'Sauid' ];

      // Set the selected feature style
      setTimeout( function () {
        sauidLayer.setFeatureStyle( selection, selectedStyle(), 100 );
      });

      // Add a popup with desired property
      L.popup().setContent( "<strong>{% if page.lang == 'en' %}Residents affected after 90 days: {% else %}Résidents relogés après 90 jours: {% endif %}</strong>" + e.layer.properties.sCt_Res90_b0.toString() )
          .setLatLng( e.latlng )
          .openOn( map );

      let props = e.layer.properties,
        string = '<table class="table table-striped table-responsive"><tr>',
        counter = 1; // Counts number of cells in table row

      for ( const key in props ) {

        mod_key = key; // Key with _b0, _r1, _le ending must be modified
        mod = '';

        if ( key.slice( -3 ) === '_b0' ) {
          mod_key = key.slice( 0, -3 );
          mod = {% if page.lang == 'en' %}' (Baseline)'{% else %}' (référence)'{% endif %};
        }
        else if ( key.slice( -3 ) === '_r1' ) {
          mod_key = key.slice( 0, -3 );
          mod = {% if page.lang == 'en' %}' (Retrofit)'{% else %}' (rénovation)'{% endif %};
        }
        else if ( key.slice( -3 ) === '_le' ) {
          mod_key = key.slice( 0, -3 );
          mod = {% if page.lang == 'en' %}' (Seismic Upgrade)'{% else %}' (amélioration sismique)'{% endif %};
        }

        var desc = window[ mod_key + 'Desc' ],
            detail = window[ mod_key + 'Detail' ],
            format = window[ mod_key + 'Format' ],
            value = props[ key ];

        // Format values with set formatting
        if ( format && value ) {
          if ( format === 444 ) {
            value = value.toLocaleString( undefined, {style:'currency', currency:'USD'});
          }
          else if ( format === 111 ) {
            value = value.toLocaleString( undefined, { maximumFractionDigits: 0 })
          }
          else if ( format === 555 ) {
            value *= 100
            value = value.toLocaleString( undefined, { maximumFractionDigits: 2 });
            value += '%';
          }
          else if ( format < 0 ) {
            mult = Math.abs(format);
            rounded = Math.round( value / ( 10 ** mult )) * 10 ** mult;
            value = rounded.toLocaleString( undefined);
          }
          else if ( format > 0 ) {
            value = value.toLocaleString( undefined, { maximumFractionDigits: format });
          }

          string +=
          '<td class="attr"><div class="prop" title="' + detail + '">' + desc + mod + '</div><div class="val">' + value + '</div></td>';
        }
        // Leaflet info not displayed
        else if ( key === 'OBJECTID' || key === 'SHAPE_Length' || key === 'SHAPE_Area' || key === 'geom_poly' || key === 'geom' ) {
        }
        // For properties with descriptions but null values
        else if ( desc ) {
          string +=
            '<td class="attr"><div class="prop" title="' + detail + '">' + desc + mod + '</div><div class="val">' + value + '</div></td>';
        }
        // Properties with no descriptions
        else {
          string +=
            '<td class="attr"><div class="prop">' + key + '</div><div class="val">' + value + '</div></td>';
        }

        // Start new row after 3 entries
        if ( counter % 3 === 0 ) {
          string += '</tr><tr>';
        }
        counter++;
      }

      string += '</tr></table>';

      // Add table to sidebar div
      $( '#sidebar' ).html( '<h3>{% if page.lang == 'en' %}Properties of Selected Feature{% else %}Propriétés de la caractéristique sélectionnée{% endif %}</h3>' + string );

    });
  }
  else {
    $( '#alert' ).show();
  }


  function getColor( d ) {
    return d > 300 ? '#ff3b00' :
           d > 100 ? '#ff6500' :
           d > 50  ? '#ff9000' :
           d > 10  ? '#ffba00' :
                     '#fff176';
  }

  function shakeColor( d ) {
    return d > 50  ? '#e81f27' :
           d > 25  ? '#f55029' :
           d > 10  ? '#fc8b40' :
           d > 5   ? '#fdb24c' :
           d > 1.5 ? '#ffd976' :
                     '#ffee9f';
  }

  function buildLegend () {

    legend.onAdd = function ( map ) {

      var div = L.DomUtil.create('div', 'info legend');

      if ( !shakeCurrent ) {

        var grades = [0, 10, 50, 100, 300],
            label = {% if page.lang == 'en' %}' Residents Affected'{% else %}' Résidents relogés'{% endif %};

        div.innerHTML = "<div style=\"padding: 3px;\"><b>{% if page.lang == 'en' %}Residents affected after 90 days{% else %}Résidents relogés après 90 jours{% endif %}</b></div>";

        // Loop through our density intervals and generate a label with a colored square for each interval
        for (var i = 0; i < grades.length; i++ ) {
          div.innerHTML +=
            '<div><i style="background:' + getColor(grades[i] + 1) + '"></i> ' + grades[i] + ( grades[i + 1] ? ' &ndash; ' + grades[i + 1] + label + '<br>' : '+' + label) + '</div>';
        }

        div.innerHTML +=
            '<br><div>🔴 <b>{% if page.lang == 'en' %}Epicentre{% else %}Épicentre{% endif %}</b></div>';
      }

      else {

        var grades = [0, 1.5, 5, 10, 25, 50],
            label = ' %g';

        div.innerHTML = "<div style=\"padding: 3px;\"><b>{% if page.lang == 'en' %}Peak Ground Acceleration{% else %}Accélération maximale du sol{% endif %}</b></div>";

        // Loop through our density intervals and generate a label with a colored square for each interval
        for (var i = 0; i < grades.length; i++ ) {
          div.innerHTML +=
            '<div><i style="background:' + shakeColor(grades[i] + 0.01) + '"></i> ' + grades[i] + ( grades[i + 1] ? ' &ndash; ' + grades[i + 1] + label + '<br>' : '+' + label) + '</div>';
        }

        div.innerHTML +=
            '<br><div>🔴 <b>{% if page.lang == 'en' %}Epicentre{% else %}Épicentre{% endif %}</b></div>';
      }

      return div;
    };

    legend.addTo( map );
  }

  function shakeStyle( properties ) {
    return {
      fillColor: shakeColor( properties[ shakemapProp ] * 100 ),
      weight: 0.1,
      fillOpacity: 0.8,
      color: shakeColor( properties[ shakemapProp ] * 100 ),
      opacity: 0.8,
      fill: true
    };
  }

  function tileStyle( properties ) {
    return {
      weight: 0.2,
      color: "#666666",
      fillColor: getColor( properties[ scenarioProp ] ),
      fillOpacity: 0.6,
      fill: true
    }
  }

  function selectedStyle() {
    return {
      fill: true,
      fillColor: 'blue',
      color: 'black',
      weight: 1,
      fillOpacity: 0.5
    };
  }

  function circleStyle() {
    return {
      radius: 6,
      fillColor: 'red',
      color: 'white',
      weight: 1,
      opacity: 1,
      fillOpacity: 1
    };
  }



function setBounds() {
    const scenarioConfig = {
        "acm7p0_georgiastraitfault": {
            southWest: [48.30891568684188, -129.0949439967106],
            northEast: [53.53110877480622, -117.3589501128889],
            epicentre: [49.243365, -123.62296]
        },
        "acm7p3_leechriverfullfault": {
            southWest: [48.30891568624434, -129.0949439967106],
            northEast: [53.30903267135562, -117.4908738038378],
            epicentre: [48.407017, -123.412134]
        },
        "sim9p0_cascadiainterfacebestfault": {
            southWest: [48.30891568684188, -139.0522010412872],
            northEast: [60.00006153221153, -114.05375826483],
            epicentre: [48.251246, -125.215269]
        },
        "scm7p5_valdesbois": {
            southWest: [42.47260780141163, -86.54942531485392],
            northEast: [55.00064603767294, -67.44787497495167],
            epicentre: [45.905377, -75.494669]
        },
        "idm7p1_sidney": {
            southWest: [48.30891568684188, -129.0949439967106],
            northEast: [53.30903267135562, -117.3589501128889],
            epicentre: [48.618961, -123.299385]
        },
        "acm4p9_georgiastraitfault": {
            southWest: [48.30891568684188, -129.0949439967106],
            northEast: [53.53110877480622, -117.3589501128889],
            epicentre: [49.280, -123.340]
        },
        "acm7p4_denalifault": {
            southWest: [60.00000000710405, -141.0180731580253],
            northEast: [69.64745530351352, -123.7893248352215],
            epicentre: [61.200 , -138.780]
        },
        "scm5p0_montreal": {
            southWest: [42.53884243059241, -86.54942531485392],
            northEast: [55.00064603767294, -65.94908207524423],
            epicentre: [45.500 , -73.600]
        },
        "scm5p5_constancebay": {
            southWest: [42.06164244999297, -86.54942531485392],
            northEast: [55.00064603767294, -68.38243594858385],
            epicentre: [45.500 , -76.060]
        },
        "acm4p9_vedderfault": {
            southWest: [48.30891418, -127.9421387],
            northEast: [53.53110886, -116.2564392],
            epicentre: [49.04, -122.08]
        },
        "acm5p0_georgiastraitfault": {
            southWest: [48.30891418, -129.0949554],
            northEast: [53.53110886, -117.2290878],
            epicentre: [49.28, -123.34]
        },
        "acm5p0_mysterylake": {
            southWest: [48.30891418, -129.0949554],
            northEast: [53.53110877, -116.8056259],
            epicentre: [49.37, -122.92]
        },
        "acm5p2_beaufortfault": {
            southWest: [48.30891569, -129.094944],
            northEast: [53.53110877, -118.7975574],
            epicentre: [49.33, -124.84]
        },
        "acm5p2_vedderfault": {
            southWest: [48.30891569, -127.9421269],
            northEast: [53.53110877, -116.2564537],
            epicentre: [49.04, -122.08]
        },
        "acm5p5_southeypoint": {
            southWest: [48.30891569, -129.094944],
            northEast: [53.53110877, -117.4908738],
            epicentre: [48.95, -123.61]
        },
        "acm5p7_southeypoint": {
            southWest: [48.30891569, -129.094944],
            northEast: [53.53110877, -117.4908738],
            epicentre: [48.95, -123.61]
        },
        "acm7p7_queencharlottefault": {
            southWest: [50.11540505, -133.1977449],
            northEast: [56.27162148, -124.9961029],
            epicentre: [53, -132.62]
        },
        "acm8p0_queencharlottefault": {
            southWest: [49.51322353, -133.1977449],
            northEast: [58.00055135, -124.9961029],
            epicentre: [53, -132.62]
        },
        "scm5p0_burlingtontorontostructuralzone": {
            southWest: [41.68143543, -86.54942531],
            northEast: [52.29313064, -71.892560649],
            epicentre: [43.49, -79.47]
        },
        "scm5p0_rougebeach": {
            southWest: [41.68143543, -86.54942531],
            northEast: [55.00064604, -69.99999997],
            epicentre: [43.78, -79.09]
        },
        "scm5p6_gloucesterfault": {
            southWest: [42.06164245, -86.54942531],
            northEast: [55.00064604, -68.38243595],
            epicentre: [43.78, -79.09]
        },
        "scm5p9_millesilesfault": {
            southWest: [42.53884243, -86.54942531],
            northEast: [55.00064604, -65.94908208],
            epicentre: [45.607, -73.82]
        },
    };

    const config = scenarioConfig[lcScenario];
    if (config) {
        const { southWest, northEast, epicentre } = config;

        const bounds = L.latLngBounds(L.latLng(...southWest), L.latLng(...northEast));
        const epicentreMarker = L.circleMarker(epicentre, circleStyle()).addTo(map);
        map.setView(L.latLng(...epicentre), 7);
    }
}



function setTileLayerStyles() {
    const tileLayerStyles = {
        "acm7p0_georgiastraitfault": "dsra_acm7p0_georgiastraitfault_indicators_s",
        "acm7p3_leechriverfullfault": "dsra_acm7p3_leechriverfullfault_indicators_s",
        "sim9p0_cascadiainterfacebestfault": "dsra_sim9p0_cascadiainterfacebestfault_indicators_s",
        "scm7p5_valdesbois": "dsra_scm7p5_valdesbois_indicators_s",
        "idm7p1_sidney": "dsra_idm7p1_sidney_indicators_s",
        "acm4p9_georgiastraitfault": "dsra_acm4p9_georgiastraitfault_indicators_s",
        "acm7p4_denalifault": "dsra_acm7p4_denalifault_indicators_s",
        "scm5p0_montreal": "dsra_scm5p0_montreal_indicators_s",
        "scm5p5_constancebay": "dsra_scm5p5_constancebay_indicators_s",
        "acm4p9_vedderfault": "dsra_acm4p9_vedderfault_indicators_s",
        "acm5p0_georgiastraitfault": "dsra_acm5p0_georgiastraitfault_indicators_s",
        "acm5p0_mysterylake": "dsra_acm5p0_mysterylake_indicators_s",
        "acm5p2_beaufortfault": "dsra_acm5p2_beaufortfault_indicators_s",
        "acm5p2_vedderfault": "dsra_acm5p2_vedderfault_indicators_s",
        "acm5p5_southeypoint": "dsra_acm5p5_southeypoint_indicators_s",
        "acm5p7_southeypoint": "dsra_acm5p7_southeypoint_indicators_s",
        "acm7p7_queencharlottefault": "dsra_acm7p7_queencharlottefault_indicators_s",
        "acm8p0_queencharlottefault": "dsra_acm8p0_queencharlottefault_indicators_s",
        "scm5p0_burlingtontorontostructuralzone": "dsra_scm5p0_burlingtontorontostructuralzone_indicators_s",
        "scm5p0_rougebeach": "dsra_scm5p0_rougebeach_indicators_s",
        "scm5p6_gloucesterfault": "dsra_scm5p6_gloucesterfault_indicators_s",
        "scm5p9_millesilesfault": "dsra_scm5p9_millesilesfault_indicators_s"
    };

    const tileLayerStyleKey = tileLayerStyles[lcScenario];
    if (tileLayerStyleKey) {
        return {
            [tileLayerStyleKey]: function(properties) {
                return tileStyle(properties);
            }
        };
    }
}



function setShakeLayerStyles(z) {
    const scenarios = {
        "acm7p0_georgiastraitfault": {
            1: "dsra_acm7p0_georgiastraitfault_shakemap_hexgrid_1km",
            5: "dsra_acm7p0_georgiastraitfault_shakemap_hexgrid_5km"
        },
        "acm7p3_leechriverfullfault": {
            1: "dsra_acm7p3_leechriverfullfault_shakemap_hexgrid_1km",
            5: "dsra_acm7p3_leechriverfullfault_shakemap_hexgrid_5km"
        },
        "sim9p0_cascadiainterfacebestfault": {
            1: "dsra_sim9p0_cascadiainterfacebestfault_shakemap_hexgrid_1km",
            5: "dsra_sim9p0_cascadiainterfacebestfault_shakemap_hexgrid_5km"
        },
        "scm7p5_valdesbois": {
            1: "dsra_scm7p5_valdesbois_shakemap_hexgrid_1km",
            5: "dsra_scm7p5_valdesbois_shakemap_hexgrid_5km"
        },
        "idm7p1_sidney": {
            1: "dsra_idm7p1_sidney_shakemap_hexgrid_1km",
            5: "dsra_idm7p1_sidney_shakemap_hexgrid_5km"
        },
        "acm4p9_georgiastraitfault": {
            1: "dsra_acm4p9_georgiastraitfault_shakemap_hexgrid_1km",
            5: "dsra_acm4p9_georgiastraitfault_shakemap_hexgrid_5km"
        },
        "acm7p4_denalifault": {
            1: "dsra_acm7p4_denalifault_shakemap_hexgrid_1km",
            5: "dsra_acm7p4_denalifault_shakemap_hexgrid_5km"
        },
        "scm5p0_montreal": {
            1: "dsra_scm5p0_montreal_shakemap_hexgrid_1km",
            5: "dsra_scm5p0_montreal_shakemap_hexgrid_5km"
        },
        "scm5p5_constancebay": {
            1: "dsra_scm5p5_constancebay_shakemap_hexgrid_1km",
            5: "dsra_scm5p5_constancebay_shakemap_hexgrid_5km"
        },
        "acm4p9_vedderfault": {
            1: "dsra_acm4p9_vedderfault_shakemap_hexgrid_1km",
            5: "dsra_acm4p9_vedderfault_shakemap_hexgrid_5km"
        },
        "acm5p0_georgiastraitfault": {
            1: "dsra_acm5p0_georgiastraitfault_shakemap_hexgrid_1km",
            5: "dsra_acm5p0_georgiastraitfault_shakemap_hexgrid_5km"
        },
        "acm5p0_mysterylake": {
            1: "dsra_acm5p0_mysterylake_shakemap_hexgrid_1km",
            5: "dsra_acm5p0_mysterylake_shakemap_hexgrid_5km"
        },
        "acm5p2_beaufortfault": {
            1: "dsra_acm5p2_beaufortfault_shakemap_hexgrid_1km",
            5: "dsra_acm5p2_beaufortfault_shakemap_hexgrid_5km"
        },
        "acm5p2_vedderfault": {
            1: "dsra_acm5p2_vedderfault_shakemap_hexgrid_1km",
            5: "dsra_acm5p2_vedderfault_shakemap_hexgrid_5km"
        },
        "acm5p5_southeypoint": {
            1: "dsra_acm5p5_southeypoint_shakemap_hexgrid_1km",
            5: "dsra_acm5p5_southeypoint_shakemap_hexgrid_5km"
        },
        "acm5p7_southeypoint": {
            1: "dsra_acm5p7_southeypoint_shakemap_hexgrid_1km",
            5: "dsra_acm5p7_southeypoint_shakemap_hexgrid_5km"
        },
        "acm7p7_queencharlottefault": {
            1: "dsra_acm7p7_queencharlottefault_shakemap_hexgrid_1km",
            5: "dsra_acm7p7_queencharlottefault_shakemap_hexgrid_5km"
        },
        "acm8p0_queencharlottefault": {
            1: "dsra_acm8p0_queencharlottefault_shakemap_hexgrid_1km",
            5: "dsra_acm8p0_queencharlottefault_shakemap_hexgrid_5km"
        },
        "scm5p0_burlingtontorontostructuralzone": {
            1: "dsra_scm5p0_burlingtontorontostructuralzone_shakemap_hexgrid_1km",
            5: "dsra_scm5p0_burlingtontorontostructuralzone_shakemap_hexgrid_5km"
        },
        "scm5p0_rougebeach": {
            1: "dsra_scm5p0_rougebeach_shakemap_hexgrid_1km",
            5: "dsra_scm5p0_rougebeach_shakemap_hexgrid_5km"
        },
        "scm5p6_gloucesterfault": {
            1: "dsra_scm5p6_gloucesterfault_shakemap_hexgrid_1km",
            5: "dsra_scm5p6_gloucesterfault_shakemap_hexgrid_5km"
        },
        "scm5p9_millesilesfault": {
            1: "dsra_scm5p9_millesilesfault_shakemap_hexgrid_1km",
            5: "dsra_scm5p9_millesilesfault_shakemap_hexgrid_5km"
        },
    };

    const scenarioStyles = scenarios[lcScenario];
    if (scenarioStyles) {
        const shakeLayerStyleKey = scenarioStyles[z];
        if (shakeLayerStyleKey) {
            return {
                [shakeLayerStyleKey]: function(properties) {
                    return shakeStyle(properties);
                }
            };
        }
    }
}
</script>
