#!/usr/bin/env python

#Import statements
import xml.etree.ElementTree as et
import configparser
import argparse
import os
import numpy as np
import sys

sys.path.append('/Users/thobbs/oq-platform-ipt')
from openquakeplatform_ipt import build_rupture_plane
from datetime import datetime
from shutil import copyfile

#Main Function
def main():
    args = parse_args() #grabs the ini file
    os.system('') #something from stack exchange
    configParser = get_config_params(args)
    runName = configParser.get('General', 'RunName')
    tectoRegion = configParser.get('General', 'tectoRegion')
    taxonomy_mapping_csv_baseline = configParser.get('File Paths', 'taxonomy_mapping_csv_baseline')

    # Save config  file as {runName}.ini for future reference
    if not os.path.exists('manyFaults'):
        os.makedirs('manyFaults')
    with open('manyFaults/manyFaults_{}_{}.ini'.format(runName, datetime.today().strftime('%Y%m%d')), 'w') as configfile:
        configParser.write(configfile)

    if not os.path.exists(configParser.get('File Paths', 'outdir')):
        os.makedirs(configParser.get('File Paths', 'outdir'))
    os.chdir(configParser.get('File Paths', 'outdir'))

    ### Creating retrofit files?
    if configParser.get('General', 'runAllRetrofits') == 'True':
        print("Creating ini's for all retrofit scenarios")
        #retroList = ['b0','r1','r2']
        retroList = ['b0','r1']
        taxoMapDict = {retroList[0]:taxonomy_mapping_csv_baseline,
                       retroList[1]:taxonomy_mapping_csv_retrofit}
    else:
        retroList = ['b0']
        taxoMapDict = {retroList[0]:taxonomy_mapping_csv_baseline}
    
    ### Creating rupture files?
    if configParser.get('General', 'generate_ruptures') == 'True':
        magnitudeList = list(np.float_(configParser.get('Moment Magnitude', 'mag')[1:-2].split(':')))
        if len(magnitudeList) >= 2:
            magnitudeList = np.linspace(magnitudeList[0], magnitudeList[2], endpoint=True, num=round((magnitudeList[2]-magnitudeList[0])/magnitudeList[1])+1)
            magnitudeList = ["%.1f" % e for e in magnitudeList] #Set Floating point precision

        strikeList = list(np.float_(configParser.get('Strike', 'strike')[1:-2].split(':')))
        if len(strikeList) >= 2:
            strikeList = np.linspace(strikeList[0], strikeList[2], endpoint=True, num=round((strikeList[2]-strikeList[0])/strikeList[1])+1)
            strikeList = ["%.1f" % e for e in strikeList] #Set Floating point precision

        dipList = list(np.float_(configParser.get('Dip', 'dip')[1:-2].split(':')))
        if len(dipList) >= 2:
            dipList = np.linspace(dipList[0], dipList[2], endpoint=True, num=round((dipList[2]-dipList[0])/dipList[1])+1)
            dipList = ["%.0f" % e for e in dipList] #Set Floating point precision #decimel for dip

        rakeList = list(np.float_(configParser.get('Rake', 'rake')[1:-2].split(':')))
        if len(rakeList) >= 2:
            rakeList = np.linspace(rakeList[0], rakeList[2], endpoint=True, num=round((rakeList[2]-rakeList[0])/rakeList[1])+1)
            rakeList = ["%.1f" % e for e in rakeList] #Set Floating point precision

        #poslist = list(filter(None, (x.strip() for x in configParser.get('Fault Position List', 'poslist').splitlines())))
        #poslist = '\n                    '+' \n                    '.join(poslist)

        hypocenter_str_dict = dict(zip(['lat', 'lon', 'depth'], list(configParser.get('Hypocenter', 'LatLonDepth')[1:-2].split(','))))
        hypocenter = dict(zip(['lat', 'lon', 'depth'], list(configParser.get('Hypocenter', 'LatLonDepth')[1:-2].split(','))))
        hypocenter.update({'lat': float(hypocenter['lat'])})
        hypocenter.update({'lon': float(hypocenter['lon'])})
        hypocenter.update({'depth': float(hypocenter['depth'])})


        i=len(magnitudeList)*len(dipList)*len(rakeList)*len(strikeList)
        if input("About to Generate %d scenarios. Proceed? (y/n):" % i).lower() == 'y':
            pass
        else:
            sys.exit('Exiting. No Scenarios Generated')
        print('Proceeding')

        for magnitude in magnitudeList:
            for strike in strikeList:
                for dip in dipList:
                    for rake in rakeList:
                        runID = str(tectoRegion)+"M"+str(magnitude).split('.')[0]+"p"+str(magnitude).split('.')[1]
                        convertArbitraryFault2nrml(magnitude, hypocenter, hypocenter_str_dict, strike, dip, rake, runName, runID)
                        ruptureFile = "../ruptures/rupture_"+str(runID)+"_"+str(runName)+".xml"
                        write_hazard_config(runName, runID, ruptureFile, configParser)
                        for retro in retroList:
                            print(retro)
                            write_damage_config(runName, runID, ruptureFile, retro, taxoMapDict, configParser)
                            write_risk_config(runName, runID, ruptureFile, retro, taxoMapDict, configParser)
                        
    else:
        # If already have a rupture file in mind, just generate damage and risk ini files
        ruptureFile = configParser.get('File Paths', 'rupture_model_file')
        print("NOT generating fault ruptures, instead using:  " + str(ruptureFile))
        runID = os.path.basename(ruptureFile).split('_')[1]
        write_hazard_config(runName, runID, ruptureFile, configParser)
        for retro in retroList:
            print(retro)
            write_damage_config(runName, runID, ruptureFile, retro, taxoMapDict, configParser)
            write_risk_config(runName, runID, ruptureFile, retro, taxoMapDict, configParser)
    
    print('Done')

