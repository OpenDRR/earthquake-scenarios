#!/bin/python

#### Python script to check DSRA calculations

import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np

##############################################################################
### Load files and select SAUID of interest
SAUID = 59007373
num = 40 #index of the single building (asset) to display for bldg level calcs
dam = pd.read_csv('s_dmgbyasset_SIM9p0_CascadiaInterfaceBestFault_b0_317_b.csv')
damr = pd.read_csv('s_dmgbyasset_SIM9p0_CascadiaInterfaceBestFault_r1_318_b.csv')
cons = pd.read_csv('s_consequences_SIM9p0_CascadiaInterfaceBestFault_b0_317_b.csv')
consr = pd.read_csv('s_consequences_SIM9p0_CascadiaInterfaceBestFault_r1_318_b.csv')
loss = pd.read_csv('s_lossesbyasset_SIM9p0_CascadiaInterfaceBestFault_b0_319_b.csv')
lossr = pd.read_csv('s_lossesbyasset_SIM9p0_CascadiaInterfaceBestFault_r1_320_b.csv')
expo = pd.read_csv('../../openquake-inputs/exposure/general-building-stock/oqBldgExp_BC.csv') #from FINISHED
census = pd.read_csv('../../openquake-inputs/exposure/census-ref-sauid/census-attributes-2016.csv')
##############################################################################

### Merge dataframes and isolate SAUID of interest
# Loss
loss = loss[loss['sauid'] == SAUID]
lossr = lossr[lossr['sauid'] == SAUID]
lossn = pd.merge(loss, lossr, on='asset_id', suffixes=('_b0', '_r1'))
losse = pd.merge(lossn, expo, how='left', left_on='asset_id', right_on='id')

# Damage
dam = dam[dam['sauid'] == SAUID]
damr = damr[damr['sauid'] == SAUID]
damn = pd.merge(dam, damr, on='asset_id', suffixes=('_b0', '_r1'))
dame = pd.merge(damn, expo, how='left', left_on='asset_id', right_on='id')

# Consequence 
consn = pd.merge(cons, consr, on='asset_ref', suffixes=('_b0', '_r1'))
conse = pd.merge(consn, dame, how='right', left_on='asset_ref', right_on='id')


##############################################################################
### CALCULATE DSRA INDICATORS
SF = ['RES1', 'RES2']; MF = ['RES3A', 'RES3B', 'RES3C', 'RES3D', 'RES3E', 'RES3F', 'RES4', 'RES5', 'RES6'] 
hazweights = [('wM', 0.0, 0.0), ('wE', 0.0, 0.9), ('wC', 1.0, 1.0)] 
DSPLCHSW = pd.DataFrame(hazweights, columns = ['weight_factor', 'SF', 'MF']); DSPLCHSW.index = DSPLCHSW['weight_factor']
#above are for household displacements
IW = 0.73
EW = 0.27
OW = 0.0
AW = 0.0
IM = [0.62, 0.42, 0.29, 0.22, 0.13]
EM = [0.40, 0.26, 0.24]
OM = [0.4, 0.4]
AM = [0.4, 0.4, 0.4]
#above are for shelter


