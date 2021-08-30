#!bash
# Script to make a map and list of all the finished scenarios in this folder.
# Uses a python script to make the map image.

lat=`grep latitude *_*.md | awk -F'|' '{print $3}' | awk '{print $1}'`
lon=`grep longitude *_*.md | awk -F'|' '{print $3}' | awk '{print $1}'`
cost=`grep cost *_*.md | awk -F'|' '{print $3}' | awk '{print $1}'`
cost=${cost//$/}
cost=${cost//,/}
redtag=`grep redtag *_*.md | awk -F'|' '{print $3}' | awk '{print $1}'`
redtag=${redtag//,/}
mag=`ls *_*.md | awk -F'(_|M)' '{print $2}'`
name=`ls *_*.md | awk -F'.' '{print $1}'`

paste -d"," <(echo "$mag") <(echo "$lat") <(echo "$lon") <(echo "$cost") <(echo "$redtag") <(echo "$name") > tempmap.txt
echo "[All Scenarios To Date](FinishedScenarios.geojson)" > FinishedScenarios.md
python3 ../scripts/finishedMap.py
python3 ../scripts/generate_yml.py

rm -f tempmap.txt