#Suport Functions
def convertArbitraryFault2nrml(magnitude, hypocenter, hypocenter_str_dict, strike, dip, rake, runName, runID):
    root = et.Element("nrml", {"xmlns:gml":"http://www.opengis.net/gml",   "xmlns":"http://openquake.org/xmlns/nrml/0.4"})
    rupture = et.SubElement(root,"singlePlaneRupture")
    magnitudeElem = et.SubElement(rupture, "magnitude")
    magnitudeElem.text = str(magnitude)
    rakeElem = et.SubElement(rupture, 'rake')
    rakeElem.text = str(rake)
    rupture_plane = build_rupture_plane.get_rupture_surface(float(magnitude), hypocenter, float(strike), float(dip), float(rake))
    hypoCenterElem = et.SubElement(rupture, "hypocenter", hypocenter_str_dict)
    planSurfStrikeDip = dict(zip(['dip', 'strike'], [str(dip), str(strike)]))

    for corner_key, corner in rupture_plane.items():
        for key, coord in rupture_plane[corner_key].items():
            rupture_plane[corner_key][key] = str(coord)

    planarSurface = et.SubElement(rupture,'planarSurface', planSurfStrikeDip)
    topLeftElem = et.SubElement(planarSurface, 'topLeft', rupture_plane['topLeft'])
    topRightElem = et.SubElement(planarSurface, 'topRight', rupture_plane['topRight'])
    bottomLeftElem = et.SubElement(planarSurface, 'bottomLeft', rupture_plane['bottomLeft'])
    bottomRightElem = et.SubElement(planarSurface, 'bottomRight', rupture_plane['bottomRight'])
    indent(root)
    tree= et.ElementTree(root)
    if not os.path.exists('ruptures/'):
        os.makedirs('ruptures/')
    return tree.write('ruptures/rupture_%s_%s.xml' % (runID, runName), encoding="utf-8",xml_declaration=True, method="xml")

