"""
Developed by: Team Equinox
Description: Revised code responsible for recalculating NDVI.

References:
- NumPy library: https://numpy.org/doc/stable/
- OpenCV library: https://docs.opencv.org/4.x/
"""


import numpy as np
import cv2

from handler import CoordinateHandler, DataHandler


class NDVI:
    """Class responsible for calculating NDVI and applyig NDVI color maps to images."""

    def apply_ndvi(self, path: str) -> np.ndarray:
        """Apply NDVI grayscale colormap to image at path.

        Args:
            path: str = Path of image to be color mapped.

        Returns:
            np.ndarray = Multi-channel array representing image.
        """

        # Register image on cv2 and call function to apply color map.
        img = cv2.imread(path)
        # Call the function to create the color mapped image, using the image as arguments
        return self.apply_color_map(img)

    def contrast_stretch(self, image: np.ndarray) -> np.ndarray:
        """Apply stretched contrast to image.

        Args:
            image: np.ndarray = Image to be contrasted.

        Returns:
            np.ndarray = Multi-channel array representing image.
        """

        in_min = np.percentile(image, 5)
        in_max = np.percentile(image, 95)

        out_min = 0.0
        out_max = 255.0

        out = image - in_min
        out *= ((out_min - out_max) / (in_min - in_max))
        out += in_min

        return out

    def calc_ndvi(self, image: np.ndarray) -> np.ndarray:
        """Calculate NDVI for each pixel and return value to array,
        making a grayscale NDVI color map.

        Args:
            image: np.ndarray = Image to be color mapped.

        Returns:
            np.ndarray = Multi-channel array representing image.
        """

        # Extract blue and red band values from image.
        blue, red = cv2.split(image)[0], cv2.split(image)[2]

        # Set the denomincator to the values of
        # the blue added to the red band of the image.
        bottom = (red.astype(float) + blue.astype(float))
        bottom[bottom == 0] = 0.01

        # Calculate the NDVI using the NDVI equation.
        ndvi = (blue.astype(float) - red) / bottom

        # Return array.
        return ndvi

    def apply_color_map(self, image: np.ndarray) -> np.ndarray:
        """Apply sequence of color maps to get
        NDVI grayscale color map as final result.

        Args:
            image: np.ndarray = Image to be color mapped.

        Returns:
            np.ndarray = Multi-channel array representing image.
        """

        # Call the function to apply the contrast.
        #contrasted = self.contrast_stretch(image)

        # Call the function to calculate NDVI.
        ndvi = self.calc_ndvi(image)

        # Calculate average NDVI value
        ndvi_value = np.average(ndvi)

        return ndvi_value


if __name__ == "__main__":
    ch = CoordinateHandler()
    dh = DataHandler()
    ndvi = NDVI()

    # Get NDVIs of all images.
    ndvis = []
    for path in ch.get_images("all-images"):
        ndvis.append(ndvi.apply_ndvi(path))

    # Get data dictionaries.
    datas = dh.get_data_dicts(dh.get_image_ids("all-images"), ndvis)

    # Save each record into XLA CSV file.
    dh.setup_xla_csv()
    for data in datas:
        dh.log_xla_csv(data)
