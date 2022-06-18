import requests
import pandas as pd
from geopy.geocoders import Nominatim

data = pd.read_csv('data.csv')
points_of_study = [3978, 4207, 4341, 4848, 5315, 5409]

record_id = data["RecordID"]
time = data["Time"].values

lat_dd = list(data.iloc[points_of_study]['Latitude'].values)
long_dd = list(data.iloc[points_of_study]['Longitude'].values)

def make_poly(lat, long):
    magnitude = 1
    plat = lat + magnitude
    nlat = lat - magnitude
    plon = long + magnitude
    nlon = long - magnitude
    geopoly = f"({plat}%2C+{plon})%2C+({nlat}%2C+{plon})%2C+({nlat}%2C+{nlon})%2C+({plat}%2C+{nlon})%2C+({plat}%2C+{plon})"
    return geopoly
def get_location(lat, long):
    geolocator = Nominatim(user_agent="GoogleV3")

    location = geolocator.reverse(str(lat)+","+str(long), language="en")
    location = location.address if location != None else 'N/A'
    location = location.split(',')[-1][1:]

    return location

for lat, long in zip(lat_dd, long_dd):
    gases = ['CO2', 'CH4']
    poly = make_poly(lat, long)
    location = get_location(lat, long)
    date = 2017
    #print(poly)
    print(location)
    for gas in gases:
        request = f"https://datasource.kapsarc.org/api/records/1.0/search/?dataset=cait-historical-emissions-data&q=&rows=1&refine.gases_name={gas}&refine.location_name={location}&refine.date={date}&geofilter.polygon={poly}"
        #print(request)
        r = requests.get(request).json()
        print(r["records"][0]["fields"]["gases_full_form"])
        print(r["records"][0]["fields"]["value"])

#f"https://datasource.kapsarc.org/api/records/1.0/search/?dataset=cait-historical-emissions-data&q=&rows=5&refine.gases_name=CO2&refine.location_name=Pakistan&refine.date={date}&geofilter.polygon={poly}"