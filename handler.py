import PIL.Image
import PIL.ExifTags
import re
import os
from geopy.geocoders import Nominatim


class CoordinateHandler:
    def get_images(self, directory: str) -> list:
        d = directory
        paths = []
        for path in os.listdir(d):
            full_path = os.path.abspath(os.path.join(d, path))
            if os.path.isfile(full_path):
                paths.append(full_path)
        return paths

    def get_coords(self, directory: str) -> list:
        """Get coordinates of images in given directory.

        Args:
            directory: str = Name of directory in which images are saved.

        Returns:
            list = Coordinates of images in given directory.
        """

        coords_list = []

        # For each image in given directory:
        for path in self.get_images(directory):
            img = PIL.Image.open(path)

            # Extract all EXIF tags from image.
            exif = {
                PIL.ExifTags.TAGS[k]: v
                for k, v in img._getexif().items()
                if k in PIL.ExifTags.TAGS
            }

            # Fetch GPS info from EXIF tags.
            lat_ref = exif["GPSInfo"][1]
            lat = exif["GPSInfo"][2]
            long_ref = exif["GPSInfo"][3]
            long = exif["GPSInfo"][4]

            # Piece together GPS info to form coordinates in DMS format
            lat_dms = f'''{lat[0]}°{lat[1]}'{lat[2]}"{lat_ref}'''
            long_dms = f'''{long[0]}°{long[1]}'{long[2]}"{long_ref}'''

            # Convert coordinates from DMS format to DD format.
            deg, minutes, seconds, direction = re.split('[°\'"]', lat_dms)
            lat_dd = (
                float(deg) + float(minutes) / 60 + float(seconds) / (60 * 60)
            ) * (-1 if direction in ['W', 'S'] else 1)
            deg, minutes, seconds, direction = re.split('[°\'"]', long_dms)
            long_dd = (
                float(deg) + float(minutes) / 60 + float(seconds) / (60 * 60)
            ) * (-1 if direction in ['W', 'S'] else 1)

            coords_list.append((lat_dd, long_dd))

        # Return all coordinates.
        return coords_list

    def get_locations(self, directory: str) -> list:
        """Get locations of images in given directory.

        Args:
            directory: str = Name of directory in which images are saved.

        Returns:
            list = Locations of images in given directory.
        """

        # Create geolocator object.
        geolocator = Nominatim(user_agent="GoogleV3")

        # Fetch coordinates of images.
        coords = self.get_coords(directory)

        locations = []

        # For each coordinate in given coordinates:
        for coordinate in coords:
            # Separately fetch latitude and longitude.
            lat, long = coordinate[0], coordinate[1]

            # Find address.
            location = geolocator.reverse(str(lat) + "," + str(long), language="en")
            location = location.address if location is not None else 'N/A'
            locations.append(location)

        # Return all addresses.
        return locations


class DataHandler:
    """Class used to handle reading image data and writing NDVI data.
    """
    def __init__(self) -> None:
        self.xla_headers = [
            "ImgID",
            "NDVI"
        ]
        self.xla_csv_record_id = 0

    def get_image_ids(self, directory: str) -> list:
        """Find image ids of images in given directory.

        Args:
            directory: str = Name of directory in which images are saved.

        Returns:
            list = list of image ids.
        """

        d = directory
        ids = []

        # For each file in the directory:
        for path in os.listdir(d):
            # Find the id from the filename.
            id = path[6:10]
            ids.append(id)

        # Return all ids.
        return ids

    def get_data_dicts(self, ids: list, ndvis: list) -> list:
        """Get all records.

        Args:
            ids: list = List of all image ids of images.
            ndvis: list = List of all NDVIs of corresponding images.

        Returns:
            list: list of dictionaries of each record.
        """

        datas = []

        # For each image id:
        for i, id in enumerate(ids):
            # Form data dictionary,
            # consisting of Image ID and corresponding NDVI of image.
            data = {"ImgID": id, "NDVI": ndvis[i]}
            datas.append(data)

        # Return list of all dictionaries.
        return datas

    def setup_xla_csv(self) -> None:
        """Create NDVI specific CSV file and write column headers to it.
        """

        # Create empty CSV file for NDVI Logging.
        with open("xla.csv", 'w') as file:
            # Write column headers into the file.
            header = ','.join(column for column in self.xla_headers) + '\n'
            file.write(header)

    def log_xla_csv(self, data: dict) -> None:
        """Log a record into the XLA CSV file.

        Args:
            data: dict = Dictionary including record data.
        """
        record = ""

        # Append each value in the data dictionary
        # to the record, separated by commas.
        for key in self.xla_headers:
            record += str(data[key])
            record += ','
        # Remove last comma and moves to next line to mark
        # the end of a record and the start of a new one.
        record = record[:-1] + '\n'

        # Open CSV file.
        with open("xla.csv", 'a') as file:
            # Append record into file.
            file.write(record)

        self.xla_csv_record_id += 1
