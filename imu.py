import numpy as np
import pandas as pd

class Imu():
    def get_resultant(self, x, y, z):
        """This function gets the absolute magnitudes of three arrays of vector quantities: x, y, and z."""
        if isinstance(x, pd.DataFrame):
            x = x.to_numpy()
            y = y.to_numpy()
            z = z.to_numpy()
        absolute = np.sqrt(np.square(x) + np.square(y) + np.square(z))
        return absolute

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
            for j in range(9):
                arr.append(arr[j] + arr[j]*decay)
            
            history_magn.append(np.flip(arr))
        return history_magn

    def cor(self, y,z):
        """This function numpy's correlate function to find correlations between two arrays"""
        return np.correlate(y,z,mode="full")

    def sumnomeq(self, y,k):
        """This function calculates the sum of all iterations of the nominaor in the autocorrelation formula"""
        nomeq = []
        end = len(y) - k
        mean = self.get_mean(y)
        for i in range(0,end):
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
        return autocorarr


    """def autocor(self, y):
        Autocorrelation of array y #Formula from: https://www.itl.nist.gov/div898/handbook/eda/section3/eda35c.htm
        autocorarr = []
        counter = 0
        denom = self.sumdenomeq(y)
        try:
            size=len(y[0])-1
        except:
            size=len(y)
        print(size)
        for i in range (len(y)-1): # IS THIS MEANT TO BE y[0]-original was "for i in range (len(y)-1):"
            autocorarr.append((self.sumnomeq(y,i)/denom))
            counter += 1
            print(f"Progress of calculating autocorrelation: {counter*100/len(y)}%")
        print(autocorarr)
        autocorarr = np.append(autocorarr, autocorarr[-1]) # IS THIS MEANT TO BE AUTOCORRARR OR AUTOCORARR
        return autocorarr"""

    
