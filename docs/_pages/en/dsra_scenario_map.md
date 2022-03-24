---
authorName: Natural Resources Canada
authorUrl:
dateModified: 2022-03-24
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

<div id="alert">Unable to load scenario</div>
<div id="scenarios">
  <h5>Available scenarios:</h5>
  <ul>
    {% for scenario in site.data.dsra.scenarios %}
      <li><a href="{{ context.environments.first["page"]["url"] }}?scenario={{scenario.name}}"><small>{{ scenario.title }}</small></a></li>
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
    center: [ 49.2576508,-123.2639868 ],
    maxZoom: 15,
    minZoom: 7,
    zoom: 8}),
    bounds, // Bounds of the tileset, set according to scenario
    legend = L.control( { position: 'bottomright' } ),
    params = new URLSearchParams( window.location.search ), // Get query paramaters
    baseUrl = "https://riskprofiler.ca/dsra_",
    eqScenario = params.get( 'scenario' ), // Scenario name
    scenarioProp = 'sCt_Res90_b0', // Property for popup and feature colour
    selection = 0; // Id of a selected feature
    

  L.tileLayer( '//{s}.tile.osm.org/{z}/{x}/{y}.png', {
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
      getFeatureId: function(feature) {
        return feature.properties[ "Sauid" ];
      },
      bounds: bounds,
      vectorTileLayerStyles: setTileLayerStyles()
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
    mag = eqScenario[ 3 ] + '.' + eqScenario[ 5 ];
    full_name = title + ' - Magnitude ' + mag;

    // Replace generic title with scenario name
    $( '#wb-cont' ).html( full_name );

    var vectorUrl = baseUrl + lcScenario + "_indicators_s/EPSG_900913/{z}/{x}/{y}.pbf";

    var sauidLayer = L.vectorGrid.protobuf( vectorUrl, vectorTileOptions ).addTo( map );

    buildLegend();

    map.on( 'fullscreenchange', function () {
      map.invalidateSize();
    })

    sauidLayer.on( 'click', function ( e ) {
      // if we have a selected feature reset the style
      if ( selection != 0 ) {
        sauidLayer.resetFeatureStyle( selection );
      }

      // set the selected feature id
      selection = e.layer.properties[ 'Sauid' ];

      // set the selected feature style
      setTimeout( function () {
        sauidLayer.setFeatureStyle( selection, selectedStyle(), 100 );
      });

      // Add a popup with desired property
      L.popup().setContent( "<strong>Residents affected after 90 days: </strong>" + e.layer.properties.sCt_Res90_b0.toString() )
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
          mod = ' (Baseline)';
        }
        else if ( key.slice( -3 ) === '_r1' ) {
          mod_key = key.slice( 0, -3 );
          mod = ' (Retrofit)';
        }
        else if ( key.slice( -3 ) === '_le' ) {
          mod_key = key.slice( 0, -3 );
          mod = ' (Seismic Upgrade)';
        }

        desc = window[ mod_key + 'Desc' ];
        detail = window[ mod_key + 'Detail' ];
        format = window[ mod_key + 'Format' ];
        value = props[ key ];

        if ( format && value ) { // Format values with set formatting
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
        else if ( desc ) { // For properties with descriptions but null values
          string +=
            '<td class="attr"><div class="prop" title="' + detail + '">' + desc + mod + '</div><div class="val">' + value + '</div></td>';
        }
        else { // Properties with no descriptions
          string +=
            '<td class="attr"><div class="prop">' + key + '</div><div class="val">' + value + '</div></td>';
        }
        if ( counter % 3 === 0 ) {
          string += '</tr><tr>';
        }
        counter++;
      }
      string += '</tr></table>';
      // Add table to sidebar div
      $( '#sidebar' ).html( '<h3>Properties of Selected Feature</h3>' + string );

    });
  }
  else {
    $( '#alert' ).show();
  }

  function getColor( d ) {
    return d > 300  ? '#ff3b00' :
      d > 100   ? '#ff6500' :
      d > 50   ? '#ff9000' :
      d > 10   ? '#ffba00' :
                  '#fff176';
  }

  function buildLegend () {
    legend.onAdd = function ( map ) {

      var div = L.DomUtil.create('div', 'info legend'),
          grades = [0, 10, 50, 100, 300],
          label = ' People Affected';

      div.innerHTML = "<div style=\"padding: 3px;\"><b>People affected after 90 days</b></div>";

      // loop through our density intervals and generate a label with a colored square for each interval
      for (var i = 0; i < grades.length; i++ ) {
          div.innerHTML +=
              '<i style="background:' + getColor( grades[i] + 1 ) + '"></i> ' +
              grades[i] + ( grades[i + 1] ? '&ndash;' + grades[i + 1] + label + '<br>' : '+' + label);
      }

      return div;
    };

    legend.addTo( map );
  }

  function setBounds() {
    if ( lcScenario == "acm7p0_georgiastraitfault" ) {
      southWest = L.latLng( 48.30891568624434, -128.4312145637652 );
      northEast = L.latLng( 52.9384673469385, -117.8488971573044 );
      bounds = L.latLngBounds( southWest, northEast );
      map.setView(new L.LatLng( 49.243365, -123.62296 ), 9);
    }
    else if ( lcScenario == "acm7p3_leechriverfullfault" ) {
      southWest = L.latLng( 48.30891568624434, -128.4312145637652 );
      northEast = L.latLng( 52.14386926906652, -118.0499496202695 );
      bounds = L.latLngBounds( southWest, northEast );
      map.setView(new L.LatLng( 48.407017, -123.412134 ), 9);
    }
    else if ( lcScenario == "sim9p0_cascadiainterfacebestfault" ) {
      southWest = L.latLng( 48.30891568624434, -132.4247727702572 );
      northEast = L.latLng( 58.50213289213824, -114.475795596884 );
      bounds = L.latLngBounds( southWest, northEast );
      map.setView(new L.LatLng( 48.251246, -125.215269 ), 8);
    }
    else if ( lcScenario == "scm7p5_valdesbois" ) {
      southWest = L.latLng( 42.50576656719492, -83.68507351241767 );
      northEast = L.latLng( 50.42592946883574, -68.22419753341977 );
      bounds = L.latLngBounds( southWest, northEast );
      map.setView(new L.LatLng( 45.905377, -75.494669 ), 8);
    }
    else if ( lcScenario == "idm7p1_sidney" ) {
      southWest = L.latLng( 48.30891568624434, -128.1932571619549 );
      northEast = L.latLng( 52.33305028176196, -117.77207886844 );
      bounds = L.latLngBounds( southWest, northEast );
      map.setView(new L.LatLng( 48.618961, -123.299385 ), 9);
    }
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

  function setTileLayerStyles() {
    if ( lcScenario == "acm7p0_georgiastraitfault" ) {
      return {
        dsra_acm7p0_georgiastraitfault_indicators_s: function ( properties ) {
          return tileStyle( properties );
        }
      }
    }
    else if ( lcScenario == "acm7p3_leechriverfullfault" ) {
      return {
        dsra_acm7p3_leechriverfullfault_indicators_s: function ( properties ) {
          return tileStyle( properties );
        }
      }
    }
    else if ( lcScenario == "sim9p0_cascadiainterfacebestfault" ) {
      return {
        dsra_sim9p0_cascadiainterfacebestfault_indicators_s: function ( properties ) {
          return tileStyle( properties );
        }
      }
    }
    else if ( lcScenario == "scm7p5_valdesbois" ) {
      return {
        dsra_scm7p5_valdesbois_indicators_s: function ( properties ) {
          return tileStyle( properties );
        }
      }
    }
    else if ( lcScenario == "idm7p1_sidney" ) {
      return {
        dsra_idm7p1_sidney_indicators_s: function ( properties ) {
          return tileStyle( properties );
        }
      }
    }
  }

  function selectedStyle( feature ) {
    return {
      fill: true,
      fillColor: 'blue',
      color: 'black',
      weight: 1,
      fillOpacity: 0.5
    };
  }

</script>
