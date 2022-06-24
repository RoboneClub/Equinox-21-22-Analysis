import time
from datetime import datetime, timedelta

import numpy as np
import pyowm
import requests
from geopy.geocoders import Nominatim

owm_api_key = 'd9ee4bf970435c859be838ab8b771a9d'
wwo_api_key = '03a6af5d265d4698b76151330221606'


class WorldWeatherOnline:
    """Class responsible for handling requesting and downloading weather data,
    as well as dividing said data into useful sections.
    """
    def __init__(self) -> None:
        self.url = "https://api.worldweatheronline.com/premium/v1/past-weather.ashx?"
        self.key = wwo_api_key

    def get_weather_data_history(
        self, lat_dd: np.ndarray, long_dd: np.ndarray, dates: np.ndarray
    ) -> list:
        """Gather weather data for the corresponding latitude, longitude, and date,
        for the past 5 years.

        Args:
            lat_dd: np.ndarray = Array of latitudes.
            long_dd: np.ndarray = Array of longitudes.
            dates: np.ndarray = Array of dates.

        Returns:
            list = Weather data for each location for the last 5 years.
        """

        weather_data = []
        length = len(lat_dd)
        counter = 0
        for lat_dd, long_dd, dates in zip(lat_dd, long_dd, dates):
            this_location_weather = []
            # Collect the weather data for this location for the last 5 years.
            for i in range(6):
                d = (
                    datetime.strptime(dates, '%d-%m-%y') - timedelta(365 * i)
                ).strftime("%d-%m-%Y")
                try:
                    print("Trying to fetch response.....")
                    response = requests.get(
                        f"{self.url}key={self.key}&q={lat_dd},{long_dd}&date={d}&format=json"
                    )
                    this_location_weather.append(response.json()['data'])
                    print(f"Fetched weather history data for {lat_dd},{long_dd} on {d}")
                except Exception as err:
                    print(err)
                    print(f"Failed to retrive data for {lat_dd},{long_dd} on {d}")
                    this_location_weather.append("Failed to retrieve")
            counter += 1
            print(f"API Fetching Progress {counter*100/length}%")
            weather_data.append(this_location_weather)
        return weather_data

    def get_weather_data_single(
        self, lat_dd: np.ndarray, long_dd: np.ndarray, dates: np.ndarray
    ) -> list:
        """Gather weather data for the corresponding latitude, longitude, and date.

        Args:
            lat_dd: np.ndarray = Array of latitudes.
            long_dd: np.ndarray = Array of longitudes.
            dates: np.ndarray = Array of dates.

        Returns:
            list = Weather data for each location.
        """

        weather_data = []
        length = len(lat_dd)
        counter = 0
        for lat_dd, long_dd, dates in zip(lat_dd, long_dd, dates):
            this_location_weather = []
            # Collect the weather data for this location.
            for i in range(1):
                d = (
                    datetime.strptime(dates, '%d-%m-%y') - timedelta(365 * i)
                ).strftime("%d-%m-%Y")
                try:
                    print("Trying to fetch response.....")
                    response = requests.get(
                        f"{self.url}key={self.key}&q={lat_dd},{long_dd}&date={d}&format=json"
                    )
                    this_location_weather.append(response.json()['data'])
                    print(f"Fetched weather history data for {lat_dd},{long_dd} on {d}")
                except Exception as err:
                    print(err)
                    print(f"Failed to retrive data for {lat_dd},{long_dd} on {d}")
                    this_location_weather.append("Failed to retrieve")
            counter += 1
            print(f"API Fetching Progress {counter*100/length}%")
            weather_data.append(this_location_weather)
        return weather_data

    def get_avg_temp(self, data: list) -> list:
        """Get the average temperatures for each point in the fetched data

        Args:
            data: list = Weather data.

        Returns:
            list: Average temperature data for each location for the last 5 years.
        """

        temp_history = []
        for point in data:
            this_point_temp = []
            for year_reading in point:
                this_point_temp.append(int(year_reading['weather'][0]['avgtempC']))
            temp_history.append(np.flip(this_point_temp))
        return temp_history

    def get_avg_temp_single(self, data: list) -> list:
        """Get the average temperatures for each point in the fetched data

        Args:
            data: list = Weather data.

        Returns:
            list: Average temperature data for each location.
        """

        temp_history = []
        for point in data:
            this_point_temp = []
            if 'error' in point[0]:
                temp_history.append([np.NaN])
            else:
                for year_reading in point:
                    this_point_temp.append(float(year_reading['weather'][0]['avgtempC']))
                temp_history.append(np.flip(this_point_temp))
        return temp_history

    def get_uv_index(self, data: list) -> list:
        """Get the average UV Index for each point in the fetched data

        Args:
            data: list = Weather data.

        Returns:
            list: Average UV Index data for each location for the last 5 years.
        """

        uv_index_history = []
        for point in data:
            this_point_uv_index = []
            for year_reading in point:
                this_point_uv_index.append(int(year_reading['weather'][0]['uvIndex']))
            uv_index_history.append(np.flip(this_point_uv_index))
        return uv_index_history

    def get_uv_index_single(self, data: list) -> list:
        """Get the average UV Index for each point in the fetched data

        Args:
            data: list = Weather data.

        Returns:
            list: Average UV Index data for each location.
        """

        uv_index_history = []
        for point in data:
            this_point_uv_index = []
            if 'error' in point[0]:
                uv_index_history.append([np.NaN])
            else:
                for year_reading in point:
                    this_point_uv_index.append(float(year_reading['weather'][0]['uvIndex']))
                uv_index_history.append(np.flip(this_point_uv_index))
        return uv_index_history

    def get_avg_precipitation(self, data: list) -> list:
        """Get the average precipitation for each point in the fetched data

        Args:
            data: list = Weather data.

        Returns:
            list: Average preicipitation data for each location for the last 5 years.
        """

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

    def get_avg_precipitation_single(self, data: list) -> list:
        """Get the average precipitation for each point in the fetched data

        Args:
            data: list = Weather data.

        Returns:
            list: Average precipitation data for each location.
        """

        precip_history = []
        for point in data:
            this_point_precip = []
            if 'error' in point[0]:
                precip_history.append([np.NaN])
            else:
                for year_reading in point:
                    hourly = []
                    for hour in year_reading['weather'][0]['hourly']:
                        hourly.append(float(hour['precipMM']))
                    this_point_precip.append(float(np.average(hourly)))
                precip_history.append(np.flip(this_point_precip))
        return precip_history

    def get_avg_wind_speed(self, data: list) -> list:
        """Get the average wind speed for each point in the fetched data

        Args:
            data: list = Weather data.

        Returns:
            list: Average wind speed data for each location for the last 5 years.
        """

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

    def get_avg_wind_speed_single(self, data: list) -> list:
        """Get the average wind speed for each point in the fetched data

        Args:
            data: list = Weather data.

        Returns:
            list: Average wind speed data for each location.
        """

        wind_speed_history = []
        for point in data:
            this_point_wind_speed = []
            if 'error' in point[0]:
                wind_speed_history.append([np.NaN])
            else:
                for year_reading in point:
                    hourly = []
                    for hour in year_reading['weather'][0]['hourly']:
                        hourly.append(float(hour['windspeedKmph']))
                    this_point_wind_speed.append(float(np.average(hourly)))
                wind_speed_history.append(np.flip(this_point_wind_speed))
        return wind_speed_history

    def get_avg_humidity(self, data: list) -> list:
        """Get the average humidity for each point in the fetched data

        Args:
            data: list = Weather data.

        Returns:
            list: Average humidity data for each location for the last 5 years.
        """

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

    def get_avg_humidity_single(self, data: list) -> list:
        """Get the average humidity for each point in the fetched data

        Args:
            data: list = Weather data.

        Returns:
            list: Average humidity data for each location.
        """
        humidity_history = []
        for point in data:
            this_point_humidity = []
            if 'error' in point[0]:
                humidity_history.append([np.NaN])
            else:
                for year_reading in point:
                    hourly = []
                    for hour in year_reading['weather'][0]['hourly']:
                        hourly.append(float(hour['humidity']))
                    this_point_humidity.append(float(np.average(hourly)))
                humidity_history.append(np.flip(this_point_humidity))
        return humidity_history


