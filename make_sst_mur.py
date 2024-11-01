#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 15:25:48 2023

@author: user
"""
import datetime as dt
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import netCDF4
import pandas as pd
import numpy as np
from numpy import ma
import time
import os,imageio
import glob
import conda # added this 12/28/2023
conda_file_dir = conda.__file__
conda_dir = conda_file_dir.split('lib')[0]
proj_lib = os.path.join(os.path.join(conda_dir, 'share'), 'proj')
from mpl_toolkits.basemap import Basemap
from scipy.interpolate import griddata as gd
import warnings
warnings.filterwarnings("ignore") # JiM added Sep 2020 to supopress the "matplotlibDeprecationWarning"

#HARDCODES
sat_option='MUR'# 'MUR' for Ultra resolution on coastwatch site, 'MARACOOS' #or 'UDEL', the two options for imagery available in mid-2020
#datetime_wanted=dt.datetime(2023,12,14,0,0,0)
datetime_wanted=dt.datetime(2024,1,20,0,0,0)
#cont_lev=[7.,10.,.20]# min, max, and interval in either degC or degF of temp contours wanted
cont_lev=[15.,20., 25.]# min, max, and interval in either degC or degF of temp contours wanted
#gbox=[-70.75,-70.,41.7,42.15] # inside_CCBAY # uses the getgbox function to define lat/lon boundary
gbox=[-66.,-65.,35.,36.] # inside_CCBAY # uses the getgbox function to define lat/lon boundary
latsize=[gbox[2],gbox[3]]
lonsize=[gbox[0],gbox[1]]
tick_int=gbox[3]-gbox[2] # allow for 3-4 tick axis label intervals
if tick_int>=1:
    tick_int=int(tick_int/2.)   # make the tick_interval integer increments
if tick_int<1:
    tick_int=.5
fig,ax=plt.subplots()
m = Basemap(projection='merc',llcrnrlat=min(latsize),urcrnrlat=max(latsize),\
            llcrnrlon=min(lonsize),urcrnrlon=max(lonsize),resolution='f')
m.fillcontinents(color='gray')
dtw=datetime_wanted.strftime("%Y-%m-%dT%H:%M:00Z")
url1='http://coastwatch.pfeg.noaa.gov/erddap/griddap/jplMURSST41.csvp?analysed_sst%5B('+dtw+'):1:('+dtw+')%5D%5B('+str(gbox[2])+'):1:('+str(gbox[3])+')%5D%5B('+str(gbox[0])+'):1:('+str(gbox[1])+')%5D'
print('extracting ultra high resolution sst from coastwatch')
df=pd.read_csv(url1)
times=df['time (UTC)']
sst=df['analysed_sst (degree_C)'].values
lat=df['latitude (degrees_north)'].values
lon=df['longitude (degrees_east)'].values
xm,ym=m([gbox[0],gbox[1]],[gbox[2],gbox[3]])
[xx,yy]=m(lon,lat)
xi = np.linspace(xm[0], xm[1], 50)
yi = np.linspace(ym[0], ym[1], 50)
xi, yi = np.meshgrid(xi, yi)
zi=gd((xx,yy),sst,(xi,yi),method='linear')
cs=m.contourf(xi,yi,zi,cont_lev,cmap=plt.get_cmap('rainbow'),zorder=0)
cbar = m.colorbar(cs,location='right',pad="2%",size="5%")
#plt.clabel(dept_cs, inline = True, fontsize =12,fmt="%1.0f")

plt.suptitle('Daily Multi-scale Ultra-high Resolution (MUR) Ocobserved SST (degC)',fontsize='10')
plt.title(dtw)
plt.savefig('SST_observed_MUR_'+dtw+'.png')
ax.suptitle(dtw)

