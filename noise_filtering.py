import numpy as np

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