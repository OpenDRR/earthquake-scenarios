#!python3

import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np


# Load and reformat data
data = pd.read_csv('tempmap.txt', header=None)
data.columns = ['mag','lat','lon','name']
data['mag'] = data['mag'].str.replace('p','.')
data = data.sort_values('mag', ascending=False).drop_duplicates()

# Load data for testing
'''data = pd.read_table("../finished/finishedscenarios.md",
                        skiprows=[0,2], sep='|',
                        skipinitialspace=True,
                        usecols=[1,2,3,4])
data.columns = data.columns.str.strip()'''

# Generate a map
extent = [-130, -55, 36.5, 75] # Map bounds
central_lon = np.mean(extent[:2]) # Longitude midpoint
central_lat = np.mean(extent[2:]) # Latitude midpoint

fig = plt.figure(figsize=(9, 6))

# Create map and set bounds
ax = plt.axes(projection=ccrs.AlbersEqualArea(central_lon, central_lat))
ax.set_extent(extent)

# Add map features
resol = '50m'
states_provinces = cfeature.NaturalEarthFeature(
    category='cultural',
    name='admin_1_states_provinces_lines',
    scale=resol,
    facecolor='none')

ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.LAKES)
ax.add_feature(cfeature.RIVERS)
ax.add_feature(cfeature.BORDERS)
ax.add_feature(states_provinces, edgecolor='gray')

# Colourmap for magnitude representation
cmap = LinearSegmentedColormap.from_list('name', ['yellow', 'red'])

# Add quake locations
mags =np.array([float(x) for x in data['mag']])
plt.scatter(x=data['lon'], y=data['lat'],
            transform=ccrs.PlateCarree(), # Plots points to Plate Carree and projects to Albers
            marker = '*',
            c=mags, # Value for colour on colourmap
            edgecolors='k',
            alpha=0.7, # Transparency
            cmap=cmap, # Maps colours to colourmap
            s=mags*18)

# Add a legend
plt.colorbar(label='magnitude', shrink=0.5, pad=0.01)
plt.clim(6, 9)
for a in [6.0, 7.0, 8.0, 9.0]:
    plt.scatter([], [], marker='*', c='k', alpha=0.7,
                s=np.dot(18,a), label='M '+str(a))
plt.legend(scatterpoints=1, frameon=False,
           labelspacing=1, loc='upper right')

# Save map
plt.savefig('FinishedScenarios.png')

# Save markdown file
md_file = 'FinishedScenarios.md'
pd.options.display.max_colwidth = 200
with open(md_file, 'a') as f:
    f.write(
        data.to_markdown(index=False)
    )

# Make it interactive?
# Add labels?
# Add legend
