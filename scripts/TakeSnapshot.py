#!/usr/bin/python3
# SPDX-License-Identifier: MIT
#
# Copyright (C) 2020-2023 Government of Canada
#
# Script to produce a pager-style output for scenario earthquakes.
# You need to have created the rupture, damage, consequence, and loss files
# already. Run from in FINISHED dir. Written by Tiegan E. Hobbs on 3 November 2020.
#
# Seems you need to be out of openquake virtual env.
#
# Usage: python3 ../scripts/TakeSnapshot.py NAME EXPO SHAKE DMGb0 DMGr1 LOSSb0 LOSSr1
#       where NAME is the tectonic indicator and name (Ex: IDM7p1_JdF)
#       and EXPO is the exposure file type (b or s)
#       and DMG/LOSS are the run numbers for the baseline/retro damage and loss calcs

import pandas as pd
import sys
import configparser
import os
from xml.dom import minidom
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import cartopy.io.img_tiles as cimgt
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import numpy as np

if len(sys.argv) == 1:
    print(
        "No arguments passed. Run from FINISHED directory. Please include NAME exposure_string SHAKEcalc DMGcalc_b0 DMGcalc_r1 LOSScalc_b0 LOSScalc_r1."
    )
    print(
        "EX: python3 ../scripts/TakeSnapshot.py SIM9p0_CSZlockedtrans b 222 140 141 142 143"
    )
    exit()

NAME = sys.argv[1]
EXPO = sys.argv[2]
SHAKE = sys.argv[3]
DMGb0 = sys.argv[4]
DMGr1 = sys.argv[5]
LOSSb0 = sys.argv[6]
LOSSr1 = sys.argv[7]

#######################################################################################
### GRAB DATA FROM INPUTS AND OUTPUTS
#######################################################################################
# Name relevant files & folders
FINISHEDdir = '.'
RUPTUREdir = '../ruptures/'
INITdir = '../initializations/'
shakename = f'{FINISHEDdir}/s_shakemap_{NAME}_{SHAKE}.csv'
dmg_basename = f'{FINISHEDdir}/s_dmgbyasset_{NAME}_b0_{DMGb0}_{EXPO}.csv'
cons_basename = f'{FINISHEDdir}/s_consequences_{NAME}_b0_{DMGb0}_{EXPO}.csv'
loss_basename = f'{FINISHEDdir}/s_lossesbyasset_{NAME}_b0_{LOSSb0}_{EXPO}.csv'
dmg_retroname = f'{FINISHEDdir}/s_dmgbyasset_{NAME}_r1_{DMGr1}_{EXPO}.csv'
cons_retroname = f'{FINISHEDdir}/s_consequences_{NAME}_r1_{DMGr1}_{EXPO}.csv'
loss_retroname = f'{FINISHEDdir}/s_lossesbyasset_{NAME}_r1_{LOSSr1}_{EXPO}.csv'
haz_in = f'{INITdir}/s_Hazard_{NAME}.ini'
dmg_in = f'{INITdir}/s_Damage_{NAME}_b0_{EXPO}.ini'
rsk_in = f'{INITdir}/s_Risk_{NAME}_b0_{EXPO}.ini'

# Read in data
loss = pd.read_csv(loss_basename)
cons = pd.read_csv(cons_basename)
damg = pd.read_csv(dmg_basename)
shake = pd.read_csv(shakename)

# Grab input configs
args = [haz_in, dmg_in, rsk_in]
os.system('')
config = configparser.ConfigParser()
config.read(args[0])
site_model_file = config.get('site_params', 'site_model_file')
rupture_model_file = config.get('Rupture information', 'rupture_model_file')
rupture_mesh_spacing = config.get('Rupture information', 'rupture_mesh_spacing')
gsim_logic_tree_file = config.get(
    'Calculation parameters', 'gsim_logic_tree_file'
)
config.read(args[2])
truncation_level_risk = config.get('Calculation parameters', 'truncation_level')
maximum_distance = config.get('Calculation parameters', 'maximum_distance')
number_of_ground_motion_fields_risk = config.get(
    'Calculation parameters', 'number_of_ground_motion_fields'
)
exposure_file = config.get('Exposure model', 'exposure_file')
taxonomy_mapping_baseline = config.get('Vulnerability', 'taxonomy_mapping_csv')
structural_vulnerability_file = config.get(
    'Vulnerability', 'structural_vulnerability_file'
)
nonstructural_vulnerability_file = config.get(
    'Vulnerability', 'nonstructural_vulnerability_file'
)
contents_vulnerability_file = config.get(
    'Vulnerability', 'contents_vulnerability_file'
)
config.read(args[1])
structural_fragility_file = config.get('fragility', 'structural_fragility_file')
description = config.get('general', 'description')