class OpenWeatherMap:
    """Class responsible for handling requesting and downloading NDVI data and fetching Mean NDVI.
    """
    def __init__(self) -> None:
        self.api_key = owm_api_key
        self.url = "https://api.agromonitoring.com/agro/1.0/ndvi/history?polyid"
        self.mgr = pyowm.OWM(self.api_key).agro_manager()

    def get_polys(self) -> list:
        """Get polygons for each study point.

        Returns:
            list = List of polygon ids for each study point.
        """

        polys = []
        for polygon in self.mgr.get_polygons():
            polys.append(polygon.id)

        return polys

    def get_dates(self, date: str) -> list:
        """Get the date of the experiment for the past 5 years.

        Args:
            date: str = Date of the experiment.

        Returns:
            list = List of dates.
        """

        ds = []
        for i in range(1, 6):
            ds.append(
                (datetime.strptime(date, '%d-%m-%y') - timedelta(365 * i)).strftime("%d-%m-%Y")
            )
        return ds

    def get_date_range(self, date: str) -> tuple:
        """Get range of dates to search for NDVI readings.

        Args:
            date: str = Given date.

        Returns:
            tuple:
                d: int = Given date in unix format.
                start: int = Start date in unix format.
                end: int = End date in unix format.
        """

        # 120 Days delta time in seconds
        delta = 10368000

        # Convert given date to unix format.
        d = int(time.mktime(datetime.strptime(date, "%d-%m-%Y").timetuple()))

        # Set start and end date to be before and after given date by 120 days.
        start = d - delta
        end = d + delta
        return d, start, end

    def get_ndvi_data(self, polys: str, dates: list) -> list:
        """Get NDVI data for give polygons and dates.

        Args:
            polys: str = Polygon ID.
            dates: list = List of given dates.

        Returns:
            list: NDVI data for give polygons and dates.
        """

        ndvi_data = []
        for poly in polys:
            this_poly_ndvi = []
            for date in dates:
                unixdate, start, end = self.get_date_range(date)

                # Search for NDVI data for a polygon during a given date range.
                request = f"{self.url}={poly}&start={start}&end={end}&appid={self.api_key}"
                responses = requests.get(request).json()
                dts = []
                for response in responses:
                    # If response is valid, append it's date to 'dts' list.
                    if "dt" in response:
                        dts.append(int(response["dt"]))
                try:
                    # Get the index of the response with the date from ('dts' list)
                    # closest to the give date.
                    ndvi_data_index = dts.index(min(dts, key=lambda x: abs(x - unixdate)))

                    # Append response with aforementioned index to data.
                    this_poly_ndvi.append(responses[ndvi_data_index]["data"])
                except Exception as err:
                    # If no responses are found, set value to 'np.NaN'.
                    print(err)
                    this_poly_ndvi.append(np.NaN)
            ndvi_data.append(this_poly_ndvi)
        return ndvi_data

    def get_mean_ndvi(self, data: list) -> list:
        """Get Mean NDVIs from NDVI data.

        Args:
            data: list = List of NDVI Data.

        Returns:
            list = List of Mean NDVIs.
        """
        mean_ndvi_history = []
        for point in data:
            this_point_mean = []
            for year_reading in point:
                try:
                    this_point_mean.append(float(year_reading["mean"]))
                except Exception as err:
                    print(err)
                    this_point_mean.append(np.NaN)
            mean_ndvi_history.append(np.flip(this_point_mean))
        return mean_ndvi_history


