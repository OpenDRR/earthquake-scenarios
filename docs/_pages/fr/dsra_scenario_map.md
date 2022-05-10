---
authorName: Natural Resources Canada
authorUrl:
dateModified: 2022-03-24
noContentTitle: true
pageclass: wb-prettify all-pre
subject:
  en: [GV Government and Politics, Government services]
  fr: [GV Gouvernement et vie politique, Services gouvernementaux]
title: Carte des scénarios de tremblement de terre
lang: fr
altLangPage: ../en/dsra_scenario_map.html
nositesearch: true
nomenu: true
nofooter: true
breadcrumbs:
  - title: "OpenDRR"
    link: "https://www.github.com/OpenDRR/"
  - title: "Téléchargements de OpenDRR"
    link: "../downloads/fr"
  - title: "Scénarios de tremblement de terre"
    link: "/fr"
  - title: "Carte des scénarios de tremblement de terre"
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
      crs: L.CRS.EPSG4326,
      center: [ 57, -100 ],
      maxZoom: 13,
      minZoom: 6,
      zoom: 6}),
      bounds, // Bounds for the tileset, set according to scenario
      legend = L.control( { position: 'bottomright' } ),
      params = new URLSearchParams( window.location.search ), // Get query paramaters
      baseUrl = "https://riskprofiler.ca/dsra_",
      shakeBaseUrl = "https://geo-api.stage.riskprofiler.ca/collections/opendrr_dsra_",
      eqScenario = params.get( 'scenario' ), // Scenario name
      shakemapProp = 'sH_PGA_max', // Property for shakemap popup
      scenarioProp = 'sCt_Res90_b0', // Property for popup and feature colour
      shakeCurrent = true,
      epicenter,
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
    $( '#wb-cont' ).html( full_name );

    var vectorUrl = baseUrl + lcScenario + "_indicators_s/EPSG_4326/{z}/{x}/{y}.pbf",
        shakemapUrl1 = baseUrl + lcScenario + "_shakemap_hexbin_1km/EPSG_4326/{z}/{x}/{y}.pbf",
        shakemapUrl5 = baseUrl + lcScenario + "_shakemap_hexbin_5km/EPSG_4326/{z}/{x}/{y}.pbf";

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
        epicenter.bringToFront();
      });

    var shakeLayer1km = L.vectorGrid.protobuf( shakemapUrl1, shakeTileOptions( 1 ) )
        .on( 'add', function () {
        shakeCurrent = true;
        // Add loading modal
        $( '#map' ).before( '<div id="modal"></div>' );
      }).on( 'load', function () {
        // Remove loading modal
        $( '#modal' ).remove();
        epicenter.bringToFront();
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
        epicenter.bringToFront();
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
            '<br><div>🔴 <b>{% if page.lang == 'en' %}Epicenter{% else %}Épicentre{% endif %}</b></div>';
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
            '<br><div>🔴 <b>{% if page.lang == 'en' %}Epicenter{% else %}Épicentre{% endif %}</b></div>';
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

    if ( lcScenario == "acm7p0_georgiastraitfault" ) {
      southWest = L.latLng( 48.30891568624434, -128.4312145637652 );
      northEast = L.latLng( 52.9384673469385, -117.8488971573044 );
      bounds = L.latLngBounds( southWest, northEast );
      epicenter = L.circleMarker( [ 49.243365, -123.62296 ], circleStyle() ).addTo( map );
      map.setView(new L.LatLng( 49.243365, -123.62296 ), 7);
    }
    else if ( lcScenario == "acm7p3_leechriverfullfault" ) {
      southWest = L.latLng( 48.30891568624434, -128.4312145637652 );
      northEast = L.latLng( 52.14386926906652, -118.0499496202695 );
      bounds = L.latLngBounds( southWest, northEast );
      epicenter = L.circleMarker( [ 48.407017, -123.412134 ], circleStyle() ).addTo( map );
      map.setView(new L.LatLng( 48.407017, -123.412134 ), 7);
    }
    else if ( lcScenario == "sim9p0_cascadiainterfacebestfault" ) {
      southWest = L.latLng( 48.30891568624434, -132.4247727702572 );
      northEast = L.latLng( 58.50213289213824, -114.475795596884 );
      bounds = L.latLngBounds( southWest, northEast );
      epicenter = L.circleMarker( [ 48.251246, -125.215269 ], circleStyle() ).addTo( map );
      map.setView(new L.LatLng( 48.251246, -125.215269 ), 7);
    }
    else if ( lcScenario == "scm7p5_valdesbois" ) {
      southWest = L.latLng( 42.50576656719492, -83.68507351241767 );
      northEast = L.latLng( 50.42592946883574, -68.22419753341977 );
      bounds = L.latLngBounds( southWest, northEast );
      epicenter = L.circleMarker( [ 45.905377, -75.494669 ], circleStyle() ).addTo( map );
      map.setView(new L.LatLng( 45.905377, -75.494669 ), 7);
    }
    else if ( lcScenario == "idm7p1_sidney" ) {
      southWest = L.latLng( 48.30891568624434, -128.1932571619549 );
      northEast = L.latLng( 52.33305028176196, -117.77207886844 );
      bounds = L.latLngBounds( southWest, northEast );
      epicenter = L.circleMarker( [ 48.618961, -123.299385 ], circleStyle() ).addTo( map );
      map.setView(new L.LatLng( 48.618961, -123.299385 ), 7);
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

  function setShakeLayerStyles( z ) {

    if ( lcScenario == "acm7p0_georgiastraitfault" ) {
      if ( z == 1 ) {
        return {
          dsra_acm7p0_georgiastraitfault_shakemap_hexbin_1km: function ( properties ) {
            return shakeStyle( properties );
          }
        }
      }
      else {
        return {
          dsra_acm7p0_georgiastraitfault_shakemap_hexbin_5km: function ( properties ) {
            return shakeStyle( properties );
          }
        }
      }
    }
    else if ( lcScenario == "acm7p3_leechriverfullfault" ) {
      if ( z == 1 ) {
        return {
          dsra_acm7p3_leechriverfullfault_shakemap_hexbin_1km: function ( properties ) {
            return shakeStyle( properties );
          }
        }
      }
      else {
        return {
          dsra_acm7p3_leechriverfullfault_shakemap_hexbin_5km: function ( properties ) {
            return shakeStyle( properties );
          }
        }
      }
    }
    else if ( lcScenario == "sim9p0_cascadiainterfacebestfault" ) {
      if ( z == 1 ) {
        return {
          dsra_sim9p0_cascadiainterfacebestfault_shakemap_hexbin_1km: function ( properties ) {
            return shakeStyle( properties );
          }
        }
      }
      else {
        return {
          dsra_sim9p0_cascadiainterfacebestfault_shakemap_hexbin_5km: function ( properties ) {
            return shakeStyle( properties );
          }
        }
      }
    }
    else if ( lcScenario == "scm7p5_valdesbois" ) {
      if ( z == 1 ) {
        return {
          dsra_scm7p5_valdesbois_shakemap_hexbin_1km: function ( properties ) {
            return shakeStyle( properties );
          }
        }
      }
      else {
        return {
          dsra_scm7p5_valdesbois_shakemap_hexbin_5km: function ( properties ) {
            return shakeStyle( properties );
          }
        }
      }
    }
    else if ( lcScenario == "idm7p1_sidney" ) {
      if ( z == 1 ) {
        return {
          dsra_idm7p1_sidney_shakemap_hexbin_1km: function ( properties ) {
            return shakeStyle( properties );
          }
        }
      }
      else {
        return {
          dsra_idm7p1_sidney_shakemap_hexbin_5km: function ( properties ) {
            return shakeStyle( properties );
          }
        }
      }
    }
  }


</script>
