import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from noise_filtering import NoiseFiltering
from imu import IMU

imu = IMU()
nf = NoiseFiltering()


data = pd.read_csv('data.csv')

record_id = data["RecordID"].values

gyroX = data["GyroX"].values
gyroY = data["GyroY"].values
gyroZ = data["GyroZ"].values

magnX = data["MagX"].values
magnY = data["MagY"].values
magnZ = data["MagZ"].values

accX = data["AccX"].values
accY = data["AccY"].values
accZ = data["AccZ"].values

magn_filtered_matrix = nf.noise_filter(
    magnX, magnY, magnZ,
    # Senstivity and Frequency are according to https://www.st.com/resource/en/datasheet/lsm9ds1.pdf
    # RMS Noise assumtion according to https://www.st.com/resource/en/datasheet/lis3mdl.pdf
    # which is a similar build
    sensitivity=0.043,
    frequency=20,
    rms=(3.2 * 10**-3)
)
acc_filtered_matrix = nf.noise_filter(
    accX, accY, accZ,
    # Senstivity and Frequency are according to https://www.st.com/resource/en/datasheet/lsm9ds1.pdf
    # RMS Noise assumtion according to https://www.st.com/resource/en/datasheet/lis3mdl.pdf
    # which is a similar build
    sensitivity=(0.000244 * 9.81),
    frequency=10,
    rms=(3.2 * 10**-3)
)

magnX_filtered = magn_filtered_matrix[:, 0]
magnY_filtered = magn_filtered_matrix[:, 1]
magnZ_filtered = magn_filtered_matrix[:, 2]

accX_filtered = acc_filtered_matrix[:, 0]
accY_filtered = acc_filtered_matrix[:, 1]
accZ_filtered = acc_filtered_matrix[:, 2]

magn_filtered_resultant = imu.get_resultant(magnX_filtered, magnY_filtered, magnZ_filtered)
acc_filtered_resultant = imu.get_resultant(accX_filtered, accY_filtered, accZ_filtered)


#magn_filtered_autocorrelation = imu.cor(magn_filtered_resultant, magn_filtered_resultant)
#magn_filtered_autocorrelation_model_2 = imu.cor(magn_filtered_resultant, magn_filtered_resultant)
#acc_filtered_autocorrelation = imu.autocor(acc_filtered_resultant)

print(imu.get_magn_history(magn_filtered_resultant[0:50]))

#magn_acc_filtered_cor = imu.cor(magn_filtered_resultant, acc_filtered_resultant)

# plt.title("Filtered Resultant Magnetic Intensity Auto-Correlation Model 1")
# plt.xlabel("Record ID")
# plt.ylabel("Autocorrelation Coefficient")
# plt.plot(record_id, magn_filtered_autocorrelation, label='Autocorrelation Coefficient')
# plt.xticks(np.arange(min(record_id), max(record_id) + 1, 500))
# plt.legend()
# plt.show()

# plt.title("Filtered Resultant Magnetic Intensity Auto-Correlation Model 2")
# plt.xlabel("Record ID")
# plt.ylabel("Autocorrelation Coefficient")
# plt.plot(magn_filtered_autocorrelation_model_2, label='Autocorrelation Coefficient')
# plt.xticks(np.arange(min(record_id), max(record_id) + 1, 500))
# plt.yticks(np.arange(.9, 1, 0.01))
# plt.legend()
# plt.show()



# plt.title("magn x acc cor")
# plt.xlabel("Record ID")
# plt.ylabel("Autocorrelation Coefficient")
# plt.plot(magn_acc_filtered_cor, label='Autocorrelation Coefficient')
# plt.xticks(np.arange(min(record_id), max(record_id) + 1, 500))
# plt.yticks(np.arange(.9, 1, 0.01))
# plt.legend()
# plt.show()
