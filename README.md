# Analysis Of Equinox AstroPi Data

This GitHub repository contains the code responsible for analysing and processing our data gathered on the International Space Station from the AstroPi competition. Our experiment was conducted on the 16th of April 2022.

![](Map.png)

Here is an image of the flight path that the ISS took while our experiment ran


# Our Main Research Topics
### Experiment 1: The Historical Comparison
* Exploring the historical comparison between NDVI and: magnetic intensity, climate and gas emissions
* Exploring the historical comparison between magnetic data and climate
### Experiment 2: Current Data Analysis
* Exploring the relation between NDVI and: the Earth’s magnetic intensity, weather
* Exploring the relation between Earth’s magnetic profile and the climate as well as its effect on Near Earth Object (NEO) behaviour in Low Earth Orbit (LEO)
* Exploring the reliability of on-board machine learning using the Coral Artificial Accelerator (AI XLA) for classification of images gathered during the experiment

# Code

**api.py**  
This file is used to handle all of requests and downloads for the APIs used in our experiment. We used it to obtain: weather data (temperature, uv index, precipitation, wind speed and humidity), NDVI data and gas emissions.

**experiment-1.py**  
This file contains the code used for fetching all of the data required from APIs, analysing data from the IMU, and plotting all of the graphs necessary for experiment 1.

**experiment-2.py**  
This file contains the code used for fetching all of the data required from APIs, analysing data from the IMU, and plotting all of the graphs necessary for experiment 2.
**gas_emission_table.py**  
This file contains the code necessary to gather the data necessary for plotting the gas emissions for the study points.

**handler.py**  
This file contains the code to handle different types of information and convert the data to the required format. The data that gets handled is: coordinates, location and writing ndvi data to a new csv file.

**imu.py**  
This file is responsible for processing all of the data gathered by the IMU

**map.py**  
This file is the code responsible for making the map of the path taken by the ISS during our experiment. It also contains the code to plot all the points on the map where the pictures were taken.

**ndviv2.py**  
This file contains the code responsible for calculating the average ndvi for each image.

**noise_filtering.py**  
This file contains the code required to remove all of the noise from the IMU readings, making it smoother.

# Results

### Experiment 1: 
![](plots/experiment%201.0/Magnetic%20Intensity%20History/NDVI/Magnetic%20Intensity%20-%20Mean%20NDVI%20-%20All%20Locations.png)
As we can see from this graph, the NDVI and magnetic intensity don’t correlate at all. Each location has a cluster of points, however, the clusters are all spread out. This is contrary to what we were expecting due to the fact that an increased magnetic field has been proven to assist and hasten germination and root growth thus increasing the NDVI.


![](plots/experiment%201.0/NDVI%20History/Climate/NDVI%20-%20UV%20Index%20-%20All%20Locations.png)
This graphs shows us that there is no visible correlation between the mean NDVI values and the UV Index. Points in each location are also not clustered and appear to be randomly scattered across the graph.

![](plots/experiment%201.0/Magnetic%20Intensity%20History/Climate/Magnetic%20Intensity%20-%20Temperature%20-%20All%20Locations.png)
The graph above shows a strong negative correlation between the average temperature of a location and its magnetic intensity. The data points are also clustered into their own respective cities. 

![](plots/experiment%201.0/NDVI%20History/Gas%20Emissions/Table.png)
As we can see from the table, there appears to be no correlation between the NDVI and the emmisions of carbon dioxide and methane. This contradicts our hypothesis. We believed that an increase in NDVI would result in an increase in the rate of photosynthesis in a specific location. This would then results in a reduction of the levels of carbon dioxide. Additionally, places with high NDVI are more likely to be cultivated lands or natural forests, jungles, plains, etc. This would mean a lower amount of industrialisation in that area and thus, lower carbon dioxide and methane emissions.

### Experiment 2:
![](plots/experiment%202.0/IMU%20Data/Noise%20Filtered/Correlations/Filtered%20Resultant%20Magnetic%20Intensity%20-%20Filtered%20Resultant%20Acceleration%20-%20Correlation.png)
This graph shows that there is an extremely high correlation coefficient between the magnetic intensity and the absolute acceleration of the ISS, the lowest point being approximately 0.94 and the mean being 0.956. These high values indicate that there is a strong relationship between the two.
