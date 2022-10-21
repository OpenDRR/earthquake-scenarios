# Canada's National Earthquake Scenario Catalogue

Last update: 21 Oct 2022

## Overview of this Repository

Visit [www.RiskProfiler.ca](www.riskprofiler.ca) to view our user-friendly interface. Here, you can explore the information without downloading data.

This repository is used for the development of the National Earthquake Scenario Catalogue, which presents the probable shaking, damage, loss and consequences from hypothetical earthquakes that could impact Canadians. It considers only damage to buildings, and their inhabitants, from earthquake shaking, and therefore does not include damage to critical infrastructure or vehicles. Losses from secondary hazards, such as aftershocks, liquefaction, landslides, or fire following are also not currently included. The information is provided at the approximate scale of Census dissemination areas, and is intended to support planning and emergency management activities in earthquake prone regions. This project is run by the Geological Survey of Canada's Public Safety Geoscience Program. For inquiries related to the National Earthquake Scenario Catalogue, please contact Tiegan E. Hobbs at tiegan.hobbs@nrcan-rncan.gc.ca. 

For those looking for completed scenarios, please use the ['FINISHED'](./FINISHED/) directory. It contains markdown (.md) files for every published scenario, with each including a high level summary of the scenario impacts, a map of the scenario location, and links to all the output/result csv files. These markdown files can be previewed in your web browser, for easy inspection of scenarios. As more scenarios are published they will be added. A web application is currently being developed to facilitate interaction with these data for non-technical users.

## Technical Use