# Merge consequences to damage and create calculated fields
data = damg.merge(cons, left_on='asset_id', right_on='asset_ref')
data['hospital'] = data['casualties_day_severity_2'] + data['casualties_day_severity_3']
data['debris'] = data['debris_brick_wood_tons'] + data['debris_concrete_steel_tons']

# Group by DAUID, ADAUID, etc. (for RDM)
# lossout = loss.groupby('csduid')['totalLoss'].sum().reset_index()
# entrapmentsout = data.groupby('dauid')['casualties_day_severity_3'].sum().reset_index()
# hospitalout = data.groupby('adauid')['hospital'].sum().reset_index()
# debrisout = data.groupby('dauid')['debris'].sum().reset_index()
# carelocalout = data.groupby('dauid')['sc_Displ90'].sum().reset_index()
# caremuniout = data.groupby('csduid')['sc_Displ90'].sum().reset_index()

# Items of Interest
mag = float(NAME[3] + '.' + NAME[5])
rup = minidom.parse(RUPTUREdir + rupture_model_file)
hypo = rup.getElementsByTagName('hypocenter')
lat = hypo[0].attributes['lat'].value
lon = hypo[0].attributes['lon'].value
cost = loss['totalLoss'].sum()
redtag = data['structural~complete'].sum()
displaced = data['sc_Displ90'].sum()
deaths = data['casualties_day_severity_4'].sum()
critical = data['casualties_day_severity_3'].sum()
hospital = data['hospital'].sum()
try:
    max_PGA = shake['gmv_PGA'].max()
except:
    max_PGA = -999999999999


#######################################################################################
### GENERATE A MAP
#######################################################################################
lon, lat = float(lon), float(lat)

extents = [lon - 2, lon + 2, lat - 1.3, lat + 1.3]  # Map extents
request = cimgt.OSM()

# Plot map
fig = plt.figure(figsize=(5, 5), frameon=True)  # figure size

ax = plt.axes(
    projection=ccrs.LambertConformal(
        central_longitude=lon, central_latitude=lat, standard_parallels=(lat, lat)
    )
)  # Proj is Lambert Conformal Conic (GSC convention)

ax.set_extent(extents)  # Set map extent using extents
ax.add_image(request, 7, interpolation='spline36')  # Add image overlay

# Add map features
gl = ax.gridlines(
    crs=ccrs.PlateCarree(),
    x_inline=False,
    y_inline=False,
    draw_labels=True,
    linewidth=1,
    color='gray',
    alpha=0.5,
    linestyle='-',
)
gl.top_labels = False
gl.left_labels = False
gl.xlocator = mticker.FixedLocator(
    np.arange(-160, -40, 2).tolist()
)  # lon gridlines every 2deg
gl.ylocator = mticker.FixedLocator(
    np.arange(44, 80, 1).tolist()
)  # lat gridlines every deg

plt.plot(lon, lat, 35, markersize=6, marker='o', color='r', zorder=5)
plt.title(NAME)
plt.savefig(str(FINISHEDdir) + '/' + str(NAME) + '.png')
# plt.show()


#######################################################################################
########### LIKELIHOOD
#######################################################################################
#### NOTE: THIS SECTION IS EXPERIMENTAL. PLEASE USE WITH EXTREME CAUTION ##############
#######################################################################################
# Python code written by THobbs on 23 Mar 2021 to add likelihood information to earthquake scenario metadata.
# Uses national seismic hazard source model to determine likelihood of an event of equal or greater magnitude occuring in the scenario source region.
# Currently in draft form, testing for western Canada non-characteristic, non-fitted events.
# In future will add likelihood of experiencing loss greater than scenario loss, based on national probabilistic seismic risk.

