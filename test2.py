import pandas as pd
import matplotlib.pyplot as plt
data = pd.read_csv('data.csv')

#Takes only the time,magnometer X,Y,Z readings from the dataset:
#time = data.iloc[:,1].values
time = data["Time"].values
magn_x = data["MagX"].values
magn_y = data["MagY"].values
magn_z = data["MagZ"].values

def get_resultant(X, Y, Z):
    """This function gets the resultant magnitudes of three arrays of vector quantities: X, Y, and Z."""
    resultant = []
    for x, y, z in zip(X, Y, Z):
        resultant.append((x**2 + y**2 + z**2)**0.5)
    return resultant

print(time)
#plt.plot(time, get_resultant(magn_x, magn_y, magn_z))
#plt.show()