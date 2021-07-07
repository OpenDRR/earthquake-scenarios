#!python3

import pandas as pd
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from itertools import chain
from matplotlib.colors import LinearSegmentedColormap
import numpy as np


# Load and reformat data
data = pd.read_csv('tempmap.txt', header=None)
data.columns = ['mag','lat','lon','name']
data['mag'] = data['mag'].str.replace('p','.')
data = data.sort_values('mag', ascending=False).drop_duplicates()
   
# Generate a map
fig = plt.figure()
cmap = LinearSegmentedColormap.from_list('name', ['yellow', 'red'])
m = Basemap(projection='lcc', resolution='l',
            width=6E6, height=4E6,
            lat_0=60, lon_0=-95)
m.shadedrelief(scale=0.2)
m.drawcountries()
m.drawstates()
x,y=m(data['lon'].values,data['lat'].values) 
plt.scatter(x, y, marker = '*', edgecolors='k',
          c=data['mag'].astype(float).values, 
          s=np.dot(18,data['mag'].astype(float).values),
          cmap=cmap, alpha=0.7)

# Add a legend
plt.colorbar(label='magnitude')
plt.clim(6, 9)
for a in [6.0, 7.0, 8.0, 9.0]:
    plt.scatter([], [], marker='*', c='k', alpha=0.7, s=np.dot(18,a),
                label='M '+str(a))
#plt.scatter(xa, ya, marker = '*', edgecolors='k', c=a, cmap=cmap, alpha=0.7, s=a, label=str(a))
plt.legend(scatterpoints=1, frameon=False,
           labelspacing=1, loc='upper right');

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
