#### MUST BE IN THE MAPPING VENV TO ACCESS PYTHON 3.9:
####$ source mapping/bin/activate

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import geopandas as gpd
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon


#### Loop through all three scenarios
#scen='ACM6p1_XELFSmall_164'; NAME = 'XELF Small'
#scen='ACM6p1_XELFMedium_169'; NAME = 'XELF Medium'
scen='ACM6p1_XELFLarge_174'; NAME = 'XELF Large'

#### Import shakemaps and shapefiles
df = pd.read_csv('/Users/thobbs/Documents/GitHub/earthquake-scenarios/outputs/s_shakemap_'+scen+'_MMI.csv')
x = np.array(df['lon']); y = np.array(df['lat'])
cval = np.array(df['gmv_PGA']); lab = 'Peak Ground Acceleration [g]'
#cval = np.array(df['MMI_worden']); lab = 'Mercalli Intensity (MMI)'
#vma = 9; vmi = 0 #MMI
vma = 0.7; vmi = 0 #PGA
print('Max PGA is '+str(100*df['gmv_PGA'].max())+' g.')
print('Max MMI is '+str(df['MMI_worden'].max()))
#exit()


#### Setup map
fig = plt.figure()#figsize=(4.8, 5.5))
fnt = 12
#ax = fig.add_subplot(211)
#ax.set_title("(a) Scenario Shaking", horizontalalignment='left',x=0)
#m = Basemap(projection='lcc', resolution='h',
#            lon_0=-125.1, lat_0=49.8, lat_1=48.3, lat_2=52.8,
#            width=50e4, height=38e4)
#m.drawmapboundary(fill_color='powderblue')
#m.fillcontinents(color='gainsboro', lake_color='powderblue')
#m.drawcoastlines(color='gray', zorder=20)
#m.drawcountries(color='black', zorder=10)
#m.drawstates(color='gray')
##m.drawmapscale(-66.8,46.2,-71,48.25,100)
#m.drawparallels(np.arange(45,55,1),labels=[1,0,0,0], zorder=104)
#m.drawmeridians(np.arange(-130,-110,1),labels=[0,0,0,1], zorder=105)
#
#
##### Add hexgrid and fault plane data
#xpt,ypt = m(x,y)
#if scen == 'SIM9p0_CascadiaInterfaceBestFault_161':
#    m.hexbin(xpt,ypt,C=cval,gridsize=250,alpha=0.75, cmap='RdYlBu_r', vmax=9, vmin=0, zorder=60) 
#    #m.colorbar(location='right', label='Peak Ground Acceleration [%g]')
#    c2,a2 = (-128.06,48.84)
#    c1,a1 = (-125.565,46.298)
#    m.drawgreatcircle(c1,a1,c2,a2,linewidth=2,color='r', zorder=80)
#    plt.text(m(c2,a2)[0], m(c2,a2)[1], ' M9.0 Cascadia', fontsize=fnt, color='r', zorder=111)
#elif scen == 'ACM6p1_XELFSmall_164':
#    m.hexbin(xpt,ypt,C=cval,gridsize=130,alpha=0.75, reduce_C_function = max, cmap='RdYlBu_r', vmax=9, vmin=0, zorder=60) 
#    x2,y2 = (-123.4901775,48.57380057)
#    x1,y1 = (-123.3640631,48.51503619)
#    #m.drawgreatcircle(x1,y1,x2,y2) #,linewidth=2,color='g', zorder=111)
#    plt.text(m(x2,y2)[0],m(x2,y2)[1] , 'XELF Small', fontsize=fnt, color='g', zorder=111, ha='left', va='top')
#elif scen == 'IDM7p0_GalianoDeep_160':
#    m.hexbin(xpt,ypt,C=cval,gridsize=100,alpha=0.75, cmap='RdYlBu_r', vmax=9, vmin=0, zorder=60) 
#    eastlon = float(-123.3006)
#    eastlat = float(48.7889)
#    westlon = float(-123.68253)
#    westlat = float(49.06744)
#    m.drawgreatcircle(westlon, westlat, eastlon, eastlat, del_s=50, linewidth=2, color='k', zorder=111)
#    plt.text(m(eastlon,eastlat)[0],m(eastlon,eastlat)[1] , ' M7.0 Intraslab', fontsize=fnt, color='k', zorder=111, ha='left')

#m.colorbar(location='right', label=lab)

###### Add inset box
##################################################################
######    ~~~~~ WORKING HERE - get box to work and plot on top
##################################################################
#LLlon=-123.276; LLlat=49.198; URlon=-123.000; URlat=49.322
#ULx,ULy = m(LLlon,URlat); URx,URy = m(URlon,URlat); LLx,LLy = m(LLlon,LLlat); LRx,LRy = m(URlon,LLlat)
#m.drawgreatcircle(ULx,ULy,URx,URy,linewidth=2,color='k', zorder=80)
#m.drawgreatcircle(LLlon,URlat,URlon,URlat,linewidth=2,color='k', zorder=80)
#m.drawgreatcircle(URlon,URlat,URlon,LLlat,linewidth=2,color='k', zorder=80)
#m.drawgreatcircle(URlon,LLlat,LLlon,LLlat,linewidth=2,color='k', zorder=80)


