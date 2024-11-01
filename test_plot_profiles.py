#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 17:21:46 2024

@author: user
"""
mode='gif'
# loading coastlines & bathy lines
#coastfilename='c:/users/james.manning/Downloads/basemaps/capecod_coastline_detail.csv'
coastfilename='/user/sst/us_coast.dat'
dfc=pd.read_csv(coastfilename,delim_whitespace=True,names=['lon','lat'])
bathyfile='/user/sst/necs_60m.bty'
dfb=pd.read_csv(bathyfile,delim_whitespace=True,names=['lon','lat','d1','d2'])
dfb=dfb[dfb.lat!=0]
dfb['lon']=dfb['lon']*-1

dfs=df.drop_duplicates(subset='tow_id')# cast positions
stas=dfs.two_id.values
dts=dfs['time (UTC)']
#stas=stas[0:24]
count=0
for i in dts:
    if mode=='just_station_plot':
        fig, ax1 = plt.subplots(1, 1) 
    else:
        fig, (ax1, ax2) = plt.subplots(1, 2)
    #plot coast
    ax1.plot(dfc.lon,dfc.lat,'k.',markersize=1)
    ax1.plot(dfb.lon,dfb.lat,'g.',markersize=1)
    ax1.text(-71.,39.,'60m isobath',color='g')
    ax1.text(-71.,38.5,'200m isobath',color='purple')
    
    # plot stations
    ax1.plot(dfs.lon,dfs.lat,'r.',markersize=12)
    df1=df[df['time (UTC)']==i]
    ax1.plot(df1.lon[0],df1.lat[0],'k.',markersize=30)
    ax1.set_title('eMOLT realtime',fontsize=12)
    ax1.set_ylim(min(dfs.lat)-.1,max(dfs.lat)+.1)
    ax1.set_xlim(min(dfs.lon)-.1,max(dfs.lon)+.1)
    ax1.text(-71.,38.,df1.sta[0],color='k')
    ax1.text(-74.5,44.,str(i)[:-3])
    if mode=='just_station_plot':
        for j in range(len(dfs)):
            ax1.text(dfs.lon.values[j],dfs.lat.values[j],dfs.sta.values[j],color='k',verticalalignment='center',horizontalalignment='center',fontsize=6)
        break
    box = ax1.get_position()
    box.x0 = box.x0 - 0.05
    box.x1 = box.x1 - 0.05
    ax1.set_position(box)
    # plot profiles
    
    df1=df1[df1['depth']>2.0]
    #id=np.where(np.diff(df1['depth'])<0)
    id=np.where(df1['depth']==max(df1['depth']))[0][0]
    df1=df1[0:id]#downcast
    #ax2.plot(df1['temp'].values[id[0]],df1['depth'].values[id[0]]*-1.,'r-')
    ax2.plot(df1['temp'].values,df1['depth'].values*-1.,'r-')
    ax2.set_ylim(-100.,0)
    ax2.set_xlabel(df1['sta'].values[0]+' temp (degC)',color='r')
    ax2.set_ylabel('depth (meters)')
    
    
    ax3 = ax2.twiny()
    ax3.plot(df1['salt'].values,df1['depth'].values*-1.,'c-')
    ax3.set_xlim(31.,36.)
    ax3.set_title('salinity (PSU)',color='c')
    
    count=count+1
    #fig.savefig('plots/'+"{:03d}".format(count)+'.png')
    ib=str(i).replace(' ','_')
    ib=ib.replace(':','')
    fig.savefig('plots/'+ib+'.png')
    plt.close(fig)

if mode=='gif':
make_gif('c:/users/james.manning/Downloads/ctd/plots/HB2204.gif','c:/users/james.manning/Downloads/ctd/plots/',frame_length=2.0)
else:
fig.savefig('station_plot.png')
