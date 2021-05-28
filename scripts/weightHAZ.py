#Python script to generate weighted average of hazard files
import os
import glob
import pandas as pd
import numpy as np
import sys
import subprocess
from tqdm import tqdm
import math

print("Calculating weighted average of scenario hazard...")

# USAGE: python3 weightHAZ.py NAME RUNNUM
#   where NAME is the run name, such as SCM7p3_Charlevoix
#   and RUNNUM is the openquake run number, such as 212
#   written by TEHobbs (2020)
#   implementing wavg code from https://pbpython.com/weighted-average.html

####FIND INPUT FILES
# grab file from oq [or local version hosted in /outputs/ using localNameCheck variable]
if len(sys.argv) == 1:
    print("No arguments passed. Please include NAME RUN#")
    exit()

inName = sys.argv[1]
runNum = sys.argv[2]

outdir = "outputs"
suffix = ".csv"
tempdir = "temp"
masterfile = "MASTER.csv"

name_native = "gmf_data"
name_out = "gmfdata"

nameCheck = str(tempdir) + "/gmf-data_" + str(runNum) + str(suffix)
rlzCheck = str(tempdir) + "/" + "realizations_" + str(runNum) + str(suffix)

try:
    if os.path.exists(glob.glob(nameCheck)[0]):
        print("Collecting locally stored hazard outputs")
except:
    print("Fetching hazard outputs from OQ")
    subprocess.call(["oq", "export", str(name_native), str(runNum), "-d", str(tempdir)])
    nameCheck = str(tempdir) + "/gmf-data_" + str(runNum) + str(suffix)

if os.path.exists(rlzCheck):
    print("Collecting locally stored realization file")
else:
    print("Fetching realization outputs from OQ")
    subprocess.call(["oq", "export", "realizations", str(runNum), "-d", str(tempdir)])

# LOAD DATA
rlz = pd.read_csv(rlzCheck)
numRlz = rlz['rlz_id'].count()
data = pd.read_csv(nameCheck, skiprows=1, thousands=',')
numEvents = (data['event_id'].unique().max())+1
data['rlz'] = numRlz*np.divide(data['event_id'],numEvents)
data['rlz'] = data['rlz'].apply(np.floor)
data['rlz'] = data['rlz'].astype(int)
#data.loc[data['site_id']==0]
datanew = data.merge(rlz[['weight','rlz_id']], left_on='rlz', right_on='rlz_id').drop('rlz_id', axis=1)
print("Data Loaded")

####CALCULATE WEIGHTED MEAN
#   Define weighted mean function
def wavg(group, avg_name, weight_name):
    d = group[avg_name]
    w = group[weight_name]
    try:
        return (d * w).sum() / w.sum()
    except ZeroDivisionError:
        return "NaN"

out = 0
new = pd.DataFrame(data.site_id.unique()).rename(columns={0:'site_id'})
print("Creating weighted average result")
for col in tqdm(data.columns[2:-1]):
    del out
    out = datanew.groupby('site_id').apply(wavg, col, 'weight')
    out.name = col
    outtest = pd.DataFrame(out)
    new = new.merge(outtest, on='site_id')    

####SAVE
print("Saving!")
outName = str(outdir) + "/s_" + str(name_out) + "_" + str(inName) + "_" + str(runNum) + str(suffix)
new.to_csv(outName, float_format='%f', index=False)

####MAKE SHAKEMAP
site = pd.read_csv(str(tempdir) + "/sitemesh_" + str(runNum) + str(suffix))
gmf = pd.read_csv(outName)
shake = gmf.merge(site,on='site_id')
shake.to_csv(str(outdir) + "/s_shakemap_" + str(inName) + "_" + str(runNum) + str(suffix),index=False)

# outnew = data.groupby('site_id')['gmv_PGA','gmv_SA(0.3)','gmv_SA(1.0)'].mean()
# outnew.to_csv('JdF6p8_updateGMPE.csv',float_format='%f', index=False)

# data2 is the output with PGV
# pgv['site_id'] = data2['site_id']
# pgv['gmv_PGV'] = data2['gmv_PGV']
# outnew2 = outnew.merge(pgv, on = 'site_id')
# outnew2.to_csv('JdF6p8_updateGMPE.csv',float_format='%f', index=False)





