import pandas as pd
import numpy as np

#### Quick script to calculate MMI from PGA using Caprio et al 2015

df = pd.read_csv('s_shakemap_IDM5p7_CR2022Aftershock_35.csv')
df['PGA_cms'] = df['gmv_PGA']*981
df['logPGA_cms'] = np.log10(df['PGA_cms'])
df['MMI'] = 0.0000

for i in df.index:
    if df.at[i, 'logPGA_cms'] <= 1.6:
        df.at[i, 'MMI'] = 2.270 + 1.647*(df.at[i, 'logPGA_cms']) - 0.6
    else:
        df.at[i, 'MMI'] = -1.361 + 3.822*(df.at[i, 'logPGA_cms']) - 0.6