import numpy as np

def noise_filtering(X,Y,Z,sensitivity,frequency,rms):
    matrix = np.transpose(np.array((X,Y,Z)))
    #Using the sensor data LSM9DS1
    cross_talk = [[1,sensitivity,sensitivity],
                  [sensitivity,1,sensitivity],
                 [sensitivity, sensitivity, 1]]

    cross_talk = np.linalg.inv(cross_talk) #Crosstalk --> inverse to divide the data on crosstalk
    noise_rms = rms * frequency**0.5
    noise = np.random.randn(len(X),1) * noise_rms
    """we remove the noise"""
    matrix = matrix - noise
    return matrix



if __name__ == '__main__':
    import pandas as pd
    import matplotlib.pyplot as plt
    data = pd.read_csv('data01.csv')
    time = data['Time']
    MagnX = data.iloc[:,10].values
    MagnY = data.iloc[:,11].values
    MagnZ = data.iloc[:,12].values
    sensitivity = 0.043 #Senstivity according to https://www.st.com/resource/en/datasheet/lsm9ds1.pdf 
    frequency = 20  #Frequency according to https://www.st.com/resource/en/datasheet/lsm9ds1.pdf
    rms = 3.2 * 10**-3 #RMS Noise assumtion according to https://www.st.com/resource/en/datasheet/lis3mdl.pdf which is a similar build
    Magn = noise_filtering(MagnX,MagnY,MagnZ,sensitivity,frequency,rms)
    """magnetometer x, y, and z readings with reduced noise"""
    plt.plot(Magn)
    plt.show()
