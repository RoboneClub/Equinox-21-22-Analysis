import time
from datetime import datetime, timedelta

import numpy
import numpy as np
import pandas
import pandas as pd
import pyowm
import requests
from geopy.geocoders import Nominatim
from pyowm.utils.geo import Polygon as GeoPolygon

owm_api_key = 'd9ee4bf970435c859be838ab8b771a9d'
wwo_api_key = '03a6af5d265d4698b76151330221606'

class WorldWeatherOnline:
    def __init__(self) -> None:
        self.url = "https://api.worldweatheronline.com/premium/v1/past-weather.ashx?"
        self.key = wwo_api_key

    def get_weather_data(self, lat_dd, long_dd, dates):
        """This function gathers weather data for the corresponding latitude, longitude, and date, for the past 10 years."""
        weather_data = []
        print(lat_dd)
        length = len(lat_dd)
        counter = 0
        for lat_dd, long_dd, dates in zip(lat_dd, long_dd, dates):
            this_location_weather = [] #collects the weather data for this location for last 5 years
            for i in range(6):
                d = (datetime.strptime(dates,'%d-%m-%y') - timedelta(365*i)).strftime("%d-%m-%Y") 
                try:
                    print("Trying to fetch response.....")
                    response = requests.get(f"{self.url}key={self.key}&q={lat_dd},{long_dd}&date={d}&format=json")
                    this_location_weather.append(response.json()['data'])
                    print(f"Fetched weather history data for {lat_dd},{long_dd} on {d}")
                except:
                    print(f"Failed to retrive data for {lat_dd},{long_dd} on {d}")
                    this_location_weather.append("Failed to retrieve")
            counter += 1
            print(f"API Fetching Progress {counter*100/length}%")
            weather_data.append(this_location_weather)
        return weather_data

    def get_avg_temp(self, data):
        """this function gets the average temperatures for each point in the fetched data"""
        temp_history = []
        for point in data:
            this_point_temp = []
            for year_reading in point:
                this_point_temp.append(int(year_reading['weather'][0]['avgtempC']))
            temp_history.append(np.flip(this_point_temp))
        return temp_history

    def get_uv_index(self, data):
        """this function gets the average uv index for each point in the fetched data"""
        uv_index_history = []
        for point in data:
            this_point_temp = []
            for year_reading in point:
                this_point_temp.append(int(year_reading['weather'][0]['uvIndex']))
            uv_index_history.append(np.flip(this_point_temp))
        return uv_index_history

    def get_avg_precipitation(self, data):
        """this function gets the average precipitation for each point in the fetched data"""
        precip_history = []
        for point in data:
            this_point_precip = []
            for year_reading in point:
                hourly = []
                for hour in year_reading['weather'][0]['hourly']:
                    hourly.append(float(hour['precipMM']))

                this_point_precip.append(float(np.average(hourly)))
            precip_history.append(np.flip(this_point_precip))
        return precip_history

    def get_avg_wind_speed(self, data):
        """this function gets the average wind speeds for each point in the fetched data"""
        wind_speed_history = []
        for point in data:
            this_point_wind_speed = []
            for year_reading in point:
                hourly = []
                for hour in year_reading['weather'][0]['hourly']:
                    hourly.append(float(hour['windspeedKmph']))

                this_point_wind_speed.append(float(np.average(hourly)))
            wind_speed_history.append(np.flip(this_point_wind_speed))
        return wind_speed_history

    def get_avg_humidity(self, data):
        """this function gets the average humidity for each point in the fetched data"""
        humidity_history = []
        for point in data:
            this_point_humidity = []
            for year_reading in point:
                hourly = []
                for hour in year_reading['weather'][0]['hourly']:
                    hourly.append(float(hour['humidity']))

                this_point_humidity.append(float(np.average(hourly)))
            humidity_history.append(np.flip(this_point_humidity))
        return humidity_history