#### Add Vancouver zoom-in
ax = fig.add_subplot() #(212)
ax.set_title(NAME, horizontalalignment='left',x=0)
m = Basemap(projection='lcc', resolution='f',
            lon_0=-123.4092, lat_0=48.5096, lat_1=48, lat_2=48.5, width=50000, height=50000)
m.drawmapboundary(fill_color='powderblue')
m.fillcontinents(color='gainsboro', lake_color='powderblue')
m.drawcoastlines(color='gray', zorder=20)
m.drawcountries(color='black', zorder=10)
m.drawcounties(color='gray')
m.drawrivers(color='powderblue')
m.drawparallels(np.arange(46,50,0.2),labels=[0,0,0,0], zorder=104) #make first 0 a 1 to get lats
m.drawmeridians(np.arange(-124,-122,0.2),labels=[0,0,0,1], zorder=105)


#### Add hexgrid data
xpt2,ypt2 = m(x,y)

if scen == 'ACM6p1_XELFLarge_174':
    m.hexbin(xpt2,ypt2,C=cval,gridsize=600,alpha=0.75, cmap='RdYlBu_r', vmax=vma, vmin=vmi, zorder=60) 
    lon = [-123.6710497, -123.6046536, -123.4863617, -123.4756772, -123.4688087, -123.3863859, -123.3673065, -122.7758468]
    lat = [48.65717731, 48.62588719, 48.57170185, 48.56635963, 48.56025424, 48.52591142, 48.5175165, 48.36869761]
    x1,y1 = m(lon, lat)
    m.plot(x1,y1,'-', markersize=0, linewidth=1, color='k', zorder=100)
elif scen == 'ACM6p1_XELFSmall_164':
    m.hexbin(xpt2,ypt2,C=cval,gridsize=600,alpha=0.75, cmap='RdYlBu_r', vmax=vma, vmin=vmi, zorder=60) 
    lat = [48.57380057, 48.56597804, 48.55910948, 48.54594473, 48.54174727, 48.51503619]
    lon = [-123.4901775, -123.475868, -123.4674731, -123.434275, -123.4228274, -123.3640631]
    x1,y1 = m(lon, lat)
    m.plot(x1,y1,'-', markersize=0, linewidth=1, color='k', zorder=100)
elif scen == 'ACM6p1_XELFMedium_169':
    m.hexbin(xpt2,ypt2,C=cval,gridsize=600,alpha=0.75, cmap='RdYlBu_r', vmax=vma, vmin=vmi, zorder=60) 
    lat = [48.65655872, 48.62604371, 48.57444562, 48.56612334, 48.55891071, 48.54282098, 48.51258338, 48.50537075, 48.35934873]
    lon = [-123.672158, -123.605025, -123.4923969, -123.4763071, -123.4668752, -123.4258187, -123.3584083, -123.3004298, -123.1299595]
    x1,y1 = m(lon, lat)
    m.plot(x1,y1,'-', markersize=0, linewidth=1, color='k', zorder=100)

m.colorbar(location='right', label=lab)

#### Show or Save
plt.tight_layout()
#plt.show()

plt.savefig('HazFig.pdf', format='pdf')

#################################################################
##### OLD
#################################################################


##Georgia Strait
#x1,y1 = (-123.2322753,49.25286459)
#x2,y2 = (-124.0096672,49.18159966)
#m.drawgreatcircle(x1,y1,x2,y2,linewidth=2,color='#A13502')
#plt.text(m(x2,y2)[0],m(x2,y2)[1] , 'M7.2 Georgia Strait', fontsize=fnt, color='#A13502', zorder=111, ha='right', va='top')
#
##Intraslab
#eastlon = float(-123.3006)
#eastlat = float(48.7889)
#westlon = float(-123.68253)
#westlat = float(49.06744)
#m.drawgreatcircle(westlon, westlat, eastlon, eastlat, del_s=50, linewidth=2, color='#064A60')
#plt.text(m(eastlon,eastlat)[0],m(eastlon,eastlat)[1] , ' M7.0 Intraslab', fontsize=fnt, color='#064A60', zorder=111, ha='left')
#


##### Add reference cities
#for po in ([-123.114, 49.261, 'Vancouver', 'k'],
#          [-122.3328, 47.6061, 'Seattle', 'k'],
#          [-123.3656, 48.4284, 'Victoria', 'k']):
#    x, y = m(po[0], po[1])
#    #plt.plot(x, y, 'o', color=po[3], markersize=6, marker="*", zorder=110)
#    if po[2] == ' Quebec City':
#        plt.text(x, y, po[2], fontsize=fnt, zorder=111, ha='right')
#    else:
#        plt.text(x, y, po[2], fontsize=fnt, zorder=111)