###################################################################################################
print("")
print("Damage State - baseline [bldg results for "+str(dame['asset_id'][num])+"]")
sDt_None_b0 = dame['structural~no_damage_b0'].sum(); print("sDt_None_b0 = "+str(round(sDt_None_b0,0))+" ["+str(round(dame['structural~no_damage_b0'][40],0))+"]")
sDtr_None_b0 = np.divide(dame['structural~no_damage_b0'], dame['number']).mean(); print("sDtr_None_b0 = "+str(round(sDtr_None_b0,2))+" ["+str(round(np.divide(dame['structural~no_damage_b0'], dame['number'])[40],2))+"]") #average, over all assets, of number of bldgs in that state divided by number of buildings in asset
sDt_Slight_b0 = dame['structural~slight_b0'].sum(); print("sDt_Slight_b0 = "+str(round(sDt_Slight_b0,0))+" ["+str(round(dame['structural~slight_b0'][40],0))+"]")
sDtr_Slight_b0 = np.divide(dame['structural~slight_b0'], dame['number']).mean(); print("sDtr_Slight_b0 = "+str(round(sDtr_Slight_b0,2))+" ["+str(round(np.divide(dame['structural~slight_b0'], dame['number'])[40],2))+"]")
sDt_Moderate_b0 = dame['structural~moderate_b0'].sum(); print("sDt_Moderate_b0 = "+str(round(sDt_Moderate_b0,0))+" ["+str(round(dame['structural~moderate_b0'][40],0))+"]")
sDtr_Moderate_b0 = np.divide(dame['structural~moderate_b0'], dame['number']).mean(); print("sDtr_Moderate_b0 = "+str(round(sDtr_Moderate_b0,2))+" ["+str(round(np.divide(dame['structural~moderate_b0'], dame['number'])[40],2))+"]")
sDt_Extensive_b0 = dame['structural~extensive_b0'].sum(); print("sDt_Extensive_b0 = "+str(round(sDt_Extensive_b0,0))+" ["+str(round(dame['structural~extensive_b0'][40],0))+"]")
sDtr_Extensive_b0 = np.divide(dame['structural~extensive_b0'], dame['number']).mean(); print("sDtr_Extensive_b0 = "+str(round(sDtr_Extensive_b0,2))+" ["+str(round(np.divide(dame['structural~extensive_b0'], dame['number'])[40],2))+"]")
sDt_Complete_b0 = dame['structural~complete_b0'].sum(); print("sDt_Complete_b0 = "+str(round(sDt_Complete_b0,0))+" ["+str(round(dame['structural~complete_b0'][40],0))+"]")
sDtr_Complete_b0 = np.divide(dame['structural~complete_b0'], dame['number']).mean(); print("sDtr_Complete_b0 = "+str(round(sDtr_Complete_b0,2))+" ["+str(round(np.divide(dame['structural~complete_b0'], dame['number'])[40],2))+"]")
sDt_Collapse_b0 = np.multiply(conse['collapse_ratio_b0'],conse['number']).sum(); print("sDt_Collapse_b0 = "+str(round(sDt_Collapse_b0,0))+" ["+str(round(np.multiply(conse['collapse_ratio_b0'],conse['number'])[40],0))+"]") #collapse_ratio is per building, so multiply by building before summing
sDtr_Collapse_b0 = conse['collapse_ratio_b0'].mean(); print("sDtr_Collapse_b0 = "+str(round(sDtr_Collapse_b0,2))+" ["+str(round(conse['collapse_ratio_b0'][40],2))+"]")

###################################################################################################
print("")
print("Damage State - retrofit")
sDt_None_r1 = dame['structural~no_damage_r1'].sum(); print("sDt_None_r1 = "+str(round(sDt_None_r1,0))+" ["+str(round(dame['structural~no_damage_r1'][40],0))+"]")
sDtr_None_r1 = np.divide(dame['structural~no_damage_r1'], dame['number']).mean(); print("sDtr_None_r1 = "+str(round(sDtr_None_r1,2))+" ["+str(round(np.divide(dame['structural~no_damage_r1'], dame['number'])[40],2))+"]") #average, over all assets, of number of bldgs in that state divided by number of buildings in asset
sDt_Slight_r1 = dame['structural~slight_r1'].sum(); print("sDt_Slight_r1 = "+str(round(sDt_Slight_r1,0))+" ["+str(round(dame['structural~slight_r1'][40],0))+"]")
sDtr_Slight_r1 = np.divide(dame['structural~slight_r1'], dame['number']).mean(); print("sDtr_Slight_r1 = "+str(round(sDtr_Slight_r1,2))+" ["+str(round(np.divide(dame['structural~slight_r1'], dame['number'])[40],2))+"]")
sDt_Moderate_r1 = dame['structural~moderate_r1'].sum(); print("sDt_Moderate_r1 = "+str(round(sDt_Moderate_r1,0))+" ["+str(round(dame['structural~moderate_r1'][40],0))+"]")
sDtr_Moderate_r1 = np.divide(dame['structural~moderate_r1'], dame['number']).mean(); print("sDtr_Moderate_r1 = "+str(round(sDtr_Moderate_r1,2))+" ["+str(round(np.divide(dame['structural~moderate_r1'], dame['number'])[40],2))+"]")
sDt_Extensive_r1 = dame['structural~extensive_r1'].sum(); print("sDt_Extensive_r1 = "+str(round(sDt_Extensive_r1,0))+" ["+str(round(dame['structural~extensive_r1'][40],0))+"]")
sDtr_Extensive_r1 = np.divide(dame['structural~extensive_r1'], dame['number']).mean(); print("sDtr_Extensive_r1 = "+str(round(sDtr_Extensive_r1,2))+" ["+str(round(np.divide(dame['structural~extensive_r1'], dame['number'])[40],2))+"]")
sDt_Complete_r1 = dame['structural~complete_r1'].sum(); print("sDt_Complete_r1 = "+str(round(sDt_Complete_r1,0))+" ["+str(round(dame['structural~complete_r1'][40],0))+"]")
sDtr_Complete_r1 = np.divide(dame['structural~complete_r1'], dame['number']).mean(); print("sDtr_Complete_r1 = "+str(round(sDtr_Complete_r1,2))+" ["+str(round(np.divide(dame['structural~complete_r1'], dame['number'])[40],2))+"]")
sDt_Collapse_r1 = np.multiply(conse['collapse_ratio_r1'],conse['number']).sum(); print("sDt_Collapse_r1 = "+str(round(sDt_Collapse_r1,0))+" ["+str(round(np.multiply(conse['collapse_ratio_r1'],conse['number'])[40],0))+"]") #collapse_ratio is per building, so multiply by building before summing
sDtr_Collapse_r1 = conse['collapse_ratio_r1'].mean(); print("sDtr_Collapse_r1 = "+str(round(sDtr_Collapse_r1,2))+" ["+str(round(conse['collapse_ratio_r1'][40],2))+"]")