def indent(elem, level=0):
    i = "\n" + level*"    "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "    "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def write_hazard_config(runName, runID, ruptureFile, configParser):
    hazardConfig = configparser.ConfigParser(allow_no_value=True)
    hazardConfig['general'] = {}
    hazardConfig['general']['description'] = configParser.get('General', 'description')
    hazardConfig['general']['calculation_mode'] = 'scenario'
    hazardConfig['general']['random_seed'] = configParser.get('General', 'random_seed') 
    
    hazardConfig['site_params'] = {}
    hazardConfig['site_params']['site_model_file'] = configParser.get('File Paths', 'HazardSites')
    
    hazardConfig['Rupture information'] = {}
    hazardConfig['Rupture information']['rupture_model_file'] = ruptureFile
    hazardConfig['Rupture information']['rupture_mesh_spacing'] = configParser.get('General', 'RuptureMeshSpacing')
    
    hazardConfig['Calculation parameters'] = {}
    hazardConfig['Calculation parameters']['gsim_logic_tree_file'] = configParser.get('File Paths', 'GMPE')
    hazardConfig['Calculation parameters']['truncation_level'] = '0'
    hazardConfig['Calculation parameters']['maximum_distance'] = configParser.get('General', 'maximum_distance')
    hazardConfig['Calculation parameters']['number_of_ground_motion_fields'] = '1'
    hazardConfig['Calculation parameters']['intensity_measure_types'] = configParser.get('File Paths', 'intensity_measure_types')
    
    with open('initializations/s_Hazard_%s_%s.ini' %(runID, runName), 'w') as configfile:
        configfile.write('# Generated automatically with manyFaults.py on: '+ str(datetime.now())+'\n')
        hazardConfig.write(configfile)
    return
    
def write_damage_config(runName, runID, ruptureFile, retro, taxoMapDict, configParser):
    damageConfig = configparser.ConfigParser(allow_no_value=True)
    damageConfig['general'] = {}
    damageConfig['general']['description'] = configParser.get('General', 'description')
    damageConfig['general']['calculation_mode'] = 'scenario_damage'
    damageConfig['general']['random_seed'] = configParser.get('General', 'random_seed')

    damageConfig['Exposure model'] = {}
    damageConfig['Exposure model']['exposure_file'] = configParser.get('File Paths', 'exposure_file')
    if 'Site' in damageConfig['Exposure model']['exposure_file']:
        expoSuffix = 's'
    else:
        expoSuffix = 'b'

    damageConfig['site_params'] = {}
    damageConfig['site_params']['site_model_file'] = configParser.get('File Paths', 'SiteParams')

    damageConfig['Rupture information'] = {}
    damageConfig['Rupture information']['rupture_model_file'] = ruptureFile
    damageConfig['Rupture information']['rupture_mesh_spacing'] = configParser.get('General', 'RuptureMeshSpacing')

    damageConfig['Calculation parameters'] = {}
    damageConfig['Calculation parameters']['gsim_logic_tree_file'] = configParser.get('File Paths', 'GMPE') 
    damageConfig['Calculation parameters']['truncation_level'] = configParser.get('General', 'truncation_level')
    damageConfig['Calculation parameters']['maximum_distance'] = configParser.get('General', 'maximum_distance')
    damageConfig['Calculation parameters']['number_of_ground_motion_fields'] = configParser.get('General', 'number_of_ground_motion_fields')

    damageConfig['fragility'] = {}
    damageConfig['fragility']['taxonomy_mapping_csv'] = taxoMapDict.get(retro) 
    damageConfig['fragility']['structural_fragility_file'] = configParser.get('File Paths', 'structural_fragility_file') 
    
    damageConfig['risk_calculation'] = {}
    damageConfig['risk_calculation']['master_seed'] = configParser.get('General', 'master_seed') 
    damageConfig['risk_calculation']['time_event'] = configParser.get('General', 'time_event') 

    with open('initializations/s_Damage_%s_%s_%s_%s.ini' %(runID, runName, retro, expoSuffix), 'w') as configfile:
        configfile.write('# Generated automatically with manyFaults.py on: '+ str(datetime.now())+'\n')
        damageConfig.write(configfile)
    return