class ClimateAnalysisIndicatorsTool():
    """Class responsible for handling requesting and downloading
    Gas Emission data and fetching separate metrics.
    """
    def __init__(self) -> None:
        self.url = "https://datasource.kapsarc.org/api/records/1.0/search/?dataset=cait-historical-emissions-data&q=&rows=1&refine.gases_name"

    def get_location(self, lat: float, long: float) -> str:
        """Get address of location with given latitude and longitude.

        Args:
            lat: float = Latitude in DD format.
            long: float = Longitude in DD format.

        Returns:
            str = Address of location.
        """

        geolocator = Nominatim(user_agent="GoogleV3")

        location = geolocator.reverse(str(lat) + "," + str(long), language="en")
        location = location.address if location is not None else 'N/A'

        return location

    def make_poly(self, lat: float, long: float) -> str:
        """Make geopolygon string using given latitude and longitude.

        Args:
            lat: float = Given latitude.
            long: float = Given longitude.

        Returns:
            str = geopolygon string.
        """
        magnitude = 1
        plat = lat + magnitude
        nlat = lat - magnitude
        plon = long + magnitude
        nlon = long - magnitude
        geopoly = f"({plat}%2C+{plon})%2C+({nlat}%2C+{plon})%2C+({nlat}%2C+{nlon})%2C+({plat}%2C+{nlon})%2C+({plat}%2C+{plon})"
        return geopoly

    def get_gas_emission_data(self, lat_dd: list, long_dd: list, date: str) -> list:
        """Get gas emission data for each location for a given date.

        Args:
            lat_dd: list = List of latitudes.
            long_dd: list = List of longitudes.
            date: str = Given date.

        Returns:
            list: List of gas emission data.
        """
        this_location_gass_emissions = []

        for lat, long in zip(lat_dd, long_dd):
            # Specify gases.
            gases = ['CO2', 'CH4']

            # Select polygon.
            poly = self.make_poly(lat, long)

            # Specify location.
            location = self.get_location(lat, long).split(',')[-1][1:]
            this_gas_emissions = []
            for gas in gases:
                # Request data.
                request = f"{self.url}={gas}&refine.location_name={location}&refine.date={date}&geofilter.polygon={poly}"
                r = requests.get(request).json()

                # Single out gas emission count value.
                value = r["records"][0]["fields"]["value"]
                value = value if value >= 0 else np.NaN
                this_gas_emissions.append(value)
            this_location_gass_emissions.append(this_gas_emissions)
        return this_location_gass_emissions

    def get_co2(self, data: list) -> list:
        """Get CO2 Emission data from all gas emission data.

        Args:
            data: list = Gas emission data.

        Returns:
            list = CO2 Emission data.
        """

        co2_values = []
        for location in data:
            co2_values.append(location[0])
        return co2_values

    def get_ch4(self, data: list) -> list:
        """Get CH4 Emission data from all gas emission data.

        Args:
            data: list = Gas emission data.

        Returns:
            list = CH4 Emission data.
        """

        ch4_values = []
        for location in data:
            ch4_values.append(location[1])
        return ch4_values