### Setup
from shapely.geometry import Point, Polygon, LineString
import shapely.wkt

tectregionnames = {
    "activecrust": "Active Shallow Crust",
    "stablecrust": "Stable Shallow Crust",
    "interface": "Subduction Interface",
    "intraslab55": "Subduction IntraSlab55",
    "intraslab30": "Subduction IntraSlab30",
}


### Grab Scenario Information
epi = Point(
    float(lon), float(lat)
)  # epicentre of scenario - want to check which source region this is in
tectonicRegion = tectregionnames[
    gsim_logic_tree_file.split('NGASa0p3weights_')[1].strip('.xml')
]  # get the tectonic region from gsim logic tree called
# COMMENTED OUT ABOVE (actual code) TO SEND WORKABLE MINIMUM CODE FOR REVIEW
# TEST SCENARIO 1 - Georgia Strait event
# epi = Point(-123.409919,49.27266143); mag = float(7.3)
# tectonicRegion = tectregionnames['activecrust']
# TEST SCENARIO 2 - Beaufort-Mackenzie Convergence event
# epi = Point(-139.572,70.002); mag=float(7.3)
# tectonicRegion = tectregionnames['interface']
# TEST SCENARIO 3 -
# epi = Point(-77.25, 47.42); mag=float(6)
# tectonicRegion = tectregionnames['stablecrust']
# TEST SCENARIO - TELECHICK
# NAME='M6p1_Telachick'
# epi = Point(-123.1792, 53.8633); mag=float(6.1)
# tectonicRegion = tectregionnames['activecrust']

### Find scenario source region and determine rate
if 'Cascadia' in NAME:
    wRR = [433]
elif 'LeechRiver' in NAME:
    wRR = [3500]
