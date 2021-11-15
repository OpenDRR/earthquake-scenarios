---
authorName: Natural Resources Canada
authorUrl:
dateModified: 2021-10-21
pageclass: wb-prettify all-pre
subject:
  en: [GV Government and Politics, Government services]
  fr: [GV Gouvernement et vie politique, Services gouvernementaux]
title: Earthquake Scenarios
lang: en
altLangPage: ../fr/
nositesearch: true
nomenu: true
nofooter: true
breadcrumbs:
  - title: "OpenDRR"
    link: https://www.github.com/OpenDRR/
  - title: "OpenDRR Downloads"
    link: "../data/en"
  - title: "Earthquake Scenarios"
---

<link href='../assets/css/app.css' rel='stylesheet'/>

<div class="row">
  <div class="col-md-8">
    <p><strong>The National Earthquake Scenario Catalogue, presents the probable shaking, damage, loss and consequences from hypothetical earthquakes that could impact Canadians.</strong></p>
    <p>It considers only damage to buildings, and their inhabitants, from earthquake shaking, and therefore does not include damage to critical infrastructure or vehicles. Losses from secondary hazards, such as aftershocks, liquefaction, landslides, or fire following are also not currently included.</p>
    <p>The information is provided at the approximate scale of Census dissemination areas, and is intended to support planning and emergency management activities in earthquake prone regions.</p>
    <p>This project is run by the Geological Survey of Canada's Public Safety Geoscience Program. For inquiries related to the National Earthquake Scenario Catalogue, please contact Tiegan E. Hobbs at <a href="mailto:tiegan.hobbs@canada.ca">tiegan.hobbs@canada.ca</a>.</p>
    <section class="jumbotron">
      <p>All products are released under the Open Government Licence - Canada.</p>
      <p><a href="https://open.canada.ca/en/open-government-licence-canada" class="btn btn-info btn-lg" role="button">Learn more</a></p>
    </section>
  </div>
  <div class="col-md-4">
    <p>
      <a href="https://github.com/OpenDRR/earthquake-scenarios" class="btn btn-info btn-lg btn-block" role="button"><i class="fab fa-github"></i> GitHub</a>
    </p>
    <div class="panel panel-primary mrgn-tp-sm">
      <div class="panel-heading">
        <div class="panel-title">Datasets</div>
      </div>
      <ul class="list-group">
      {% for scenario in site.data.dsra.scenarios %}
        <li class="list-group-item">
          <a href="#{{ scenario.name }}" style="display:block; width:inherit; overflow:hidden; white-space:nowrap; text-overflow: ellipsis;">{{ scenario.title }}</a>
        </li>
        {% endfor %}
      </ul>
    </div>
    <div class="panel panel-primary mrgn-tp-sm">
      <div class="panel-heading">
        <div class="panel-title">Distribution contact</div>
      </div>
      <ul class="list-group">
        <li class="list-group-item">
          <b>Organization name:</b><br>
          Government of Canada;Natural Resources Canada;Lands and Minerals Sector, Geological Survey of Canada
        </li>
        <li class="list-group-item">
          <b>Email:</b><br>
          <a href="mailto:GSC.info.CGC@NRCan.gc.ca">GSC.info.CGC@NRCan.gc.ca</a>
        </li>
      </ul>
    </div>
  </div>
</div>

<!-- <div class="row">
  <div class="col-md-12">
    <iframe width="100%" height="480" frameborder="0" src="https://viewscreen.githubusercontent.com/view/geojson?url=https%3a%2f%2fraw.githubusercontent.com%2fDamonU2%2fearthquake-scenarios%2fgeojson-maps%2fFINISHED%2fFinishedScenarios.geojson" title="FinishedScenarios.geojson"></iframe>
    <table style="width:100%; font-size:14px;">
      <tr>
        <td><img src="../assets/img/small.png" width='20'> Magnitude less than 6.0</td>
        <td><img src="../assets/img/medium.png" width='25'> Magnitude 6.0 to 7.9</td>
        <td><img src="../assets/img/large.png" width='30'> Magnitude 8.0 or greater</td>
      </tr>
    </table>
  </div>
</div> -->

