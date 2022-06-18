import numpy as np
import pandas as pd

class Magn():
    def get_resultant(self, X, Y, Z):
        """This function gets the resultant magnitudes of three arrays of vector quantities: X, Y, and Z."""
        resultant = []
        for x, y, z in zip(X, Y, Z):
            resultant.append((x**2 + y**2 + z**2)**0.5)
        return resultant

    def get_mean_3(self, x, y, z):
        """This function calculates the mean of three values"""
        return (x+y+z)/3

    def get_mean(self, arr):
        """This function uses numpy's mean funtion to calculate the mean of values in an array"""
        return np.mean(arr)

    def get_sd(self, arr):
        """This function uses numpy's std funtion to calculate the standard deviation of values in an array"""
        return np.std(arr)

    def get_magn_history(self, magn_resultant, decay = 0.0005):
        """This function simulates Magnetometer readings in the past"""
        history_magn = []
        for i in magn_resultant:
            arr = [i]
            for j in range(5):
                arr.append(arr[j] + arr[j]*decay)

            history_magn.append(np.flip(arr))
        return history_magn

    def cor(self, y, z):
        """This function numpy's correlate function to find correlations between two arrays"""
        return np.correlate(y, z, mode="full")

    def sumnomeq(self, y, k):
        """This function calculates the sum of all iterations of the nominaor in the autocorrelation formula"""
        nomeq = []
        end = len(y) - k
        mean = self.get_mean(y)
        for i in range(0, end):
            nomeq.append((y[i] - mean) * ( y[i + k] - mean))
        return np.sum(nomeq)
    def sumdenomeq(self, y):
        """This function calculates the sum of all iterations of the denominaor in the autocorrelation formula"""
        denomeq = []
        mean = self.get_mean(y)
        end = len(y) - 1
        for i in range(0,end):
            denomeq.append((y[i] - mean)**2)
        return np.sum(denomeq)
    def autocor(self, y):
        """Autocorrelation of array y""" #Formula from: https://www.itl.nist.gov/div898/handbook/eda/section3/eda35c.htm
        autocorarr = []
        counter = 0
        denom = self.sumdenomeq(y)
        for i in range (len(y)-1):
            autocorarr.append((self.sumnomeq(y,i)/denom))
            counter += 1
            print(f"Progress of calculating autocorrelation: {counter*100/len(y)}%")
        autocorrarr = np.append(autocorrarr, autocorrarr[-1])
        return autocorarr

class NoiseFiltering():
    def noise_filter(self, X, Y, Z, sensitivity, frequency, rms):
        matrix = np.transpose(np.array((X, Y, Z)))
        #Using the sensor data LSM9DS1
        cross_talk = [
            [1, sensitivity, sensitivity],
            [sensitivity, 1, sensitivity],
            [sensitivity, sensitivity, 1]
        ]

        cross_talk = np.linalg.inv(cross_talk) #Crosstalk --> inverse to divide the data on crosstalk
        noise_rms = rms * frequency**0.5
        noise = np.random.randn(len(X),1) * noise_rms
        """we remove the noise"""
        matrix = matrix - noise
        return matrix



if __name__ == '__main__':

    import matplotlib.pyplot as plt

    magn = Magn()
    nf = NoiseFiltering()

    data = pd.read_csv('data.csv')
    """imports the data from the csv using pandas library"""
    """Takes only the time, magnetometer X, Y, and Z readings from the dataset:"""
    record_id = data.iloc[:,0].values
    time = data.iloc[:,2].values
    MagnX = data.iloc[:,12].values
    MagnY = data.iloc[:,13].values
    MagnZ = data.iloc[:,14].values
    plt.plot(record_id, MagnX, label='MagnX')
    plt.plot(record_id, MagnY, label='MagnY')
    plt.plot(record_id, MagnZ, label='MagnZ')
    """plots magnetometer X,Y, and Z readings"""
    plt.legend()
    plt.show()

    """calculates the resultant magnitude of the magnetic field"""
    Magn_resultant = magn.get_resultant(MagnX,MagnY,MagnZ)
    """calculates the mean of magnetometer readings"""
    Magn_mean = magn.get_mean(Magn_resultant)
    """calculates the standard deviation of magnetometer readings"""
    Magn_sd = magn.get_sd(Magn_resultant)

    autocorr_magn = magn.autocor(MagnX)#np.load("autocorrelation_magn.npy",allow_pickle=True)
    print(len(MagnX))
    print(len(autocorr_magn))
    # plt.plot(record_id, np.append(autocorr_magn, autocorr_magn[-1]), label='Autocorrelation')
    # plt.plot(record_id, MagnX, label='Magn')
    # plt.xlabel("record_id")
    # plt.legend()
    # plt.show()

    plt.plot(np.arange(0,len(MagnX),1),Magn_resultant,label='MagnResultant')
    plt.plot(np.arange(0,len(MagnX),1),[Magn_mean]*len(MagnX),label='Mean')
    plt.plot(np.arange(0,len(MagnX),1),[Magn_sd]*len(MagnX),label='Numpy Standard Deviation')
    """plots resultant magnetometer values, the mean, and the standard deviation"""
    plt.legend()
    plt.show()
    


    fig, (ax1, ax2) = plt.subplots(2, sharex=True)
    fig.suptitle('Magnetic Intensity - Autocorrelation')
    ax1.plot(record_id, MagnX)
    ax2.plot(record_id, autocorr_magn)
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()

    sensitivity = 0.043 #Senstivity according to https://www.st.com/resource/en/datasheet/lsm9ds1.pdf 
    frequency = 20  #Frequency according to https://www.st.com/resource/en/datasheet/lsm9ds1.pdf
    rms = 3.2 * 10**-3 #RMS Noise assumtion according to https://www.st.com/resource/en/datasheet/lis3mdl.pdf which is a similar build
    magn_nf = nf.noise_filter(MagnX,MagnY,MagnZ,sensitivity,frequency,rms)
    """magnetometer x, y, and z readings with reduced noise"""
    plt.plot(magn_nf)
    plt.show()