else:
    filepath = "../../CanadaSHM6/source_summary_csv/simplifiedModel/"
    W = pd.read_csv(filepath + "W_CANADA_UPDATED_simplified_collapsedRates.csv")
    W['regWt'] = 1
    W['regName'] = 'W'
    SE_R2 = pd.read_csv(filepath + "SE_CANADA_R2_simplified_collapsedRates.csv")
    SE_R2['regWt'] = 0.2
    SE_R2['regName'] = 'SE_R2'
    SE_H2 = pd.read_csv(filepath + "SE_CANADA_H2_simplified_collapsedRates.csv")
    SE_H2['regWt'] = 0.4
    SE_H2['regName'] = 'SE_H2'
    SE_HY = pd.read_csv(filepath + "SE_CANADA_HY_simplified_collapsedRates.csv")
    SE_HY['regWt'] = 0.4
    SE_HY['regName'] = 'SE_HY'
    EA_R = pd.read_csv(filepath + "EasternArctic_R_simplified_collapsedRates.csv")
    EA_R['regWt'] = 0.4
    EA_R['regName'] = 'EA_R'
    EA_H = pd.read_csv(filepath + "EasternArctic_H_simplified_collapsedRates.csv")
    EA_H['regWt'] = 0.6
    EA_H['regName'] = 'EA_H'
    df = pd.concat([W, SE_R2, SE_H2, SE_HY, EA_R, EA_H]).reset_index()
    df2 = df.loc[df['tectReg'] == tectonicRegion]  # only scenario tectonic region
    thresh = 0.01
    rate = pd.DataFrame(
        columns=[
            'srcWeight',
            'srcName',
            'regWeight',
            'regName',
            'maxMagCentral',
            'N0Central',
            'bCentral',
            'betaC',
            'NC',
            'RP',
        ]
    )
    # for each row
    for index, row in df2.iterrows():
        coords = row['shape']
        if 'POLYGON' in coords:
            newcoords = (
                (coords.split('))')[0])
                + ', '
                + (coords.split('((')[1].split(',')[0])
                + '))'
            )  # append first point to end
            poly = shapely.wkt.loads(newcoords)
            if epi.within(poly.buffer(thresh)):
                weightIn = row['srcWt']
                srcNameIn = row['srcName']
                regWtIn = row['regWt']
                regNameIn = row['regName']
                maxMagCentralIn = row['maxMagCentral']
                N0CentralIn = row['N0Central']
                bCentralIn = row['bCentral']
                beta_CIn = row['bCentral'] * np.log(10)
                NCIn = (
                    row['N0Central']
                    * (np.exp(-beta_CIn * mag))
                    * (1 - np.exp(-beta_CIn * (row['maxMagCentral'] - mag)))
                )
                RPIn = 1 / NCIn
                rate = rate.append(
                    {
                        'srcWeight': weightIn,
                        'srcName': srcNameIn,
                        'regWeight': regWtIn,
                        'regName': regNameIn,
                        'maxMagCentral': maxMagCentralIn,
                        'N0Central': N0CentralIn,
                        'bCentral': bCentralIn,
                        'betaC': beta_CIn,
                        'NC': NCIn,
                        'RP': RPIn,
                    },
                    ignore_index=True,
                )
        if 'LINESTRING' in coords:
            poly = shapely.wkt.loads(coords)
            if poly.distance(epi) < thresh:
                weightIn = row['srcWt']
                srcNameIn = row['srcName']
                regWtIn = row['regWt']
                regNameIn = row['regName']
                maxMagCentralIn = row['maxMagCentral']
                N0CentralIn = row['N0Central']
                bCentralIn = row['bCentral']
                beta_CIn = row['bCentral'] * np.log(10)
                NCIn = (
                    row['N0Central']
                    * (np.exp(-beta_CIn * mag))
                    * (1 - np.exp(-beta_CIn * (row['maxMagCentral'] - mag)))
                )
                RPIn = 1 / NCIn
                rate = rate.append(
                    {
                        'srcWeight': weightIn,
                        'srcName': srcNameIn,
                        'regWeight': regWtIn,
                        'regName': regNameIn,
                        'maxMagCentral': maxMagCentralIn,
                        'N0Central': N0CentralIn,
                        'bCentral': bCentralIn,
                        'betaC': beta_CIn,
                        'NC': NCIn,
                        'RP': RPIn,
                    },
                    ignore_index=True,
                )

    print(rate)

    # for each region (SE_H2, SE_HY, etc) find recurrence rate for any of the sources
    wRR = list()
    for r in rate['regName'].unique():
        dftemp = rate.loc[rate['regName'] == r]
        if any(dftemp['srcWeight'] != 1.0):
            # weight the non-1's by their source branch weighting
            dftemp['NC'] = dftemp['NC'] * dftemp['srcWeight']
        RR = 1 / (dftemp['NC'].sum())
        print(f"The recurrence rate for {r} is {RR} years")
        wRR.append(np.multiply(RR, dftemp['regWeight'].max()))

    # find weighted average between regions
    print("Weighted recurrence rate is " + str(sum(wRR)))
wRRprint = sum(wRR)

# unanswered pieces
# - is it ok that the regions overlap / choice of buffer?
# - will things on linestring also be within polygon?
# - will there be cases where something is in Arctic and East, or other overlap?
# - how to include cascadia and leech river in W_CANADA_UPDATED_simplified_collapsedRates_Fitted and W_CANADA_UPDATED_simplified_collapsedRates_Characteristic


#######################################################################################
######## SAVE MARKDOWN
#######################################################################################


# Function to generate github link and download button markdown
def link_markdown(link):
    if link.startswith('../../openquake-inputs'):
        gh_link = link.replace(
            '../../openquake-inputs',
            'https://github.com/OpenDRR/openquake-inputs/blob/main',
        )
        display_link = link.replace('../', '', 2)
    elif link.startswith('../../CanadaSHM6'):
        gh_link = link.replace(
            '../../CanadaSHM6', 'https://github.com/OpenDRR/CanadaSHM6/blob/master'
        )
        display_link = link.replace('../', '', 2)
    elif link.startswith('../'):
        gh_link = link.replace(
            '..', 'https://github.com/OpenDRR/earthquake-scenarios/blob/master', 1
        )
        display_link = link.replace('../', '', 1)
    elif link.startswith('.'):
        gh_link = link.replace(
            '.',
            'https://github.com/OpenDRR/earthquake-scenarios/blob/master/FINISHED',
            1,
        )
        display_link = link.replace('./', '', 1)
    download_link = gh_link.replace('blob', 'raw', 1)
    # Markdown for link - [link text](link url)
    md_link = f'[{display_link}]({gh_link})'
    # HTML button for download link
    button = f'[<kbd>Download</kbd>]({download_link})'
    return md_link + '<br/>' + button


