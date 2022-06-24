import numpy as np


class IMU():
    """Class that handles IMU data processing.
    """
    def get_resultant(self, X: np.ndarray, Y: np.ndarray, Z: np.ndarray) -> np.ndarray:
        """Get the resultant magnitudes of three arrays of vector quantities: X, Y, and Z.

        Args:
            X: np.ndarray = X components of array of vector quantity.
            Y: np.ndarray = Y components of array of vector quantity.
            Z: np.ndarray = Z components of array of vector quantity.

        Returns:
            np.ndarray = Resultant magnitude of array of three vectors.
        """

        resultant = np.sqrt(np.square(X) + np.square(Y) + np.square(Z))
        return resultant

    def get_mean(self, arr: np.ndarray) -> float:
        """Calculate the mean of values in an array using numpy's mean funtion.

        Args:
            arr: np.ndarray = Given array.

        Returns:
            float: Mean of values in given array.
        """

        return np.mean(arr)

    def get_sd(self, arr: np.ndarray) -> float:
        """Calculate the standard deviation of values in an array using numpy's std funtion.

        Args:
            arr: np.ndarray = Given array.

        Returns:
            float: Standard deviation of values in given array.
        """

        return np.std(arr)

    def get_magn_history(self, magn_resultant: np.ndarray, decay: float = 0.0005) -> list:
        """Get simulated magnetometer readings in the past

        Args:
            magn_resultant: np.ndarray = Given array of resultant magnetic intensity values.

        Returns:
            list: List of arrays of resultant magnetic intensity values
        for each year in the past 5 years.
        """

        history_magn = []
        for i in magn_resultant:
            arr = [i]
            for j in range(5):
                arr.append(arr[j] + arr[j] * decay)

            history_magn.append(np.flip(arr))
        return history_magn

    def correlate(self, y: np.ndarray, z: np.ndarray) -> list:
        """This function numpy's corrcoef function to find
        the correlation coefficients between two arrays.

        Args:
            y: np.ndarray = First array.
            z: np.ndarray = Seconds array.

        Returns:
            list: List of correlation coefficients.
        """

        lags = range(-len(y) + 1, len(z))
        correlation = []
        for lag in lags:
            idx_lower_a1 = max(lag, 0)
            idx_lower_a2 = max(-lag, 0)
            idx_upper_a1 = min(len(y), len(y) + lag)
            idx_upper_a2 = min(len(z), len(z) - lag)
            b1 = y[idx_lower_a1:idx_upper_a1]
            b2 = z[idx_lower_a2:idx_upper_a2]
            c = np.correlate(b1, b2)[0]
            c = c / np.sqrt((b1**2).sum() * (b2**2).sum())
            correlation.append(c)
        return correlation[::2]