###################################################################################################
print("")
print("Recovery Time - baseline")
sCm_Interruption_b0 = conse['mean_interruption_time_b0'].mean(); print("sCm_Interruption_b0 = "+str(round(sCm_Interruption_b0,0))+" ["+str(round(conse['mean_interruption_time_b0'][40],0))+"]")
sCm_Repair_b0 = conse['mean_repair_time_b0'].mean(); print("sCm_Repair_b0 = "+str(round(sCm_Repair_b0,0))+" ["+str(round(conse['mean_repair_time_b0'][40],0))+"]")
sCm_Recovery_b0 = conse['mean_recovery_time_b0'].mean(); print("sCm_Recovery_b0 = "+str(round(sCm_Recovery_b0,0))+" ["+str(round(conse['mean_recovery_time_b0'][40],0))+"]")
sCt_DebrisTotal_b0 = conse['debris_brick_wood_tons_b0'].sum() + conse['debris_concrete_steel_tons_b0'].sum(); print("sCt_DebrisTotal_b0 = "+str(round(sCt_DebrisTotal_b0,-3))+" ["+str(round(conse['debris_brick_wood_tons_b0'][40],-3))+"]")
sCt_DebrisBW_b0 = conse['debris_brick_wood_tons_b0'].sum(); print("sCt_DebrisBW_b0 = "+str(round(sCt_DebrisBW_b0,-3))+" ["+str(round(conse['debris_brick_wood_tons_b0'][40],-3))+"]")
sCt_DebrisCS_b0 = conse['debris_concrete_steel_tons_b0'].sum(); print("sCt_DebrisCS_b0 = "+str(round(sCt_DebrisCS_b0,-3))+" ["+str(round(conse['debris_concrete_steel_tons_b0'][40],-3))+"]")

###################################################################################################
print("")
print("Recovery Time - retrofit")
sCm_Interruption_r1 = conse['mean_interruption_time_r1'].mean(); print("sCm_Interruption_r1 = "+str(round(sCm_Interruption_r1,0))+" ["+str(round(conse['mean_interruption_time_r1'][40],0))+"]")
sCm_Repair_r1 = conse['mean_repair_time_r1'].mean(); print("sCm_Repair_r1 = "+str(round(sCm_Repair_r1,0))+" ["+str(round(conse['mean_repair_time_r1'][40],0))+"]")
sCm_Recovery_r1 = conse['mean_recovery_time_r1'].mean(); print("sCm_Recovery_r1 = "+str(sCm_Recovery_r1)+" ["+str(conse['mean_recovery_time_r1'][40])+"]")
sCt_DebrisTotal_r1 = conse['debris_brick_wood_tons_r1'].sum() + conse['debris_concrete_steel_tons_r1'].sum(); print("sCt_DebrisTotal_r1 = "+str(round(sCt_DebrisTotal_r1,-3))+" ["+str(round(conse['debris_brick_wood_tons_r1'][40],-3))+"]")
sCt_DebrisBW_r1 = conse['debris_brick_wood_tons_r1'].sum(); print("sCt_DebrisBW_r1 = "+str(round(sCt_DebrisBW_r1,-3))+" ["+str(round(conse['debris_brick_wood_tons_r1'][40],-3))+"]")
sCt_DebrisCS_r1 = conse['debris_concrete_steel_tons_r1'].sum(); print("sCt_DebrisCS_r1 = "+str(round(sCt_DebrisCS_r1,-3))+" ["+str(round(conse['debris_concrete_steel_tons_r1'][40],-3))+"]")

