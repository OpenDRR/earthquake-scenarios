#!/bin/python3
# Python script written by TEH on 17 June 2021 to calculate the annual probability of PGA = scenario PGA at Vancouver City Hall

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from geopy.distance import geodesic
import requests
#from scipy.interpolate import interp1d
from scipy.optimize import curve_fit
from matplotlib.lines import Line2D

#############################################################

def find_closest_point(df, LL):
    """
    Finds the closest point in the DataFrame to the given latitude and longitude.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing 'lat' and 'lon' columns.
        LL (tuple): Latitude and longitude as (lat, lon).
    
    Returns:
        pd.Series: The row corresponding to the closest point.
    """
    
    # Compute distances using geopy's geodesic function
    distances = df.apply(lambda row: geodesic((row['lat'], row['lon']), LL).kilometers, axis=1)
    
    # Find the index of the minimum distance
    min_index = distances.idxmin()
    
    # Return the closest point (row)
    return df.loc[min_index]

# Example usage:
# LL = (45.50892574986321, -73.55433183238827)
# closest_point = find_closest_point(df, LL)
# print(closest_point)

def fetch_sa0p3_values(LL):
    """
    Fetches SA(0.3) values for different probabilities using the NRCan API.
    
    Parameters:
        LL (tuple): Latitude and longitude as (lat, lon).
    
    Returns:
        pd.DataFrame: DataFrame with POE values and corresponding SA(0.3) values.
    """
    url = "https://www.earthquakescanada.nrcan.gc.ca/api/canshm/graphql"
    poe_values = [2.0, 2.5, 3.5, 5.0, 7.0, 10.0, 14.0, 20.0, 30.0, 40.0]
    
    query = f"""
    query{{
      NBC2020(latitude: {LL[0]}, longitude: {LL[1]}){{
        XC: siteDesignationsXs(siteClass: C, poe50: {poe_values}){{
          sa0p3
        }}
      }}
    }}
    """
    
    response = requests.post(url, json={"query": query})
    if response.status_code == 200:
        data = response.json()
        sa0p3_values = [item['sa0p3'] for item in data['data']['NBC2020']['XC']]
        return pd.DataFrame({'POE': poe_values, 'SA0p3': sa0p3_values})
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

def extrapolate_poe(df):
    """
    Extrapolates the missing 'POE' value using a power-law function that 
    asymptotes to zero.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing 'POE' and 'SA0p3' columns.
    
    Returns:
        pd.DataFrame: DataFrame with missing 'POE' value filled.
    """
    
    # Extract known POE and SA0p3 values
    known_poe = df['POE'].dropna().values
    known_sa0p3 = df.index[df['POE'].notna()].values
    
    # Define a power-law function that approaches y = 0
    def power_law(x, a, b):
        return a * np.power(x, b)
    
    # Fit the power-law function to the known data
    params, _ = curve_fit(power_law, known_sa0p3, known_poe)
    
    # Apply extrapolation for missing POE
    missing_sa0p3 = df.index[df['POE'].isna()].values[0]
    df.loc[df['POE'].isna(), 'POE'] = power_law(missing_sa0p3, *params)
    
    return df


#############################################################

# City Hall or some other site of interest:
LL = (45.50892574986321, -73.55433183238827)

# Grab scenario SA(0.3) value as close as possible to point
closest_point = find_closest_point(df, LL)
SCEN = closest_point['gmv_SA(0.3)']

# Create UHS from values in NRCan earthquake hazard web calculator, using 2020 values and assuming site class C:
df_sa0p3 = fetch_sa0p3_values(LL)
df_sa0p3.index = df_sa0p3['SA0p3']; del df_sa0p3['SA0p3'] #reset index to SA0.3

# Add a row for the scenario level of shaking, sort the dataframe
df_sa0p3['Source'] = ['NRCan','NRCan','NRCan','NRCan','NRCan','NRCan','NRCan','NRCan','NRCan','NRCan']
df_sa0p3['c'] = ['b','b','b','b','b','b','b','b','b','b'] #colours
df_sa0p3.loc[SCEN] = [None]+['Scenario']+['k']; df_sa0p3.sort_index(ascending = False, inplace = True)

# Interpolate
df = df_sa0p3.copy()
extrapolate_poe(df)

# Plot results to check -- THIS ISNT ALL WORKING FOR SOME REASON
plt.figure()
plt.plot(df.index, df['POE'], color='b', label='Exponential Fit')
plt.axvline(x = SCEN, color = 'k', label = 'Scenario')
plt.scatter(df.index, df['POE'], c=df['c'], zorder=100)
# access legend objects automatically created from data
handles, labels = plt.gca().get_legend_handles_labels()
point = Line2D([0], [0], label='NBCC2020', marker='o', markersize=4, 
         markeredgecolor='b', markerfacecolor='b', linestyle='')
# add manual symbols to auto legend
handles.extend([point])
for i, txt in enumerate(df['POE']):
    plt.annotate("{:2.0f}%".format(txt), xy=(df.index[i], df['POE'][df.index[i]]), xycoords='data', xytext=(2, 2.5), textcoords='offset points', c='b')

plt.annotate("{:2.0f}%".format(df['POE'][SCEN]), xy=(SCEN, df['POE'][SCEN]), xycoords='data', xytext=(2, 2.5), textcoords='offset points', c='k')
plt.legend(handles=handles)
plt.xlabel('SA(0.3) [%g]'); plt.ylabel('Probability of Exceedance [%/50 years]'); #plt.title('Expected Hazard at '+LL) #this doesnt work yet
plt.show()


############## SCRAPS  ###############################################
# Interpolate to get annual POE for scenario 
#UHS = UHS.interpolate(method='index')


#def extrapolate_poe(df):
#    """
#    Extrapolates the missing 'POE' value using interpolation.
#    
#    Parameters:
#        df (pd.DataFrame): DataFrame containing 'POE' and 'SA0p3' columns.
#    
#    Returns:
#        pd.DataFrame: DataFrame with missing 'POE' value filled.
#    """
#    
#    # Extract known POE and SA0p3 values
#    known_poe = df['POE'].dropna().values
#    known_sa0p3 = np.log10(df.index[df['POE'].notna()].values) #LOG of SAs
#    
#    # Interpolation function
#    interp_func = interp1d(known_sa0p3, known_poe, kind='linear', fill_value='extrapolate')
#    
#    # Apply extrapolation for missing POE
#    # log of SA value
#    salog = np.log10(df.loc[df['POE'].isna()].index.values[0])
#    df.loc[df['POE'].isna(), 'POE'] = interp_func(salog)
#    
#    return df



