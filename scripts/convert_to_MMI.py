import pandas as pd
import numpy as np
import sys

#### Quick script to calculate MMI from PGA using Caprio et al 2015
#USAGE: python convert_to_MMI.py outputs/s_shakemap_IDM5p7_StevestonJdFAftershock_80.csv 

shakemap = 's_shakemap_ACM7p3_LeechRiverFullFault_107.csv' #sys.argv[1]
df = pd.read_csv(shakemap)
df['PGA_cms'] = df['gmv_PGA']*981
df['logPGA_cms'] = np.log10(df['PGA_cms'])
df['MMI'] = 0.0000

for i in df.index:
    if df.at[i, 'logPGA_cms'] <= 1.6:
        df.at[i, 'MMI'] = 2.270 + 1.647*(df.at[i, 'logPGA_cms']) - 0.6
    else:
        df.at[i, 'MMI'] = -1.361 + 3.822*(df.at[i, 'logPGA_cms']) - 0.6

df.to_csv(str(shakemap).split('.')[0]+'_MMI.csv', index=False)