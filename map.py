from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.cm as cmx
import numpy as np
import pandas as pd
import reverse_geocode as rg

from handler import CoordinateHandler


class MapMaker:
    def __init__(self) -> None:

        self.data = pd.read_csv('data.csv')
        self.lat_data = np.array(self.data['Latitude'].values)
        self.long_data = np.array(self.data['Longitude'].values)
        self.alt_data = np.array(self.data['Altitude'].values)
        self.points_of_study = [3978, 4207, 4341, 4848, 5315, 5409]
        self.ip_lat_data = np.array(self.data.iloc[self.points_of_study]['Latitude'].values)
        self.ip_long_data = np.array(self.data.iloc[self.points_of_study]['Longitude'].values)

    def make_map_2d(self) -> None:

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
        plt.scatter(x, y, c=z, cmap="plasma", marker='o', s=0.1, label="ISS Orbit")
        plt.colorbar(fraction = 0.01175, label="Altitude / km", aspect=40)

        plt.scatter(x[0], y[0], color="#57b34f", marker=7, s=50, label="Start [hh:mm:ss]")
        plt.scatter(x[11796], y[11796], color="#d64747", marker=7, s=50, label="End [hh:mm:ss]")

        plt.scatter(self.ip_long_data, self.ip_lat_data, color="#d64747", marker="x", s=150, label = "Points of interest")
        plt.xlabel("Longitude", labelpad=20)
        plt.ylabel('Latitude', labelpad=25)
        plt.legend()
        plt.show()




if __name__ == '__main__':
    map_maker = MapMaker()
    ch = CoordinateHandler()
    map_maker.make_map_2d()
    print(ch.get_coords("interest-points"))
    print(ch.get_locations("interest-points"))