class OpenWeatherMap:
    def __init__(self) -> None:
        self.api_key = owm_api_key
        self.url = 'https://api.agromonitoring.com/agro/1.0/ndvi/history?polyid'
        self.mgr = pyowm.OWM(self.api_key).agro_manager()

    def get_polys(self) -> list:
        polys = []
        for polygon in self.mgr.get_polygons():
            polys.append(polygon.id)

        return polys
    
    def get_dates(self, date):
        ds = []
        for i in range(1, 6):
            ds.append((datetime.strptime(date,'%d-%m-%y') - timedelta(365*i)).strftime("%d-%m-%Y"))
        return ds

    def get_date_range(self, date):
        # 120 Days delta time
        delta = 10368000
        d = int(time.mktime(datetime.strptime(date, "%d-%m-%Y").timetuple()))
        start = d - delta
        end = d + delta
        return d, start, end

    def get_ndvi_data(self, polys, dates):
        ndvi_data = []
        for poly in polys:
            this_poly_ndvi = []
            for date in dates:
                unixdate, start, end = self.get_date_range(date)
                request = f"{self.url}={poly}&start={start}&end={end}&appid={self.api_key}"
                responses = requests.get(request).json()
                #print(responses)
                #print(poly)
                #print(date)
                dts = []
                for response in responses:
                    if "dt" in response:
                        dts.append(int(response["dt"]))
                try:
                    ndvi_data_index = dts.index(min(dts, key=lambda x:abs(x-unixdate)))
                    this_poly_ndvi.append(responses[ndvi_data_index]["data"])
                except:
                    this_poly_ndvi.append(np.NaN)
            ndvi_data.append(this_poly_ndvi)
        return ndvi_data

    def get_mean_ndvi(self, data):
        mean_ndvi_history = []
        for point in data:
            this_point_mean = []
            for year_reading in point:
                try:
                    this_point_mean.append(float(year_reading["mean"]))
                except:
                    this_point_mean.append(np.NaN)
            mean_ndvi_history.append(np.flip(this_point_mean))
        return mean_ndvi_history

class ClimateAnalysisIndicatorsTool():
    def __init__(self) -> None:
        pass

    def get_location(self, lat, long):
        geolocator = Nominatim(user_agent="GoogleV3")

        location = geolocator.reverse(str(lat)+","+str(long), language="en")
        location = location.address if location != None else 'N/A'

        return location
    
    def make_poly(self, lat, long):
        magnitude = 1
        plat = lat + magnitude
        nlat = lat - magnitude
        plon = long + magnitude
        nlon = long - magnitude
        geopoly = f"({plat}%2C+{plon})%2C+({nlat}%2C+{plon})%2C+({nlat}%2C+{nlon})%2C+({plat}%2C+{nlon})%2C+({plat}%2C+{plon})"
        return geopoly
    
    def get_gas_emission_data(self, lat_dd, long_dd, date):
        this_location_gass_emissions = []
        for lat, long in zip(lat_dd, long_dd):
            gases = ['CO2', 'CH4']
            poly = self.make_poly(lat, long)
            location = self.get_location(lat, long).split(',')[-1][1:]
            this_gas_emissions = []
            for gas in gases:
                request = f"https://datasource.kapsarc.org/api/records/1.0/search/?dataset=cait-historical-emissions-data&q=&rows=1&refine.gases_name={gas}&refine.location_name={location}&refine.date={date}&geofilter.polygon={poly}"
                # print(request)
                r = requests.get(request).json()
                this_gas_emissions.append(r["records"][0]["fields"]["value"])
            this_location_gass_emissions.append(this_gas_emissions)
        return this_location_gass_emissions

    def get_co2(self, data):
        co2_values = []
        for location in data:
            co2_values.append(location[0])
        return co2_values
    
    def get_ch4(self, data):
        ch4_values = []
        for location in data:
            ch4_values.append(location[1])
        return ch4_values


if __name__ == "__main__":
    data = pd.read_csv('data.csv')
    date = data.iloc[3978]['Date']
    owm = OpenWeatherMap()
    polys = owm.get_polys()
    dates = owm.get_dates(date)
    owm.get_ndvi_data(polys, dates)