###################################################################################################
print("")
print("Casualties - baseline")
sCt_CasDayL1_b0 = conse['casualties_day_severity_1_b0'].sum(); print("sCt_CasDayL1_b0 = "+str(round(sCt_CasDayL1_b0,0))+" ["+str(round(conse['casualties_day_severity_1_b0'][40],0))+"]")
sCt_CasDayL2_b0 = conse['casualties_day_severity_2_b0'].sum(); print("sCt_CasDayL2_b0 = "+str(round(sCt_CasDayL2_b0,0))+" ["+str(round(conse['casualties_day_severity_2_b0'][40],0))+"]")
sCt_CasDayL3_b0 = conse['casualties_day_severity_3_b0'].sum(); print("sCt_CasDayL3_b0 = "+str(round(sCt_CasDayL3_b0,0))+" ["+str(round(conse['casualties_day_severity_3_b0'][40],0))+"]")
sCt_CasDayL4_b0 = conse['casualties_day_severity_4_b0'].sum(); print("sCt_CasDayL4_b0 = "+str(round(sCt_CasDayL4_b0,0))+" ["+str(round(conse['casualties_day_severity_4_b0'][40],0))+"]")
sCt_CasNightL1_b0 = conse['casualties_night_severity_1_b0'].sum(); print("sCt_CasNightL1_b0 = "+str(round(sCt_CasNightL1_b0,0))+" ["+str(round(conse['casualties_night_severity_1_b0'][40],0))+"]")
sCt_CasNightL2_b0 = conse['casualties_night_severity_2_b0'].sum(); print("sCt_CasNightL2_b0 = "+str(round(sCt_CasNightL2_b0,0))+" ["+str(round(conse['casualties_night_severity_2_b0'][40],0))+"]")
sCt_CasNightL3_b0 = conse['casualties_night_severity_3_b0'].sum(); print("sCt_CasNightL3_b0 = "+str(round(sCt_CasNightL3_b0,0))+" ["+str(round(conse['casualties_night_severity_3_b0'][40],0))+"]")
sCt_CasNightL4_b0 = conse['casualties_night_severity_4_b0'].sum(); print("sCt_CasNightL4_b0 = "+str(round(sCt_CasNightL4_b0,0))+" ["+str(round(conse['casualties_night_severity_4_b0'][40],0))+"]")
sCt_CasTransitL1_b0 = conse['casualties_transit_severity_1_b0'].sum(); print("sCt_CasTransitL1_b0 = "+str(round(sCt_CasTransitL1_b0,0))+" ["+str(round(conse['casualties_transit_severity_1_b0'][40],0))+"]")
sCt_CasTransitL2_b0 = conse['casualties_transit_severity_2_b0'].sum(); print("sCt_CasTransitL2_b0 = "+str(round(sCt_CasTransitL2_b0,0))+" ["+str(round(conse['casualties_transit_severity_2_b0'][40],0))+"]")
sCt_CasTransitL3_b0 = conse['casualties_transit_severity_3_b0'].sum(); print("sCt_CasTransitL3_b0 = "+str(round(sCt_CasTransitL3_b0,0))+" ["+str(round(conse['casualties_transit_severity_3_b0'][40],0))+"]")
sCt_CasTransitL4_b0 = conse['casualties_transit_severity_4_b0'].sum(); print("sCt_CasTransitL4_b0 = "+str(round(sCt_CasTransitL4_b0,0))+" ["+str(round(conse['casualties_transit_severity_4_b0'][40],0))+"]")

