---
authorName: Natural Resources Canada
authorUrl:
dateModified: 2021-07-26
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
    link: "../data/fr"
  - title: "Scénarios de tremblement de terre"
    link: "/fr"
  - title: "Carte des scénarios de tremblement de terre"
    link: "/fr/dsra_scenario_map"
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

<script src="https://code.jquery.com/jquery-3.6.0.min.js" integrity="sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4=" crossorigin="anonymous"></script>

<link href='../assets/css/app.css' rel='stylesheet'/>

<div id="map"></div>
<div id="sidebar"></div>

<div id="alert">Impossible de charger le scénario</div>
<div id="scenarios">
  <h5>Scénarios disponibles:</h5>
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
    center: [ 57, -100 ],
    zoom: 4}),
    legend = L.control( { position: 'bottomright' } ),
    params = new URLSearchParams(window.location.search), // Get query paramaters
    baseUrl = "https://geo-api.stage.riskprofiler.ca/collections/opendrr_dsra_",
    eqScenario = params.get( 'scenario' ), // Scenario name
    featureProperties = 'Sauid,sCt_Res90_b0', // Limit fetched properties for performance
    scenarioProp = 'sCt_Res90_b0', // Property for popup and feature colour
    limit = 500,
    selection;
    

  L.tileLayer( '//{s}.tile.osm.org/{z}/{x}/{y}.png', {
		attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
	}).addTo( map );

  const geojsonLayer = L.geoJSON([], {
        style: featureStyle,
        onEachFeature: geoJsonOnEachFeature
      }).addTo( map );

  if ( eqScenario ) {

    $("#scenarios").hide();

    var scenario = eqScenario.toLowerCase(); // API uses lowercase
      geojsonUrl = baseUrl + scenario + "_indicators_s/items?lang=en_US&f=json&limit=" + limit  + '&properties=' + featureProperties,
      featureUrl = baseUrl + scenario + "_indicators_s/items/";

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

    // Add progress modal to map before fetching geoJSON
    $( '#map' ).before( '<div id="modal"></div>' );
    getData( geojsonUrl );

    map.on( 'fullscreenchange', function () {
      map.invalidateSize();
    });
  }
  
  // Get all geoJSON for scenario
  function getData( url ) {
    
    var nxt_lnk;

    $.getJSON( url, function ( data ) {
      
      geojsonLayer.addData( data );

      for ( var l in data.links ) {
        lnk = data.links[ l ];
        if ( lnk.rel == 'next' ) {
          nxt_lnk = lnk.href;
          break;
        }
      }
      
      // if next link continue loading data
      if ( nxt_lnk ) {
        getData( nxt_lnk );
      } else {
        // set map bounds to frame loaded features
        map.fitBounds(geojsonLayer.getBounds());
        // done with paging so remove progress
        $( '#modal' ).remove();
        // Add legend
        legend.addTo( map );
      }
    })
    .fail( function ( jqXHR, error ) {
      $( '#alert' ).show();
      $( '#modal' ).remove();
      $( '#scenarios' ).show();
    });
  }

  // Handles events for each feature
  function geoJsonOnEachFeature( feature, layer ){
    layer.bindPopup( function ( e ) {
      return L.Util.template( '<p>Residents displaced after 90 days: <strong>' + e.feature.properties.sCt_Res90_b0.toLocaleString( undefined, { maximumFractionDigits: 0 }) + '</strong></p>' );
    }).on({
      click: function( e ) {
        if ( selection ) {
          // reset style of previously selected feature
          selection.setStyle(featureStyle(selection.feature));
        }
        selection = e.target;
        selection.setStyle(selectedStyle());

        // Get geoJSON of selected feature
        $.ajax({
          method: "GET",
          tryCount : 0,
          retryLimit : 3,
          crossDomain: true,
          url: featureUrl +  selection.feature.id,
          headers: { "content-type": "application/json" }
        })

        // Displays properties of selection in a table
        .done( function ( resp ) {

          let props = resp.properties,
             string = '<table class="table table-striped table-responsive"><tr>';

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
            else if ( key === 'OBJECTID' || key === 'SHAPE_Length' || key === 'SHAPE_Area' || key === 'geom_poly' ) {
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
        })

        .fail( function ( error ) {
        this.tryCount++;
        if ( this.tryCount <= this.retryLimit ) {
            //try again
            $.ajax( this );
            return;
        }   
        console.log( "Doh! " + error )    
        return;
        
        });
      }
    });
  };

  function getColor( d ) {
      return d > 300  ? '#ff3b00' :
          d > 100   ? '#ff6500' :
          d > 50   ? '#ff9000' :
          d > 10   ? '#ffba00' :
                      '#fff176';
  }

  legend.onAdd = function ( map ) {

    var div = L.DomUtil.create('div', 'info legend'),
        grades = [0, 10, 50, 100, 300],
        label = ' Personnes déplacées';

    div.innerHTML = "<div style=\"padding: 3px;\"><b>Personnes déplacées après 90 jours</b></div>";

    // loop through our density intervals and generate a label with a colored square for each interval
    for (var i = 0; i < grades.length; i++ ) {
        div.innerHTML +=
            '<i style="background:' + getColor(grades[i] + 1) + '"></i> ' +
            grades[i] + ( grades[i + 1] ? '&ndash;' + grades[i + 1] + label + '<br>' : '+' + label);
    }

    return div;
  };
  
  function featureStyle( feature ) {
    return {
        fillColor: getColor( feature.properties[ scenarioProp ] ),
        weight: 0.6,
        fillOpacity: 0.7,
        color: '#4b4d4d',
        opacity: 1
    };
  }

  function selectedStyle( feature ) {
      return {
        fillColor: 'blue',
        color: 'black',
        weight: 1,
        fillOpacity: 0.5
    };
  }

</script>

<style>
  #alert {
    display: none;
    background: rgb(220, 20, 20);
    color: white;
    padding: 5px;
  }
</style>