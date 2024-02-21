#! python3
# Script to produce a pager-style output for scenario earthquakes. 
# You need to have created the rupture, damage, consequence, and loss files 
# already. Run from in FINISHED dir. Written by Tiegan E. Hobbs on 3 November 2020.
# Seems you need to be out of openquake virtual env. 
# Usage: python3 ../scripts/TakeSnapshot.py NAME EXPO HAZ DMGb0 DMGr1 LOSSb0 LOSSr1
#       where NAME is the tectonic indicator and name (Ex: IDM7p1_JdF)
#       and EXPO is the exposure file type (b or s)
#       and DMG/LOSS are the run numbers for the baseline/retro damage and loss calcs

import pandas as pd
import sys
import os
from xml.dom import minidom
import numpy as np
import glob
from shapely.geometry import Point, Polygon, LineString
import shapely.wkt

#if len(sys.argv) == 1:
#    print("No arguments passed. Run from FINISHED directory. Please include NAME exposure_string SHAKEcalc DMGcalc_b0 DMGcalc_r1 LOSScalc_b0 LOSScalc_r1.")
#    print("EX: python3 ../scripts/TakeSnapshot.py SIM9p0_CSZlockedtrans b 222 140 141 142 143")
#    exit()

#NAME = sys.argv[1]
#EXPO = sys.argv[2]
#SHAKE = sys.argv[3]
#DMGb0 = sys.argv[4]
#DMGr1 = sys.argv[5]
#LOSSb0 = sys.argv[6]
#LOSSr1 = sys.argv[7]



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
tectregionnames = {
    "activecrust": "Active Shallow Crust",
    "stablecrust": "Stable Shallow Crust",
    "interface": "Subduction Interface",
    "intraslab55": "Subduction IntraSlab55",
    "intraslab30": "Subduction IntraSlab30"
}

logicweights = {
    "WCan_H2east_Harctic_simplified_collapsedRates.xml": 0.24,
    "WCan_H2east_Rarctic_simplified_collapsedRates.xml": 0.16,
    "WCan_HYeast_Harctic_simplified_collapsedRates.xml": 0.24,
    "WCan_HYeast_Rarctic_simplified_collapsedRates.xml": 0.16,
    "WCan_R2east_Harctic_simplified_collapsedRates.xml": 0.12,
    "WCan_R2east_Rarctic_simplified_collapsedRates.xml": 0.08
}


### Grab Scenario Information
#epi = Point(float(lon), float(lat))  # epicentre of scenario - want to check which source region this is in
#tectonicRegion = tectregionnames[gsim_logic_tree_file.split('NGASa0p3weights_')[1].strip('.xml')]  # get the tectonic region from gsim logic tree called

# COMMENTED OUT ABOVE (actual code) TO SEND WORKABLE MINIMUM CODE FOR REVIEW
# TEST SCENARIO 1 - Georgia Strait event
#epi = Point(-123.409919,49.27266143); mag = float(7.3)
#tectonicRegion = tectregionnames['activecrust']
# TEST SCENARIO 2 - Beaufort-Mackenzie Convergence event
#epi = Point(-139.572,70.002); mag=float(7.3)  
#tectonicRegion = tectregionnames['interface']
# TEST SCENARIO 3 - 
#epi = Point(-77.25, 47.42); mag=float(6)
#tectonicRegion = tectregionnames['stablecrust']
# TEST SCENARIO - TELECHICK
NAME='M6p1_Telachick'
epi = Point(-123.1792, 53.8633); mag=float(6.1)
tectonicRegion = tectregionnames['activecrust']

df2 = pd.DataFrame(columns=['code', 'name', 'tectonicRegion', 'weight', 'posList', 'rates', 'minMag', 'binWidth', 'maxMag'])

### Find scenario source region and determine rate
#if 'Cascadia' in NAME:
#    wRR = 433
#elif 'LeechRiver' in NAME:
#    wRR = 3500
#else:

filepath = "../CanadaSHM6/OpenQuake_model_files/sources/nationalModel/xml/simplifiedModel/"
all_files = glob.glob(filepath + "WCan_*.xml")
for fname in all_files:
    ### Read in source xml file
    file = minidom.parse(fname)
    ### Grab weight
    wt = logicweights[fname.split('/')[-1]]
    
    ### Extract sources
    source = file.getElementsByTagName('areaSource')
    for el in source:
        code = el.attributes['id'].value
        name = el.attributes['name'].value
        regi = el.attributes['tectonicRegion'].value
        coords = el.getElementsByTagName('gml:posList').item(0).toprettyxml().split('                                    ')[1].split('\n')[0]
        binw = float(el.getElementsByTagName('incrementalMFD').item(0).attributes['binWidth'].value)
        minm = float(el.getElementsByTagName('incrementalMFD').item(0).attributes['minMag'].value)
        rates = el.getElementsByTagName('occurRates').item(0).firstChild.nodeValue.split('                        ')[1].split('\n')[0].split(' ')
        numr = len(rates)
        maxm = minm+((numr-1)*binw)
        df2 = df2.append({'code': code, 'name': name, 'tectonicRegion': regi, 'weight': wt, 'posList': coords, 'rates': rates, 'minMag': minm, 'binWidth': binw, 'maxMag': maxm}, ignore_index=True)

df2 = df2.drop_duplicates(subset='name')
df = df2.loc[df2['tectonicRegion'] == tectonicRegion] #only scenario tectonic region
thresh = 0.01 #set threshold for point being 'in' a polygon
df3 = pd.DataFrame(columns=['code', 'name', 'tectonicRegion', 'weight', 'posList', 'rates', 'minMag', 'binWidth', 'maxMag', 'rate'])

#for each row 
for index, row in df.iterrows():
    coords = row['posList']
    coords2 = [float(i) for i in coords.split()]
    newcoords = [coords2[n:n+2] for n in range(0, len(coords2), 2)]
    poly = Polygon(newcoords)
    if epi.within(poly.buffer(thresh)):
        mags = np.arange(row['minMag'], row['maxMag']+row['binWidth'], row['binWidth'])
        RATES = [float(i) for i in row['rates']]
        row['rate'] = np.interp(mag,mags,RATES) # Find the rate based on specified magnitude
        df3 = df3.append(row)
        
#### Find total weighted rate
df3['normrate'] = df3['rate']*df3['weight']
totRate = 1/(df3['normrate'].sum()/df3['weight'].sum())