###################################################################################################
print("")
print("Casualties - retrofit")
sCt_CasDayL1_r1 = conse['casualties_day_severity_1_r1'].sum(); print("sCt_CasDayL1_r1 = "+str(round(sCt_CasDayL1_r1,0))+" ["+str(round(conse['casualties_day_severity_1_r1'][40],0))+"]")
sCt_CasDayL2_r1 = conse['casualties_day_severity_2_r1'].sum(); print("sCt_CasDayL2_r1 = "+str(round(sCt_CasDayL2_r1,0))+" ["+str(round(conse['casualties_day_severity_2_r1'][40],0))+"]")
sCt_CasDayL3_r1 = conse['casualties_day_severity_3_r1'].sum(); print("sCt_CasDayL3_r1 = "+str(round(sCt_CasDayL3_r1,0))+" ["+str(round(conse['casualties_day_severity_3_r1'][40],0))+"]")
sCt_CasDayL4_r1 = conse['casualties_day_severity_4_r1'].sum(); print("sCt_CasDayL4_r1 = "+str(round(sCt_CasDayL4_r1,0))+" ["+str(round(conse['casualties_day_severity_4_r1'][40],0))+"]")
sCt_CasNightL1_r1 = conse['casualties_night_severity_1_r1'].sum(); print("sCt_CasNightL1_r1 = "+str(round(sCt_CasNightL1_r1,0))+" ["+str(round(conse['casualties_night_severity_1_r1'][40],0))+"]")
sCt_CasNightL2_r1 = conse['casualties_night_severity_2_r1'].sum(); print("sCt_CasNightL2_r1 = "+str(round(sCt_CasNightL2_r1,0))+" ["+str(round(conse['casualties_night_severity_2_r1'][40],0))+"]")
sCt_CasNightL3_r1 = conse['casualties_night_severity_3_r1'].sum(); print("sCt_CasNightL3_r1 = "+str(round(sCt_CasNightL3_r1,0))+" ["+str(round(conse['casualties_night_severity_3_r1'][40],0))+"]")
sCt_CasNightL4_r1 = conse['casualties_night_severity_4_r1'].sum(); print("sCt_CasNightL4_r1 = "+str(round(sCt_CasNightL4_r1,0))+" ["+str(round(conse['casualties_night_severity_4_r1'][40],0))+"]")
sCt_CasTransitL1_r1 = conse['casualties_transit_severity_1_r1'].sum(); print("sCt_CasTransitL1_r1 = "+str(round(sCt_CasTransitL1_r1,0))+" ["+str(round(conse['casualties_transit_severity_1_r1'][40],0))+"]")
sCt_CasTransitL2_r1 = conse['casualties_transit_severity_2_r1'].sum(); print("sCt_CasTransitL2_r1 = "+str(round(sCt_CasTransitL2_r1,0))+" ["+str(round(conse['casualties_transit_severity_2_r1'][40],0))+"]")
sCt_CasTransitL3_r1 = conse['casualties_transit_severity_3_r1'].sum(); print("sCt_CasTransitL3_r1 = "+str(round(sCt_CasTransitL3_r1,0))+" ["+str(round(conse['casualties_transit_severity_3_r1'][40],0))+"]")
sCt_CasTransitL4_r1 = conse['casualties_transit_severity_4_r1'].sum(); print("sCt_CasTransitL4_r1 = "+str(round(sCt_CasTransitL4_r1,0))+" ["+str(round(conse['casualties_transit_severity_4_r1'][40],0))+"]")

###################################################################################################
print("")
print("Social Disruption - baseline")

######## start of displaced households calc
dame['#Fams'] = '-'; dame.loc[dame.OccClass.isin(SF), '#Fams'] = 'SF'; dame.loc[dame.OccClass.isin(MF), '#Fams'] = 'MF'
displ = dame[dame['#Fams'].isin(['SF', 'MF'])] #isolate only residential buildings
conditions = [displ['#Fams'] == 'SF', displ['#Fams'] == 'MF']
choices = [(np.multiply((displ['structural~moderate_b0']/displ['number']), DSPLCHSW['SF']['wM']) + np.multiply((displ['structural~extensive_b0']/displ['number']), DSPLCHSW['SF']['wE']) + np.multiply((displ['structural~complete_b0']/displ['number']), DSPLCHSW['SF']['wC'])), (np.multiply((displ['structural~moderate_b0']/displ['number']), DSPLCHSW['MF']['wM']) + np.multiply((displ['structural~extensive_b0']/displ['number']), DSPLCHSW['MF']['wE']) + np.multiply((displ['structural~complete_b0']/displ['number']), DSPLCHSW['MF']['wC']))]
displ['wt'] = np.select(conditions, choices) #weighted probability of being displaced (based on HAZUS table) - equivalent to %SF or %MF depending on asset type
conditions2 = [displ['OccClass'] == 'RES1',
               displ['OccClass'] == 'RES2', 
               displ['OccClass'] == 'RES3A',
               displ['OccClass'] == 'RES3B',
               displ['OccClass'] == 'RES3C',
               displ['OccClass'] == 'RES3D',
               displ['OccClass'] == 'RES3E',
               displ['OccClass'] == 'RES3F',
               displ['OccClass'] == 'RES4',
               displ['OccClass'] == 'RES5',
               displ['OccClass'] == 'RES6']
choices2 = [1, 1, 2, 4, 9, 17, 32, 110, 68, 50, 65]
displ['unitsPerBldg'] = np.select(conditions2, choices2)
displ['numUnits'] = np.multiply(displ['number'], displ['unitsPerBldg'])
sCt_Hshld3_b0 = np.multiply(displ['wt'], displ['numUnits']).sum()
######## end of displaced households calc
####### start of shelter needs calc
census_info = census[census['SAUIDi'] == SAUID]
ppl = (sCt_Hshld3_b0*dame['night'].sum())/(displ['numUnits'].sum())
conHI = [census_info['Inc_Hshld'] <= 15000,
        (census_info['Inc_Hshld'] > 15000) & (census_info['Inc_Hshld'] <= 20000),
        (census_info['Inc_Hshld'] > 20000) & (census_info['Inc_Hshld'] <= 35000),
        (census_info['Inc_Hshld'] > 35000) & (census_info['Inc_Hshld'] <= 50000),
        census_info['Inc_Hshld'] > 50000]
