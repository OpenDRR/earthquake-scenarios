---
authorName: Natural Resources Canada
authorUrl:
dateModified: 2021-05-07
pageclass: wb-prettify all-pre
subject:
  en: [GV Government and Politics, Government services]
  fr: [GV Gouvernement et vie politique, Services gouvernementaux]
title: Scénarios de séismes
lang: fr
altLangPage: ../en
nositesearch: true
nomenu: true
nofooter: true
breadcrumbs:
  - title: "OpenDRR"
    link: "https://www.github.com/OpenDRR/"
  - title: "Téléchargements de OpenDRR"
    link: "../data/fr"
  - title: "Scénarios de séismes"
---

<link href='../assets/css/app.css' rel='stylesheet'/>

<div class="row">
  <div class="col-md-8">
    <p><strong>Le dépôt est utilisé pour l’élaboration du catalogue national de scénarios de tremblement de terre, qui présente les secousses, les dommages, les pertes et les conséquences probables de tremblements de terre hypothétiques qui pourraient frapper la population canadienne.</strong></p>
    <p>Le catalogue ne comporte que les dommages causés aux immeubles et à leurs habitants et ne comprend donc pas les dommages causés aux infrastructures essentielles ou aux véhicules. À l’heure actuelle, il ne comprend pas non plus les pertes causées par les dangers secondaires, comme les répliques, la liquéfaction, les glissements de terrain ou les feux.</p>
    <p>Les renseignements sont présentés selon une échelle qui correspond approximativement aux aires de diffusion du recensement et visent à soutenir les activités de planification et de gestion des urgences dans les régions sujettes aux tremblements de terre.</p>
    <p>Le projet est mené par les responsables du programme Géoscience pour la sécurité publique de la Commission géologique du Canada. Pour toute question sur le catalogue national de scénarios de tremblement de terre, veuillez communiquer avec Tiegan E. Hobbs à <a href="tiegan.hobbs@canada.ca">tiegan.hobbs@canada.ca</a>.</p>
    <section class="jumbotron">
      <p>Tous les produits sont publiés sous la licence du gouvernement ouvert – Canada.</p>
      <p><a href="https://ouvert.canada.ca/fr/licence-du-gouvernement-ouvert-canada" class="btn btn-info btn-lg" role="button">Voir</a></p>
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
        <div class="panel-title">Personne-ressource responsable de la distribution</div>
      </div>
      <ul class="list-group">
        <li class="list-group-item">
          <b>Nom de l'organisation:</b><br>
          Gouvernement du Canada;Ressources naturelles Canada;Secteur des terres et des minéraux, Commission géologique du Canada
        </li>
        <li class="list-group-item">
          <b>Courriel:</b><br>
          <a href="mailto:GSC.info.CGC@NRCan.gc.ca">GSC.info.CGC@NRCan.gc.ca</a>
        </li>
      </ul>
    </div>
  </div>
</div>

<h3>Scénarios Sélectionnés</h3>

<div class="row">
  <div class="col-md-12">
    <iframe width="100%" height="480" frameborder="0" src="https://viewscreen.githubusercontent.com/view/geojson?url=https%3a%2f%2fraw.githubusercontent.com%2fDamonU2%2fearthquake-scenarios%2fauto-updates-for-pages%2fFINISHED%2fFinishedScenariosFr.geojson" title="FinishedScenariosFr.geojson"></iframe>
    <table style="width:100%; font-size:14px;">
      <tr>
        <td><img src="../assets/img/small.png" width='20'> Magnitude < 6.0</td>
        <td><img src="../assets/img/medium.png" width='25'> Magnitude 6.0 - 7.9</td>
        <td><img src="../assets/img/large.png" width='30'> Magnitude 8.0+</td>
      </tr>
    </table>
  </div>
</div>

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
  <h4 id={{ scenario.name }}>{{ scenario.title }}</h4>
  <p>
    <div class="card" style="float:left;margin:10px 20px 0px 0px;">
      <img src="https://github.com/OpenDRR/earthquake-scenarios/raw/master/FINISHED/{{ scenario.name }}.png" width="350" class="img-rounded img-responsive"/>
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
              <tr>
                  <td>Riskprofiler Page (Points)</td>
                  <td class="hidden-xs">Web Service</td>
                  <td><span class="label HTML">HTML</span></td>
                  <td><a href="https://geo-api.stage.riskprofiler.ca/collections/opendrr_dsra_{{ scenario.name | downcase}}_indicators_b" class="btn btn-primary">{{ btntxt }}</a></td>
              </tr>
              <tr>
                  <td>Riskprofiler Page (Polygons)</td>
                  <td class="hidden-xs">Web Service</td>
                  <td><span class="label HTML">HTML</span></td>
                  <td><a href="https://geo-api.stage.riskprofiler.ca/collections/opendrr_dsra_{{ scenario.name | downcase }}_indicators_s" class="btn btn-primary">{{ btntxt }}</a></td>
              </tr>
              <tr>
                  <td>{{ scenario.title }} (Points)</td>
                  <td class="hidden-xs">Dataset</td>
                  <td><span class="label GPKG">GPKG</span></td>
                  <td><a href="https://github.com/OpenDRR/earthquake-scenarios/blob/master/FINISHED/{{ scenario.name }}_indicators_b.gpkg.zip" class="btn btn-primary">{{ btntxt }}</a></td>
                  </tr>
              <tr>
                  <td>{{ scenario.title }} (Polygons)</td>
                  <td class="hidden-xs">Dataset</td><td><span class="label GPKG">GPKG</span></td>
                  <td><a href="https://github.com/OpenDRR/earthquake-scenarios/blob/master/FINISHED/{{ scenario.name }}_indicators_s.gpkg.zip" class="btn btn-primary">{{ btntxt }}</a></td>
              </tr>
          </tbody>
      </table>
  </div>
{% endfor %}

<script>

  var urlRegex = /(\b(https?|ftp|file):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/ig,
    descriptions = document.getElementsByClassName('scenario-desc');

  for (let i = 0; i < descriptions.length; i++) {
    descriptions[i].innerHTML = urlify( descriptions[i].innerHTML );
  }

  function urlify( text ) {
    return text.replace( urlRegex, function( url ) {
      return '<a href="' + url + '">' + url + '</a>';
    })
  }

</script>
