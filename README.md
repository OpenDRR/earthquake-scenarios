# Canada's National Earthquake Scenario Catalogue
Last update: 28 May 2021

## Overview of this Repository
This repository is used for the development of the National Earthquake Scenario Catalogue, which presents the probable shaking, damage, loss and consequences from hypothetical earthquakes that could impact Canadians. It considers only damage to buildings, and their inhabitants, from earthquake shaking, and therefore does not include damage to critical infrastructure or vehicles. Losses from secondary hazards, such as aftershocks, liquefaction, landslides, or fire following are also not currently included. The information is provided at the approximate scale of Census dissemination areas, and is intended to support planning and emergency management activities in earthquake prone regions. This project is run by the Geological Survey of Canada's Public Safety Geoscience Program. For inquiries related to the National Earthquake Scenario Catalogue, please contact Tiegan E. Hobbs at tiegan.hobbs@canada.ca. 

For those looking for completed scenarios, please use the ['FINISHED'](./FINISHED/) directory. It contains markdown (.md) files for every published scenario, with each including a high level summary of the scenario impacts, a map of the scenario location, and links to all the output/result csv files. These markdown files can be previewed in your web browser, for easy inspection of scenarios. As more scenarios are published they will be added. A web application is currently being developed to facilitate interaction with these data for non-technical users. 

## Technical Use
It is possible to download individual files from the web, by clicking on either 'Raw' or 'Download' from the top right corner of a file preview page. For those wishing to clone this repository, please ensure you have [Git LFS](https://git-lfs.github.com/) enabled on your machine prior to cloning. Earthquake risk assessments herein are completed using the [OpenQuake Engine](https://www.globalquakemodel.org/openquake) which can be cloned [here](https://github.com/gem/oq-engine). Any input files which are housed outside of this repository will be made public as soon as supporting documentation is available, including the hazard source model, site response, exposure, vulnerability and fragility functions. 

## Documentation
A Geological Survey of Canada Open File Report contains basic information about how these models are produced and provides several examples/tutorials. These are aimed at a user who wishes to inspect details of scenarios and has some minimal experience with GIS, Tableau, or Python. For example, emergency managers may find this tutorial is enough to help them identify the impacts of a scenario in their region of interest. This document is available through [GEOSCAN](https://doi.org/10.4095/328364).

Additional supporting documentation is in development and will be described here as it is published.

## A Note on Acceptable Use
These scenarios are HYPOTHETICAL, but represent credible events which may occur. This suite of scenarios is based primarily on historical earthquakes, known faults, and/or background seismicity levels consistent with [Canada's National Seismic Hazard Model](https://doi.org/10.4095/327322). It is by no means an exhaustive list of all potential scenarios that are possible.

This modelling approach uses state of the art techniques and data, but is subject to significant sources of uncertainty inherent in any seismic risk model. Therefore, scenarios should be regarded as estimates, representing the average result of thousands of realizations of model parameters. Furthermore, the exposure model used herein is a representative inventory rather than a true database of the built environment. Results are not to be used for any building- or site-specific application, or any other domain which would require oversight by an accredited professional. The results may be used in aggregate for estimating the likely impacts of certain representative earthquake scenarios on a region of interest such as a municipality or regional district. For any questions on the appropriate use of these data, please contact our team.

## Attribution
If using any of these scenarios, please include reference to any works which are cited in the scenario descriptions as well as reference to the scenario catalogue itself. The following citation should be used:

Hobbs, T.E., Journeay, J.M., Rotheram, D., 2021. An Earthquake Scenario Catalogue for Canada: A Guide to Using Scenario Hazard and Risk Results; Geological Survey of Canada, Open File 8806, 22 p. [https://doi.org/10.4095/328364](https://doi.org/10.4095/328364)