choiceHI = [[1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1]]
HI = np.select(conHI, choiceHI)
HE = [census_info['Vis_Min'].values[0], census_info['Indigenous'].values[0], 1-census_info['Vis_Min'].values[0]-census_info['Indigenous'].values[0]] #[visible minorities, indigenous, not visible minorities]
HO = [1-census_info['Renter'].values[0], census_info['Renter'].values[0]] #[owners, renters]
HA = [census_info['Age_LT6'].values[0], 1-(census_info['Age_LT6'].values[0]+census_info['Age_GT65'].values[0]), census_info['Age_GT65'].values[0]] #[under6, 6-65, over65]
STP = 0.0
for i in range(len(IM)):
    for j in range(len(EM)):
        for k in range(len(OM)):
            for l in range(len(AM)):
                    alpha = (IW*IM[i]) + (EW*EM[j]) + (OW*OM[k]) + (AW*AM[l])
                    STP = STP + (alpha*ppl*HI[i]*HE[j]*HO[k]*HA[l])

####### end of shelter needs calc
sCt_Shelter_b0 = STP; print("sCt_Shelter_b0 = "+str(round(sCt_Shelter_b0,0)))
sCt_Res3_b0 = conse['sc_Displ3_b0'].sum(); print("sCt_Res3_b0 = "+str(round(sCt_Res3_b0,-1))+" ["+str(round(conse['sc_Displ3_b0'][40],-1))+"]")
sCt_Res30_b0 = conse['sc_Displ30_b0'].sum(); print("sCt_Res30_b0 = "+str(round(sCt_Res30_b0,0))+" ["+str(round(conse['sc_Displ30_b0'][40],0))+"]")
sCt_Res90_b0 = conse['sc_Displ90_b0'].sum(); print("sCt_Res90_b0 = "+str(round(sCt_Res90_b0,0))+" ["+str(round(conse['sc_Displ90_b0'][40],0))+"]")
sCr_DisplRes90_b0 = np.divide(conse['sc_Displ90_b0'].sum(),conse['night'].sum()); print("sCr_DisplRes90_b0 = "+str(round(sCr_DisplRes90_b0,2))+" ["+str(round(np.divide(conse['sc_Displ90_b0'],conse['night'])[40],2))+"]")
sCt_Res180_b0 = conse['sc_Displ180_b0'].sum(); print("sCt_Res180_b0 = "+str(round(sCt_Res180_b0,0))+" ["+str(round(conse['sc_Displ180_b0'][40],0))+"]")
sCt_Res360_b0 = conse['sc_Displ360_b0'].sum(); print("sCt_Res360_b0 = "+str(round(sCt_Res360_b0,0))+" ["+str(round(conse['sc_Displ360_b0'][40],0))+"]")
print("sCt_Hshld_b0 = "+str(round(sCt_Hshld3_b0,0))+" ["+str(round(np.multiply(displ['wt'], displ['numUnits'])[40],0))+"]")
sCt_Empl30_b0 = conse['sc_BusDispl30_b0'].sum(); print("sCt_Empl30_b0 = "+str(round(sCt_Empl30_b0,0))+" ["+str(round(conse['sc_BusDispl30_b0'][40],0))+"]")
sCt_Empl90_b0 = conse['sc_BusDispl90_b0'].sum(); print("sCt_Empl90_b0 = "+str(round(sCt_Empl90_b0,0))+" ["+str(round(conse['sc_BusDispl90_b0'][40],0))+"]")
sCr_Empl90_b0 = np.divide(conse['sc_BusDispl90_b0'].sum(),conse['day'].sum()); print("sCr_Empl90_b0 = "+str(round(sCr_Empl90_b0,2))+" ["+str(round(np.divide(conse['sc_BusDispl90_b0'],conse['day'])[40],2))+"]")
sCt_Empl180_b0 = conse['sc_BusDispl180_b0'].sum(); print("sCt_Empl180_b0 = "+str(round(sCt_Empl180_b0,0))+" ["+str(round(conse['sc_BusDispl180_b0'][40],0))+"]")
sCt_Empl360_b0 = conse['sc_BusDispl360_b0'].sum(); print("sCt_Empl360_b0 = "+str(round(sCt_Empl360_b0,0))+" ["+str(round(conse['sc_BusDispl360_b0'][40],0))+"]")