{% assign header = '' %}
{% if page.lang == 'fr' %}
    {% assign header = '<tr>
        <th scope="col" class="col-sm-6">Nom de la ressource</th>
        <th scope="col" class="col-sm-2 hidden-xs">Type de ressource</th>
        <th scope="col" class="col-sm-2">Format</th>
        <th scope="col" class="col-sm-1">Liens</th>
    </tr>' %}
{% else %}
    {% assign header = '<tr>
        <th scope="col" class="col-sm-6">Resource Name</th>
        <th scope="col" class="col-sm-2 hidden-xs">Resource Type</th>
        <th scope="col" class="col-sm-2">Format</th>
        <th scope="col" class="col-sm-1">Links</th>
    </tr>' %}
{% endif %}

{% if page.lang == 'en' %}{% assign btntxt = "Access" %}{% else %}{% assign btntxt = "Accès" %}{% endif %}

{% for scenario in site.data.dsra.scenarios %}
  <a name="{{ scenario.name }}"></a>
  <h2 id={{ scenario.name }}>{{ scenario.title }}</h2>
  <p>
    <div class="card" style="float:left;margin:10px 20px 0px 0px;">
      <a href="dsra_scenario_map.html?scenario={{ scenario.name }}">
        <img src="https://github.com/OpenDRR/earthquake-scenarios/raw/master/FINISHED/{{ scenario.name }}.png" width="350" class="img-rounded img-responsive"/>
      </a>
      <div class="card-body">
        <a href="dsra_scenario_map.html?scenario={{ scenario.name }}" class="btn btn-primary btn-lg btn-block mrgn-tp-sm" role="button">
         {% if page.lang == 'en' %} View on Map {% else %} Voir sur la carte {% endif %}
        </a>
      </div>
      <br>
    </div>
    <div class="scenario-desc" style="word-break: break-word;">
      {{ scenario.description[page.lang] }}
    </div>
  </p>
  <div>
      <table class="table table-striped table-responsive">
          <tbody>
              {{ header }}
              <tr>
                  <td>GitHub repository</td>
                  <td class="hidden-xs">Document</td>
                  <td><span class="label HTML">HTML</span></td>
                  <td><a href="https://github.com/OpenDRR/earthquake-scenarios/blob/master/FINISHED/{{ scenario.name }}.md" class="btn btn-primary">{{ btntxt }}</a></td>
              </tr>
              <!--<tr>
                  <td>OGC API - Features (Points)</td>
                  <td class="hidden-xs">Web Service</td>
                  <td><span class="label HTML">HTML</span></td>
                  <td><a href="https://geo-api.stage.riskprofiler.ca/collections/opendrr_dsra_{{ scenario.name | downcase }}_indicators_b?lang=en-CA" class="btn btn-primary">{{ btntxt }}</a></td>
              </tr>
              <tr>
                  <td>OGC API - Features (Polygons)</td>
                  <td class="hidden-xs">Web Service</td>
                  <td><span class="label HTML">HTML</span></td>
                  <td><a href="https://geo-api.stage.riskprofiler.ca/collections/opendrr_dsra_{{ scenario.name | downcase }}_indicators_s?lang=en-CA" class="btn btn-primary">{{ btntxt }}</a></td>
              </tr>-->
              <tr>
                  <td>{{ scenario.title }} (Points)</td>
                  <td class="hidden-xs">Dataset</td>
                  <td><span class="label GPKG">GPKG</span></td>
                  <td><a href="{{site.github.releases_url}}/download/{{site.github.releases[0].tag_name}}/dsra_{{ scenario.name }}_indicators_b.zip" class="btn btn-primary">{{ btntxt }}</a></td>
                  </tr>
              <tr>
                  <td>{{ scenario.title }} (Polygons)</td>
                  <td class="hidden-xs">Dataset</td><td><span class="label GPKG">GPKG</span></td>
                  <td><a href="{{site.github.releases_url}}/download/{{site.github.releases[0].tag_name}}/dsra_{{ scenario.name }}_indicators_s.zip" class="btn btn-primary">{{ btntxt }}</a></td>
              </tr>
              <tr>
                  <td>{{ scenario.title }} ShakeMap</td>
                  <td class="hidden-xs">Dataset</td><td><span class="label GPKG">GPKG</span></td>
                  <td><a href="{{site.github.releases_url}}/download/{{site.github.releases[0].tag_name}}/dsra_{{ scenario.name }}_shakemap.zip" class="btn btn-primary">{{ btntxt }}</a></td>
              </tr>
          </tbody>
      </table>
  </div>
{% endfor %}

<script src="../assets/js/app.js"></script>

<script>

  let descriptions = document.getElementsByClassName('scenario-desc');

  for (let i = 0; i < descriptions.length; i++) {
    descriptions[i].innerHTML = urlify( descriptions[i].innerHTML );
  }

</script>