def write_risk_config(runName, runID, ruptureFile, retro, taxoMapDict, configParser):
    riskConfig = configparser.ConfigParser(allow_no_value=True)
    riskConfig['general'] = {}
    riskConfig['general']['description'] = configParser.get('General', 'description')
    riskConfig['general']['calculation_mode'] = 'scenario_risk'
    riskConfig['general']['random_seed'] = configParser.get('General', 'random_seed')

    riskConfig['Exposure model'] = {}
    riskConfig['Exposure model']['exposure_file'] = configParser.get('File Paths', 'exposure_file')
    if 'Site' in riskConfig['Exposure model']['exposure_file']:
        expoSuffix = 's'
    else:
        expoSuffix = 'b'

    riskConfig['site_params'] = {}
    riskConfig['site_params']['site_model_file'] = configParser.get('File Paths', 'SiteParams')

    riskConfig['Rupture information'] = {}
    riskConfig['Rupture information']['rupture_model_file'] = ruptureFile
    riskConfig['Rupture information']['rupture_mesh_spacing'] = configParser.get('General', 'RuptureMeshSpacing')

    riskConfig['Calculation parameters'] = {}
    riskConfig['Calculation parameters']['gsim_logic_tree_file'] = configParser.get('File Paths', 'GMPE') 
    riskConfig['Calculation parameters']['truncation_level'] = configParser.get('General', 'truncation_level')
    riskConfig['Calculation parameters']['maximum_distance'] = configParser.get('General', 'maximum_distance')
    riskConfig['Calculation parameters']['number_of_ground_motion_fields'] = configParser.get('General', 'number_of_ground_motion_fields')

    riskConfig['Vulnerability'] = {}
    riskConfig['Vulnerability']['taxonomy_mapping_csv'] = taxoMapDict.get(retro)
    riskConfig['Vulnerability']['structural_vulnerability_file'] = configParser.get('File Paths', 'structural_vulnerability_file')
    riskConfig['Vulnerability']['nonstructural_vulnerability_file'] = configParser.get('File Paths', 'nonstructural_vulnerability_file')
    riskConfig['Vulnerability']['contents_vulnerability_file'] = configParser.get('File Paths', 'contents_vulnerability_file')
    riskConfig['Vulnerability']['occupants_vulnerability_file'] = configParser.get('File Paths', 'occupants_vulnerability_file')

    with open('initializations/s_Risk_%s_%s_%s_%s.ini' %(runID, runName, retro, expoSuffix), 'w') as configfile:
        configfile.write('# Generated automatically with manyFaults.py on: '+ str(datetime.now())+'\n')
        riskConfig.write(configfile)
    return

def get_config_params(args):
    """
    Parse Input/Output columns from supplied *.ini file
    """
    configParser = configparser.ConfigParser()
    configParser.read("manyFaults.ini")  #args.manyFaultsINI)
    return configParser

def parse_args():
    ### THIS SCRIPT NO LONGER HANDLES INI FILES NAMED ANYTHING OTHER THAN manyFaults.ini  
    parser = argparse.ArgumentParser(description="Create NRML ruputure file and all calibration files required to begin Open Quake model run")
    parser.add_argument("--manyFaultsINI",
                        type = str,
                        default = "manyFaults.ini",
                        help = "Full or relative filepath of initialization file. i.e --manyFaultsINI=C:\Python_Scripts\Many_Faults.ini")
    args = parser.parse_args()
    return args

def updateProgressBar(progress, totalProgress):
    unitColor = "\037[5;36m\033[5;47m"
    endColor = "\037[0;0m\037[0;0m"
    incre = int(50.0 / totalProgress * progress)
    if i != count -1:
        sys.stdout.write("\r" + "|%s%s%s%s| %d%%" % (unitColor, "\033[7m" + " "*incre + " \033[27m", endColor, " "*(50-incre), 2*incre))
    else:
        sys.stdout.write("\r" + "|%s%s%s| %d%%" % (unitColor, "\033[7m" + " "*20 + "COMPLETE!" + " "*21 + " \033[27m", endColor, 100))
    sys.stdout.flush()
    sys.stdout.write("\n")


#Classes

if __name__ == "__main__":
    main() 

