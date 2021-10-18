# script to plot ruptures and hypocentres, written by TEH on 13 Oct 2021

#usage: python plotRupture.py NAME

####### EDIT THESE IF USING ON ANOTHER MACHINE
fileloc = "/Users/thobbs/Documents/GitHub/deterministic-projects/CoV/ruptures/"
####################################################

### Import
import pandas as pd
import sys
import configparser
import argparse
import os
from xml.dom import minidom
import cartopy.crs as ccrs
import cartopy
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import numpy as np

### Load file
NAME = sys.argv[1]
rup = minidom.parse(fileloc+NAME)
hypo = rup.getElementsByTagName('hypocenter')
lat = hypo[0].attributes['lat'].value
lon = hypo[0].attributes['lon'].value;

surf = rup.getElementsByTagName('simpleFaultGeometry')


