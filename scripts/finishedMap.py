#!python3

import pandas as pd
from geojson import Feature, Point, FeatureCollection
import geojson
import numpy as np


# Load and reformat data
data = pd.read_csv('tempmap.txt', header=None)
data.columns = ['mag','lat','lon', 'cost', 'redtag', 'title']
data['mag'] = data['mag'].str.replace('p','.')
data = data.sort_values('mag', ascending=False).drop_duplicates()

# Offset
sigma = 0.0015

features = []
# Generate points for scenarios
for i in range(len(data)):
    point = data.iloc[i]
    # Set marker size and colour according to magnitude
    size = 'medium'
    color = '#ff7b00'
    link = 'https://github.com/OpenDRR/earthquake-scenarios/blob/master/FINISHED/' + point.title.strip() + '.md'
    if float(point.mag) < 6:
        size = 'small'
        color = '#ffea00'
    elif float(point.mag) >= 8:
        size = 'large'
        color = '#ff4000'
    # Offset coordinates randomly to prevent overlap
    lon = np.random.normal(point.lon, sigma)
    lat = np.random.normal(point.lat, sigma)
    # Set data for point features
    feature = Feature(geometry=Point((lon, lat)),
                    properties={"magnitude": str(point.mag),
                                "cost": '$' + str("{:,}".format(point.cost)),
                                "redtag buildings": "{:,}".format(point.redtag),
                                "URL": f'<a href="#{point.title.strip()}">Additional info and resources</a>',
                                "marker-color": color,
                                "marker-size": size})
    features.append(feature)
collection = FeatureCollection(features)
dump = geojson.dumps(collection, sort_keys=False)


# Save geoJSON file
geo_file = 'FinishedScenarios.geojson'
with open(geo_file, 'w') as f:
    f.write(dump)


# Save markdown file
del data['cost']
del data['redtag']
data.rename(columns={'title': 'name'}, inplace=True)
md_file = 'FinishedScenarios.md'
pd.options.display.max_colwidth = 200
with open(md_file, 'a') as f:
    f.write(
        data.to_markdown(index=False)
    )

# Add legend
