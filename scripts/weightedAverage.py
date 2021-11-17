import pandas as pd
import numpy as np
import sys
import glob
import os
import subprocess
from tqdm import tqdm
import csv

print("Calculating weighted average of scenario results...")

# USAGE: python3 weightedAverage.py NAME RETRO RUNNUM ExpoSuffix RUNTYPE
#   where NAME is the run name, such as SCM7p3_Charlevoix 
#   and RETRO is b0, r1, or r2
#   and RUNNUM is the openquake run number, such as 212
#   and RUNTYPE is damage, loss, consequence or hazard
#   default OUTFILE is s_FormattedTYPE_NAME_retro.csv
#   written by TEHobbs (2020)
#   implementing wavg code from https://pbpython.com/weighted-average.html

####FIND INPUT FILES
# grab file from oq [or local version hosted in /outputs/ using localNameCheck variable]
if len(sys.argv) == 1:
    print("No arguments passed. Please include NAME RETRO RUN# expoSuffix RUNTYPE")
    exit()

inName = sys.argv[1]
retro = sys.argv[2]
runNum = sys.argv[3]
expoSuffix = sys.argv[4]
runType = sys.argv[5]
print(str(runType))
outdir = "outputs"
suffix = ".csv"
tempdir = "temp"
masterfile = "MASTER.csv"

# Check if files exist under expected names


if runType.lower() == 'damage':
    name_native = "damages"; name_native_long = "avg_damages-rlz"
    name_out = "dmgbyasset"
    skippy = 1
    lastcol = 'lat'
    groupname = 'asset_id'
elif runType.lower() == 'loss':
    name_native = "avg_losses"; name_native_long = "avg_losses-rlz"
    name_out = "lossesbyasset"
    skippy = 1
    lastcol = 'lat'
    groupname = 'asset_id'
elif runType.lower() == 'consequence':
    name_native = "consequences"; name_native_long = "consequences-rlz"
    name_out = "consequences"
    skippy = 0
    lastcol = 'occupants_transit'
    groupname = 'asset_ref'

nameCheck = str(tempdir) + "/" + str(name_native_long) + "-000_" + str(runNum) + str(suffix)
rlzCheck = str(tempdir) + "/realizations_" + str(runNum) + str(suffix)
print(nameCheck)
if os.path.exists(nameCheck):
    print("Collecting locally stored " + str(runType) + " outputs")
else:
    print("Fetching loss outputs from OQ")
    subprocess.call(["oq", "export", str(name_native)+"-rlzs", str(runNum), "-d", str(tempdir)])

if os.path.exists(rlzCheck):
    print("Collecting locally stored realization file")
else:
    print("Fetching realization outputs from OQ")
    subprocess.call(["oq", "export", "realizations", str(runNum), "-d", str(tempdir)])

# LOAD WEIGHTS FROM REALIZATIONS
rlz = pd.read_csv(rlzCheck)

####LOAD DATA
nameCheck = str.replace(nameCheck, "-000_", "-???_")
nameName = glob.glob(nameCheck)
df = pd.DataFrame()
k = 0; data = 0
for f in nameName:
    del k
    del data
    i = int(f.split('-')[2][0:3])
    # split localname to get the rlz# out, use that to query rlz dictionary
    k = rlz.iloc[i].weight
    data = pd.read_csv(f, skiprows=skippy, thousands=',')
    if runType.lower() == 'loss':
        data['totalLoss'] = data['structural'] + data['nonstructural'] + data['contents']
    data['weight'] = k
    df = df.append(data)

print("Header of dataframe:")
print(df.head())

####CALCULATE WEIGHTED MEAN
#   Define weighted mean function
def wavg(group, avg_name, weight_name):
    d = group[avg_name]
    w = group[weight_name]
    try:
        return (d * w).sum() / w.sum()
    except ZeroDivisionError:
        return "NaN"


####FIND WEIGHTED AVERAGES
breakpt = (data.columns.get_loc(lastcol))
new = data[data.columns[0:(breakpt+1)]]  # load in context info #18 for CoV
out = 0;
for indicator in tqdm(data.columns[(breakpt+1):(len(data.columns))-1]): #25 for CoV
    del out
    out = df.groupby([groupname]).apply(wavg, indicator, 'weight').reset_index(name=indicator)
    new = pd.merge(new, out, on=groupname, how='outer')

#### EXPORT!
#   Remove outfile if it already exists
outName = "s_" + str(name_out) + "_" + str(inName) + "_" + str(retro) + "_" + str(runNum) + "_" + str(expoSuffix) + ".csv"
try:
    os.remove(outName)
except:
    print()

new.to_csv(outName, float_format='%f', index=False)
os.rename(str(outName), str(outdir) + "/" + str(outName))
print("Weighted average stored in " + str(outName))

#### REPORT OUTPUT
master = [inName, name_out, retro, runNum]
if runType.lower() == 'damage':
    RedTag = new['structural~complete'].sum()
    print("TOTAL RED TAGGED BUILDINGS: " + f'{RedTag:,.0f}')
    Ds = ['RedTag',RedTag]
elif runType.lower() == 'loss':
    EventLoss = new['totalLoss'].sum()
    print("TOTAL EVENT LOSS: $" + f'{EventLoss:,.0f}')
    Ds = ['EventLoss', EventLoss]
elif runType.lower() == 'consequence':
    Displacement = new['sc_Displ30'].sum()
    print("TOTAL PEOPLE DISPLACED AFTER 30 DAYS: " + f'{Displacement:,.0f}')
    Deaths = new['casualties_night_severity_4'].sum()
    print("TOTAL NIGHT FATALITIES: " + f'{Deaths:,.0f}')
    Ds = ['Displacement', Displacement, 'Deaths', Deaths]

### Send reports to a masterfile
#master.append(Ds)
#with open(masterfile, 'a', newline='') as myfile:
#    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
#    wr.writerow(master)