# Generate markdown for all files
sh_file = link_markdown(shakename)
db_file = link_markdown(dmg_basename)
dr_file = link_markdown(dmg_retroname)
cb_file = link_markdown(cons_basename)
cr_file = link_markdown(cons_retroname)
lb_file = link_markdown(loss_basename)
lr_file = link_markdown(loss_retroname)
sm_file = link_markdown(site_model_file)
rm_file = link_markdown(rupture_model_file)
gl_tree_file = link_markdown(gsim_logic_tree_file)
ex_file = link_markdown(exposure_file)
tmb_file = link_markdown(taxonomy_mapping_baseline)
sf_file = link_markdown(structural_fragility_file)
sv_file = link_markdown(structural_vulnerability_file)
nv_file = link_markdown(nonstructural_vulnerability_file)
cv_file = link_markdown(contents_vulnerability_file)

metadata = {
    "magnitude": mag,
    "latitude": '{0:.3f} degrees'.format(float(lat)),
    "longitude": '{0:.3f} degrees'.format(float(lon)),
    "maximum_peak_ground_acceleration": '{0:.3f} g'.format(max_PGA),
    "recurrence rate": '{0:,.0f} years*'.format(wRRprint),
    "": '*For Cascadia, Leech River, and Devil\'s Mountain Faults these are characteristic earthquakes, else they are recurrence interval for an event of equal or greater magnitude in the scenario source region.',
    "cost": '${0:,.0f}'.format(cost),
    "redtag": '{0:,.0f} buildings'.format(redtag),
    "displaced": '{0:,.0f} people'.format(displaced),
    "deaths": '{0:,.0f} people'.format(deaths),
    "critical_injuries_and_entrapments": '{0:,.0f} people'.format(critical),
    "all_hospitalizations": '{0:,.0f} people'.format(hospital),
    "epicentre_map": '![Epicentre]({}.png)'.format(NAME),
    "shakemap_file": sh_file,
    "damage_baseline_file": db_file,
    "damage_retrofitted_file": dr_file,
    "consequence_baseline_file": cb_file,
    "consequence_retrofitted_file": cr_file,
    "loss_baseline_file": lb_file,
    "loss_retrofitted_file": lr_file,
    "site_model_file": sm_file,
    "rupture_model_file": rm_file,
    "rupture_mesh_spacing": rupture_mesh_spacing,
    "gsim_logic_tree_file": gl_tree_file,
    "truncation_level_risk": truncation_level_risk,
    "maximum_distance": maximum_distance,
    "number_of_ground_motion_fields_risk": number_of_ground_motion_fields_risk,
    "exposure_file": ex_file,
    "taxonomy_mapping_baseline": tmb_file,
    "structural_fragility_file": sf_file,
    "structural_vulnerability_file": sv_file,
    "nonstructural_vulnerability_file": nv_file,
    "contents_vulnerability_file": cv_file,
    "description": description,
}

# Save markdown file
md_file = f'{FINISHEDdir}/{NAME}.md'
df = pd.DataFrame(list(metadata.items()), columns=['Name', NAME])
pd.options.display.max_colwidth = 200
with open(md_file, 'w') as f:
    f.write(df.to_markdown(index=False))
    f.write('\n')


################################################## OLD SCRAPS

# Print statements
# print('Total cost: ${0:,.0f}'.format(cost))
# print('Total red tags: {0:,.0f}'.format(redtag))
# print('Total displaced: {0:,.0f}'.format(displaced))
# print('Total deaths: {0:,.0f}'.format(deaths))
# print('Total criticalinjuries/entrap: {0:,.0f}'.format(critical))
# print('Total hospital surge: {0:,.0f}'.format(hospital))

# Write out csv data (for RDM)
# lossout.to_csv('loss.csv', index=False)
# entrapmentsout.to_csv('entrapment.csv', index=False)
# hospitalout.to_csv('hospital.csv', index=False)
# debrisout.to_csv('debris.csv', index=False)
# carelocalout.to_csv('carelocal.csv', index=False)
# caremuniout.to_csv('caremuni.csv', index=False)
