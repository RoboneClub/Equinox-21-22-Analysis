from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.cm as cmx
import numpy as np

import csv_handler


class MapMaker:
    def __init__(self) -> None:
        csvh = csv_handler.CsvHandler()
        self.data = csvh.get_records('data.csv')
        self.lat_data = np.array([float(data["Latitude"]) for data in self.data])
        self.long_data = np.array([float(data["Longitude"]) for data in self.data])
        self.alt_data = np.array([float(data["Altitude"]) for data in self.data])

    def make_map_2d(self):

        m = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,\
            llcrnrlon=-180,urcrnrlon=180,resolution='c')

        #m.etopo()
        m.shadedrelief()
        #m.bluemarble()

        parallels = np.arange(-90.,91,30.)
        meridians = np.arange(-180.,181.,30.)
        m.drawparallels(parallels, labels=[1,0,0,0])

        m.drawmeridians(meridians, labels=[0,0,0,1])

        plt.title("Equinox runtime ISS Orbit")

        x, y, z = self.long_data, self.lat_data, self.alt_data
        plt.scatter(x, y, c=z, cmap="YlOrBr", marker='o', s=0.5)

        plt.xlabel("Longitude", labelpad=20)
        plt.ylabel('Latitude', labelpad=25)
        plt.colorbar(fraction = 0.01175, label="Altitude / km", aspect=40)

        plt.show()




if __name__ == '__main__':
    map_maker = MapMaker()
    #map_maker.make_map_3d()
    map_maker.make_map_2d()