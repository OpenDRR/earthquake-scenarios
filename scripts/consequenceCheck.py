# python script to error check consequence scripts. Testing if any individual assets have disrupted people that decrease with time. run from FINISHED. Written by TH on 29 Oct 2021.

import glob 
import pandas as pd
import numpy as np

files = glob.glob('s_consequences_*.csv')
for f in files:

f = 's_consequences_IDM7p1_Sidney_r1_119_b.csv'
df = pd.read_csv(f)
if any((df['sc_Displ30'] < df['sc_Displ3']) & (df['sc_Displ30'] > 0.0)):
#    print(f)
    print(df[['asset_ref','sc_Displ3','sc_Displ30']][((df['sc_Displ30'] < df['sc_Displ3']) & (df['sc_Displ30'] > 0.0))])
#if any((df['sc_Displ90'] < df['sc_Displ30']) & (df['sc_Displ90'] > 0.0)):
#    print(f)
#if any((df['sc_Displ180'] < df['sc_Displ90']) & (df['sc_Displ180'] > 0.0)):
#    print(f)
#if any((df['sc_Displ360'] < df['sc_Displ180']) & (df['sc_Displ360'] > 0.0)):
#    print(f)


dam = pd.read_csv('/Users/thobbs/Documents/GitHub/earthquake-scenarios/FINISHED/s_dmgbyasset_IDM7p1_Sidney_r1_119_b.csv')
expo = pd.read_csv('../../openquake-inputs/exposure/general-building-stock/oqBldgExp_BC.csv')


#### testing asset '52067-RES2-MH-PC' (index 5497) of Sidney M7.1 r1:
#                  asset_ref  sc_Displ3  sc_Displ30
#5497       52067-RES2-MH-PC        8.3       6.225


num = expo['number'][expo['id'] == '52067-RES2-MH-PC']
damg = [(dam['structural~no_damage'][dam.index == 5497]).values[0], (dam['structural~slight'][dam.index == 5497]).values[0], (dam['structural~moderate'][dam.index == 5497]).values[0], (dam['structural~extensive'][dam.index == 5497]).values[0], (dam['structural~complete'][dam.index == 5497]).values[0]]
damr = np.array(damg)/2
rec = np.array([0, 5, 20, 120, 240])

recovery_time = np.dot(damr, rec) #29.1125 days

occs = expo['night'][expo['id'] == '52067-RES2-MH-PC']
sc_Displ3 = occs if recovery_time > 3 else 0


###### checking HAZUS params
recovery_time_df = read_params["Building Recovery Time"](xlsx)
recovery = pd.read_csv('scripts/recoverytimes.csv')
recovery.index = recovery['label']
recovery = recovery.drop('label', axis=1)
recovery = recovery.drop('occupancy', axis=1)
recovery.columns = recovery_time_df.columns
all(recovery.eq(recovery_time_df))

repair_time_df = read_params["Building Repair Time"](xlsx)
repair = pd.read_csv('scripts/repairtime.csv')
repair.index = repair['label']
repair = repair.drop('label', axis=1)
repair = repair.drop('occupancy', axis=1)
repair.columns = repair_time_df.columns
all(repair.eq(repair_time_df))

interruption_df = read_params["Interruption Time Multipliers"](xlsx)
inter = pd.read_csv('scripts/interruptionmodifiers.csv')
inter.index = inter['label']
inter = inter.drop('label', axis=1)
inter = inter.drop('occupancy', axis=1)
inter.columns = interruption_df.columns
all(inter.eq(interruption_df))