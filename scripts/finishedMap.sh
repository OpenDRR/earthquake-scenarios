#!bash
# Script to make a map and list of all the finished scenarios in this folder.
# Uses python scripts to make the map geojson and yaml for github pages.

lat=`grep latitude *_*.md | awk -F'|' '{print $3}' | awk '{print $1}'`
lon=`grep longitude *_*.md | awk -F'|' '{print $3}' | awk '{print $1}'`
cost=`grep cost *_*.md | awk -F'|' '{print $3}' | awk '{print $1}'`
cost=${cost//$/}
cost=${cost//,/}
redtag=`grep redtag *_*.md | awk -F'|' '{print $3}' | awk '{print $1}'`
redtag=${redtag//,/}
mag=`ls *_*.md | awk -F'(_|M)' '{print $2}'`
name=`ls *_*.md | awk -F'.' '{print $1}'`
description=`grep description *_*.md | awk -F'|' '{print $3}' | sed -e 's/^[[:space:]]*/"/' -e 's/[[:space:]]*$/"/'`
displaced=`grep displaced *_*.md | awk -F'|' '{print $3}' | awk '{print $1}'`
deaths=`grep deaths *_*.md | awk -F'|' '{print $3}' | awk '{print $1}'`
critical_injuries_and_entrapments=`grep critical_injuries_and_entrapments *_*.md | awk -F'|' '{print $3}' | awk '{print $1}'`
all_hospitalizations=`grep all_hospitalizations *_*.md | awk -F'|' '{print $3}' | awk '{print $1}'`
max_pga=`grep maximum_peak_ground_acceleration *_*.md | awk -F'|' '{print $3}' | awk '{print $1}'`

# Create temporary file for finishedMap.py
paste -d"," <(echo "$mag") <(echo "$lat") <(echo "$lon") <(echo "$cost") <(echo "$redtag") <(echo "$name") > tempmap.txt

# Create .csv of scenarios and base properties
echo "name,description,mag,lat,lon,max_pga,cost,redtag,displaced,deaths,critical_injuries_and_entrapments,all_hospitalizations" > scenarios.csv
paste -d"," <(echo "$name" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//') <(echo "$description") <(echo "$mag" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//') <(echo "$lat" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//') <(echo "$lon" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//') <(echo "$max_pga" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//') <(echo "$cost" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//') <(echo "$redtag" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//') <(echo "$displaced" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//') <(echo "$deaths" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//') <(echo "$critical_injuries_and_entrapments" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//') <(echo "$all_hospitalizations" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//') >> scenarios.csv

echo "[All Scenarios To Date](FinishedScenarios.geojson)" > FinishedScenarios.md

python3 ../scripts/finishedMap.py
python3 ../scripts/generate_yml.py

rm -f tempmap.txt
