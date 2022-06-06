"""

Created by Mechabot team
This function offers to plot a worldmap with the path of the ISS alongside other given points

"""
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def dms2dd(arr):
    """
    This method returns an array with the Decimal Degree format
    of an array with points in Degree,Minutes,Seconds format. 

    Input Parameters:
    arr --> 1 Dimensional array with a list of location points in the DMS format

    Returned Parameters:
    result --> 1 Dimensional array with the points of arr in DD format 
    """
    result = []
    for i in arr:
        deg, minutes, seconds =  i.split(':')
        result.append((float(deg) + float(minutes)/60 + float(seconds)/(60*60)))
    return result

def plot(x=[],y=[],label=''):
    """
    This Method Plots the Path of the ISS alongside with indicating specific points on the map 
    of longitude x and latitude y parameters. If no paramters were passed theb only the ISS orbit
    will be plotted.
    This requires an active internet service to load the World map image on the background of the plot.

    Input Parameters:
    x --> 1D array with the Longitude location of the points which will be indicated on map.
    y --> 1D array with the Latitude location of the points which will be indicated on map.
    label --> String storing the label that will be added on the map's legend for the points to be plotted.
    """


    '''Importing the cs file'''
    data=pd.read_csv('data.csv')

    '''Getting the Latitude and longitude data of our flight in DMS format'''
    lat_dms = data.iloc[:,2].values 
    long_dms = data.iloc[:,3].values

    '''Changing the format from DMS to DD for plotting on the map'''
    long_dd = dms2dd(long_dms) 
    lat_dd = dms2dd(lat_dms)

    '''Preparing the grid for the map plot'''
    m = Basemap(projection='mill',
               llcrnrlat = -90,
               urcrnrlat = 90,
               llcrnrlon = -180,
               urcrnrlon = 180,
               resolution = 'c',
               epsg = 4269)

    m.drawcoastlines()

    '''Plotting our path of the ISS orbit'''
    m.plot(long_dd[0:2562],lat_dd[0:2562],color='yellow', latlon = True,label='ISS orbit')
    m.plot(long_dd[2562:5019],lat_dd[2562:5019],color='yellow', latlon = True)
    m.plot(long_dd[5019:],lat_dd[5019:],color='yellow', latlon = True)

    '''Adding specific points on the map if parameter x,y were passed'''
    m.scatter(x,y,color='red',s=60, latlon = True,marker='x',label=label)

    '''Adds the grid for the plot'''
    m.drawparallels(np.arange(-90,90,10),labels=[True,False,False,False])
    m.drawmeridians(np.arange(-180,180,30),labels=[0,0,0,1])

    '''Loads the map background image from the online server''' 
    m.arcgisimage(service='ESRI_Imagery_World_2D', xpixels = 2000, verbose= True)

    '''Adds a title for the plot'''
    plt.title(' Experiment runtime ISS orbit', fontsize=20)

    '''Adds a legend for the plot'''
    plt.legend()

    plt.show()


'''If this module is ran separately it will plot the path of the ISS'''
if __name__ == '__main__':
    plot()
