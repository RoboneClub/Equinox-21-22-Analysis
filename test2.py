import pandas as pd
import matplotlib.pyplot as plt
data = pd.read_csv('data.csv')

#Takes only the time,magnometer X,Y,Z readings from the dataset:
#time = data.iloc[:,1].values
time = data["Time"].values
magn_x = data["MagX"].values
magn_y = data["MagY"].values
magn_z = data["MagZ"].values


print(type(time))
print(time)