###################################################################################################
print("")
print("Social Disruption - retrofit")
choicesr1 = [(np.multiply((displ['structural~moderate_r1']/displ['number']), DSPLCHSW['SF']['wM']) + np.multiply((displ['structural~extensive_r1']/displ['number']), DSPLCHSW['SF']['wE']) + np.multiply((displ['structural~complete_r1']/displ['number']), DSPLCHSW['SF']['wC'])), (np.multiply((displ['structural~moderate_r1']/displ['number']), DSPLCHSW['MF']['wM']) + np.multiply((displ['structural~extensive_r1']/displ['number']), DSPLCHSW['MF']['wE']) + np.multiply((displ['structural~complete_r1']/displ['number']), DSPLCHSW['MF']['wC']))]
displ['wtr1'] = np.select(conditions, choicesr1)
sCt_Hshld3_r1 = np.multiply(displ['wtr1'], displ['numUnits']).sum()
ppl = (sCt_Hshld3_r1*dame['night'].sum())/(displ['numUnits'].sum())
STP = 0.0
for i in range(len(IM)):
    for j in range(len(EM)):
        for k in range(len(OM)):
            for l in range(len(AM)):
                    alpha = (IW*IM[i]) + (EW*EM[j]) + (OW*OM[k]) + (AW*AM[l])
                    STP = STP + (alpha*ppl*HI[i]*HE[j]*HO[k]*HA[l])
print("sCt_Shelter_r1 = "+str(round(STP,0)))
sCt_Res3_r1 = conse['sc_Displ3_r1'].sum(); print("sCt_Res3_r1 = "+str(round(sCt_Res3_r1,-1))+" ["+str(round(conse['sc_Displ3_r1'][40],-1))+"]")
sCt_Res30_r1 = conse['sc_Displ30_r1'].sum(); print("sCt_Res30_r1 = "+str(round(sCt_Res30_r1,0))+" ["+str(round(conse['sc_Displ30_r1'][40],0))+"]")
sCt_Res90_r1 = conse['sc_Displ90_r1'].sum(); print("sCt_Res90_r1 = "+str(round(sCt_Res90_r1,0))+" ["+str(round(conse['sc_Displ90_r1'][40],0))+"]")
sCr_DisplRes90_r1 = np.divide(conse['sc_Displ90_r1'].sum(),conse['night'].sum()); print("sCr_DisplRes90_r1 = "+str(round(sCr_DisplRes90_r1,2))+" ["+str(round(np.divide(conse['sc_Displ90_r1'],conse['night'])[40],2))+"]")
sCt_Res180_r1 = conse['sc_Displ180_r1'].sum(); print("sCt_Res180_r1 = "+str(round(sCt_Res180_r1,0))+" ["+str(round(conse['sc_Displ180_r1'][40],0))+"]")
sCt_Res360_r1 = conse['sc_Displ360_r1'].sum(); print("sCt_Res360_r1 = "+str(round(sCt_Res360_r1,0))+" ["+str(round(conse['sc_Displ360_r1'][40],0))+"]")
print("sCt_Hshld_r1 = "+str(round(sCt_Hshld3_r1,0))+" ["+str(round(np.multiply(displ['wtr1'], displ['numUnits'])[40],0))+"]")
sCt_Empl30_r1 = conse['sc_BusDispl30_r1'].sum(); print("sCt_Empl30_r1 = "+str(round(sCt_Empl30_r1,0))+" ["+str(round(conse['sc_BusDispl30_r1'][40],0))+"]")
sCt_Empl90_r1 = conse['sc_BusDispl90_r1'].sum(); print("sCt_Empl90_r1 = "+str(round(sCt_Empl90_r1,0))+" ["+str(round(conse['sc_BusDispl90_r1'][40],0))+"]")
sCr_Empl90_b0 = np.divide(conse['sc_BusDispl90_b0'].sum(),conse['day'].sum()); print("sCr_Empl90_b0 = "+str(round(sCr_Empl90_b0,2))+" ["+str(round(np.divide(conse['sc_BusDispl90_b0'],conse['day'])[40],2))+"]")
sCt_Empl180_r1 = conse['sc_BusDispl180_r1'].sum(); print("sCt_Empl180_r1 = "+str(round(sCt_Empl180_r1,0))+" ["+str(round(conse['sc_BusDispl180_r1'][40],0))+"]")
sCt_Empl360_r1 = conse['sc_BusDispl360_r1'].sum(); print("sCt_Empl360_r1 = "+str(round(sCt_Empl360_r1,0))+" ["+str(round(conse['sc_BusDispl360_r1'][40],0))+"]")

