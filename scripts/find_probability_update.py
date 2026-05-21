#!/bin/python3
# Python script written by TEH on 17 June 2021 to calculate the annual probability of PGA = scenario PGA at Vancouver City Hall

import matplotlib.pyplot as plt
import pandas as pd

# Provincial Legislature in Victoria
lat = 48.419; lon = -123.371

# Grab scenario SA(0.3) values as close as possible to point
CSZ = 0.966037; CSZ_color='r' #XELF LARGE
BZM = 0.9548549999999999; BZM_color='k' #XELF MEDIUM
GS = 0.33276300000000003; GS_color='g' #XELF SMALL

# Create UHS from values in NRCan earthquake hazard web calculator, using 2020 values.
data = {'SA0p3': [1.24,1.13,0.992,0.851,0.727,0.608,0.506,0.407,0.304,0.238], 
       'POE': [2,2.5,3.5,5,7,10,14,20,30,40]}
UHS_orig = pd.DataFrame(data, columns=['POE', 'SA0p3']); UHS_orig.index = UHS_orig['SA0p3']; del UHS_orig['SA0p3']

data = {'SA0p3': [1.24,1.13,0.992,CSZ,BZM,0.851,0.727,0.608,0.506,0.407,GS,0.304,0.238], 
       'POE': [2,2.5,3.5,None,None,5,7,10,14,20,None,30,40],
       'Source': ['NRCan', 'NRCan', 'NRCan', 'XELF Large','XELF Medium', 'NRCan', 'NRCan', 'NRCan', 'NRCan', 'NRCan', 'XELF Small', 'NRCan', 'NRCan'],
       'c': ['b', 'b', 'b', CSZ_color, BZM_color, 'b', 'b', 'b', 'b', 'b', GS_color, 'b', 'b']}
UHS = pd.DataFrame(data, columns=['POE', 'SA0p3', 'Source', 'c']); UHS.index = UHS['SA0p3']; del UHS['SA0p3']

# Interpolate to get annual POE for scenario PGA's
UHS = UHS.interpolate(method='index')

# Plot results to check
plt.plot(UHS_orig.index, UHS_orig['POE'], color='b', label='NBCC2020')
plt.axvline(x = CSZ, color = CSZ_color, label = 'XELF Large')
plt.axvline(x = GS, color = GS_color, label = 'XELF Small')
plt.axvline(x = BZM, color = BZM_color, label = 'XELF Medium')
plt.scatter(UHS.index, UHS['POE'], c=UHS['c'], zorder=100)
for i, txt in enumerate(UHS_orig['POE']):
    plt.annotate("{:2.0f}%".format(txt), xy=(UHS_orig.index[i], UHS_orig['POE'][UHS_orig.index[i]]), xycoords='data', xytext=(2, 2.5), textcoords='offset points', c='b')

plt.annotate("{:2.0f}%".format(UHS['POE'][CSZ]), xy=(CSZ, UHS['POE'][CSZ]), xycoords='data', xytext=(1, 8.5), textcoords='offset points', c=CSZ_color)
plt.annotate("{:2.0f}%".format(UHS['POE'][GS]), xy=(GS, UHS['POE'][GS]), xycoords='data', xytext=(4, 0), textcoords='offset points', c=GS_color)
plt.annotate("{:2.0f}%".format(UHS['POE'][BZM]), xy=(BZM, UHS['POE'][BZM]), xycoords='data', xytext=(-20, -12), textcoords='offset points', c=BZM_color)
plt.legend()
plt.xlabel('SA(0.3) [%g]'); plt.ylabel('Probability of Exceedance [%/50 years]'); plt.title('Expected Hazard at BC Legislative Assembly')
plt.show()