It is possible to download individual files from the web, by clicking on either 'Raw' or 'Download' from the top right corner of a file preview page. For those wishing to clone this repository, please ensure you have [Git LFS](https://git-lfs.github.com/) enabled on your machine prior to cloning. Earthquake risk assessments herein are completed using the [OpenQuake Engine](https://www.globalquakemodel.org/openquake) which can be cloned [here](https://github.com/gem/oq-engine). Any input files which are housed outside of this repository will be made public as soon as supporting documentation is available, including the hazard source model, site response, exposure, vulnerability and fragility functions. 

## Documentation

A Geological Survey of Canada Open File Report contains basic information about how these models are produced and provides several examples/tutorials. These are aimed at a user who wishes to inspect details of scenarios and has some minimal experience with GIS, Tableau, or Python. For example, emergency managers may find this tutorial is enough to help them identify the impacts of a scenario in their region of interest. This document is available through [GEOSCAN](https://doi.org/10.4095/328364).

Additional supporting documentation is in development and will be described here as it is published.

## A Note on Acceptable Use

These scenarios are HYPOTHETICAL, but represent credible events which may occur. This suite of scenarios is based primarily on historical earthquakes, known faults, and/or background seismicity levels consistent with [Canada's National Seismic Hazard Model](https://doi.org/10.4095/327322). It is by no means an exhaustive list of all potential scenarios that are possible.

Earthquake risk information on RiskProfiler is based on national-scale models of seismic hazard, building exposure, and building vulnerability, and represents typical conditions in any given area, but may not precisely represent local conditions. Results should not be used for building- or property-specific applications and should be interpreted in the appropriate context of a local community. All information represents the expected risk from hypothetical earthquakes. The modelling approach is subject to significant sources of uncertainty inherent in any seismic risk model. Therefore, information should be regarded as estimates, and interpreted in the context of limitations of modelling. Estimates are provided for the effect of shaking damage to buildings and inhabitants; damage from secondary hazards (aftershocks, tsunami, landslide, fire following, etc.), damage to linear infrastructure, and subsequent disruption costs are not included. RiskProfiler provides a visual representation of values, which are rounded as appropriate. See the discussion of uncertainties and intended use [here](https://riskprofiler.ca/learn-more/uncertainties-and-intended-use/index.html). As stated in the Open Government Licence – Canada, the information is provided with No Warranty. 

## Attribution

If using any of these scenarios, please include reference to any works which are cited in the scenario descriptions as well as reference to the scenario catalogue itself. The following citation should be used:

Hobbs, T.E., Journeay, J.M., Rotheram, D., 2021. An Earthquake Scenario Catalogue for Canada: A Guide to Using Scenario Hazard and Risk Results; Geological Survey of Canada, Open File 8806, 22 p. [https://doi.org/10.4095/328364](https://doi.org/10.4095/328364)

---

# Catalogue national de scénarios de tremblement de terre

Date de modification: 21 Octobre 2022

## Aperçu du dépôt

Visitez [www.RiskProfiler.ca](www.riskprofiler.ca) pour voir notre interface conviviale. Vous pourrez y explorer les informations sans avoir à télécharger de données.

Le dépôt est utilisé pour l’élaboration du catalogue national de scénarios de tremblement de terre, qui présente les secousses, les dommages, les pertes et les conséquences probables de tremblements de terre hypothétiques qui pourraient frapper la population canadienne. Le catalogue ne comporte que les dommages causés aux immeubles et à leurs habitants et ne comprend donc pas les dommages causés aux infrastructures essentielles ou aux véhicules. À l’heure actuelle, il ne comprend pas non plus les pertes causées par les dangers secondaires, comme les répliques, la liquéfaction, les glissements de terrain ou les feux. Les renseignements sont présentés selon une échelle qui correspond approximativement aux aires de diffusion du recensement et visent à soutenir les activités de planification et de gestion des urgences dans les régions sujettes aux tremblements de terre. Le projet est mené par les responsables du programme Géoscience pour la sécurité publique de la Commission géologique du Canada. Pour toute question sur le catalogue national de scénarios de tremblement de terre, veuillez communiquer avec Tiegan E. Hobbs à tiegan.hobbs@nrcan-rncan.gc.ca.

Si vous souhaitez consulter des scénarios complets, veuillez utiliser le dépôt « FINISHED » (en anglais seulement). Il contient des fichiers Markdown (.md) pour chaque scénario publié, et chaque scénario comprend un résumé général des répercussions associées au scénario, une carte de l’emplacement utilisé et des liens vers tous les fichiers de résultats .csv. Il est possible de prévisualiser ces fichiers Markdown dans votre navigateur Web pour faciliter l’examen des scénarios. Les scénarios seront ajoutés à mesure qu’ils seront publiés. On élabore actuellement une application Web pour que les utilisateurs qui ne possèdent pas de connaissances techniques puissent aisément consulter les données.

## Utilisation technique

Il est possible de télécharger des fichiers individuels sur le Web, il suffit de cliquer sur « Raw » ou « Download » dans le coin supérieur droit d’une page de prévisualisation d’un fichier. Si vous souhaitez produire un clone de ce dépôt, assurez-vous d’avoir l’extension Git Large File Storage (en anglais seulement) sur votre ordinateur avant d’effectuer l’opération. Les évaluations de risques de tremblements de terre sont réalisées à l’aide d’OpenQuake Engine (en anglais seulement) qui peut être copié à partir de GitHub (en anglais seulement). Tout fichier de résultat hébergé à l’extérieur du dépôt sera rendu public aussitôt que les documents à l’appui seront disponibles, y compris le modèle de la source de danger, l’intervention sur place, l’exposition et les fonctions de vulnérabilité et de fragilité.

## Documents

Un rapport public de la Commission géologique du Canada contient des renseignements de base sur la façon dont les modèles sont produits et comprend plusieurs exemples ou tutoriels. Ces exemples et tutoriels sont conçus pour les utilisateurs qui souhaitent examiner les détails des scénarios, mais qui possèdent peu d’expérience de l’utilisation de systèmes d’information géographique, de Tableau ou de Python. Par exemple, les gestionnaires des urgences pourraient trouver qu’un tutoriel est suffisant pour leur permettre de repérer les effets d’un scénario dans la région qui les intéressent. Le document est disponible sur GEOSCAN (en anglais seulement).

Des documents à l’appui supplémentaires sont en cours d’élaboration et une description sera ajoutée ici à mesure qu’ils seront publiés.

## Remarque sur l’utilisation acceptable

Les scénarios sont HYPOTHÉTIQUES, mais ils représentent des événements envisageables. Cet ensemble de scénarios est fondé principalement sur des tremblements de terre antérieurs ou des niveaux de sismicité de référence qui correspondent au Seismic Hazard Model of Canada (en anglais seulement – modèle d’aléa sismique du Canada). Il ne s’agit en aucun cas d’une liste exhaustive de tous les scénarios possibles. 

Les informations relatives au risque sismique sur RiskProfiler sont basées sur des modèles à l'échelle nationale de l'aléa sismique, de l'exposition et de la vulnérabilité des bâtiments, et représentent les conditions typiques d'une zone donnée, mais peuvent ne pas représenter précisément les conditions locales. Les résultats ne doivent pas être utilisés pour des applications spécifiques aux bâtiments ou aux propriétés et doivent être interprétés dans le contexte approprié d'une communauté locale. Toutes les informations représentent le risque attendu de séismes hypothétiques. L'approche de modélisation est soumise à d'importantes sources d'incertitude inhérentes à tout modèle de risque sismique. Par conséquent, les informations doivent être considérées comme des estimations, et interprétées dans le contexte des limites de la modélisation. Les estimations sont fournies pour l'effet des dommages causés par les secousses aux bâtiments et aux habitants ; les dommages causés par les risques secondaires (répliques, tsunami, glissement de terrain, incendie consécutif, etc.), les dommages aux infrastructures linéaires et les coûts des perturbations ultérieures ne sont pas inclus. RiskProfiler fournit une représentation visuelle des valeurs, qui sont arrondies comme il convient. Voir la discussion sur les incertitudes et l'utilisation prévue [ici] (https://riskprofiler.ca/learn-more/uncertainties-and-intended-use/index.html). Comme indiqué dans la Licence de gouvernement ouvert - Canada, les informations sont fournies sans garantie. 

## Attribution

Si vous utilisez l’un de ces scénarios, veuillez ajouter un renvoi aux travaux qui sont cités dans les descriptions de scénarios ainsi qu’un renvoi au catalogue de scénarios. La référence suivante devrait être utilisée :

Hobbs, T.E., Journeay, J.M., Rotheram, D., 2021. An Earthquake Scenario Catalogue for Canada: A Guide to Using Scenario Hazard and Risk Results; Geological Survey of Canada, Open File 8806, 22 p. https://doi.org/10.4095/328364