###################################################################################################
print("")
print("Economic Security - baseline")
sLt_Asset_b0 = losse['totalLoss_b0'].sum(); print("sLt_Asset_b0 = "+str(round(sLt_Asset_b0,-4))+" ["+str(round(losse['totalLoss_b0'][40],-4))+"]")
sLm_Asset_b0 = np.average(np.divide(losse['totalLoss_b0'], (losse['structural']+losse['nonstructural']+losse['contents']))); print("sLm_Asset_b0 = "+str(round(sLm_Asset_b0,2))+" ["+str(round(np.divide(losse['totalLoss_b0'], (losse['structural']+losse['nonstructural']+losse['contents']))[40],2))+"]") # total loss divided by replacement cost for each asset, averaged over all assets
sLt_Bldg_b0 = losse['nonstructural_b0'].sum() + losse['structural_b0'].sum(); print("sLt_Bldg_b0 = "+str(round(sLt_Bldg_b0,-4))+" ["+str(round((losse['nonstructural_b0'] + losse['structural_b0'])[40],-4))+"]")
sLmr_Bldg_b0 = np.average(np.divide((losse['structural_b0']+losse['nonstructural_b0']), (losse['structural']+losse['nonstructural']))); print("sLmr_Bldg_b0 = "+str(round(sLmr_Bldg_b0,2))+" ["+str(round(np.divide((losse['structural_b0']+losse['nonstructural_b0']), (losse['structural']+losse['nonstructural']))[40],2))+"]") # str+nonstr loss divided by replacement str+nonstr cost for each asset, averaged over all assets
sLt_Str_b0 = losse['structural_b0'].sum(); print("sLt_Str_b0 = "+str(round(sLt_Str_b0,-4))+" ["+str(round(losse['structural_b0'][40],-4))+"]")
sLt_Nstr_b0 = losse['nonstructural_b0'].sum(); print("sLt_Nstr_b0 = "+str(round(sLt_Nstr_b0,-4))+" ["+str(round(losse['nonstructural_b0'][40],-4))+"]")
sLt_Cont_b0 = losse['contents_b0'].sum(); print("sLt_Cont_b0 = "+str(round(sLt_Cont_b0,-4))+" ["+str(round(losse['contents_b0'][40],-4))+"]")

###################################################################################################
print("")
print("Economic Security - retrofit")
sLt_Asset_r1 = losse['totalLoss_r1'].sum(); print("sLt_Asset_r1 = "+str(round(sLt_Asset_r1,-4))+" ["+str(round(losse['totalLoss_r1'][40],-4))+"]")
sLm_Asset_r1 = np.average(np.divide(losse['totalLoss_r1'], (losse['structural']+losse['nonstructural']+losse['contents']))); print("sLm_Asset_r1 = "+str(round(sLm_Asset_r1,2))+" ["+str(round(np.divide(losse['totalLoss_r1'], (losse['structural']+losse['nonstructural']+losse['contents']))[40],2))+"]") # total loss divided by replacement cost for each asset, averaged over all assets
sLt_Bldg_r1 = losse['nonstructural_r1'].sum() + losse['structural_r1'].sum(); print("sLt_Bldg_r1 = "+str(round(sLt_Bldg_r1,-4))+" ["+str(round((losse['nonstructural_r1'] + losse['structural_r1'])[40],-4))+"]")
sLmr_Bldg_r1 = np.average(np.divide((losse['structural_r1']+losse['nonstructural_r1']), (losse['structural']+losse['nonstructural']))); print("sLmr_Bldg_r1 = "+str(round(sLmr_Bldg_r1,2))+" ["+str(round(np.divide((losse['structural_r1']+losse['nonstructural_r1']), (losse['structural']+losse['nonstructural']))[40],2))+"]") # str+nonstr loss divided by replacement str+nonstr cost for each asset, averaged over all assets
sLt_Str_r1 = losse['structural_r1'].sum(); print("sLt_Str_r1 = "+str(round(sLt_Str_r1,-4))+" ["+str(round(losse['structural_r1'][40],-4))+"]")
sLt_Nstr_r1 = losse['nonstructural_r1'].sum(); print("sLt_Nstr_r1 = "+str(round(sLt_Nstr_r1,-4))+" ["+str(round(losse['nonstructural_r1'][40],-4))+"]")
sLt_Cont_r1 = losse['contents_r1'].sum(); print("sLt_Cont_r1 = "+str(round(sLt_Cont_r1,-4))+" ["+str(round(losse['contents_r1'][40],-4))+"]")
