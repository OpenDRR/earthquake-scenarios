import pandas as pd
import numpy as np
import sys

#### Quick script to calculate MMI from PGA using Caprio et al 2015 and Worden et al., 2012
#USAGE: python convert_to_MMI.py outputs/s_shakemap_IDM5p7_StevestonJdFAftershock_80.csv 

## Specify filename and GMICE reference
shakemap = sys.argv[1]

## Load data
df = pd.read_csv(shakemap)
df['PGA_cms'] = df['gmv_PGA']*981
df['logPGA_cms'] = np.log10(df['PGA_cms'])
df['MMI_caprio'] = 0.0000
for i in df.index:
    if df.at[i, 'logPGA_cms'] <= 1.6:
        df.at[i, 'MMI_caprio'] = 2.270 + 1.647*(df.at[i, 'logPGA_cms']) - 0.6
    else:
        df.at[i, 'MMI_caprio'] = -1.361 + 3.822*(df.at[i, 'logPGA_cms']) - 0.6

df['MMI_worden'] = 0.0000
c1 = 1.78; c2 = 1.55; c3 = -1.6; c4 = 3.70; t1 = 1.57
for i in df.index:
    if df.at[i, 'logPGA_cms'] <= t1:
        df.at[i, 'MMI_worden'] = c1 + c2*(df.at[i, 'logPGA_cms']) - 0.6
    else:
        df.at[i, 'MMI_worden'] = c3 + c4*(df.at[i, 'logPGA_cms']) - 0.6

df.to_csv(str(shakemap).split('.')[0]+'_MMI.csv', index=False)