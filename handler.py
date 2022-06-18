import csv
import PIL.Image
import PIL.ExifTags
from pathlib import Path
import re
import os
import reverse_geocode as rg


class CsvHandler:
    def get_records(self, filename: str) -> list:
        with open(filename, mode='r') as csvfile:
            dict_reader = csv.DictReader(csvfile)
            records = []
            for record in dict_reader:
                records.append(record)
        return records


class CoordinateHandler:
    def get_images(self, filename: str) -> list:
        d = filename
        paths = []
        for path in os.listdir(d):
            full_path = os.path.abspath(os.path.join(d, path))
            if os.path.isfile(full_path):
                paths.append(full_path)
        return paths

    def get_coords(self, filename: str) -> list:
        coords_list = []
        for path in self.get_images(filename):
            img = PIL.Image.open(path)
            exif = {
                PIL.ExifTags.TAGS[k]: v
                for k, v in img._getexif().items()
                if k in PIL.ExifTags.TAGS
            }
            lat_ref = exif["GPSInfo"][1]
            lat = exif["GPSInfo"][2]
            long_ref = exif["GPSInfo"][3]
            long = exif["GPSInfo"][4]
            lat_dms = f'''{lat[0]}°{lat[1]}'{lat[2]}"{lat_ref}'''
            long_dms = f'''{long[0]}°{long[1]}'{long[2]}"{long_ref}'''
            deg, minutes, seconds, direction =  re.split('[°\'"]', lat_dms)
            lat_dd = (float(deg) + float(minutes)/60 + float(seconds)/(60*60)) * (-1 if direction in ['W', 'S'] else 1)
            deg, minutes, seconds, direction =  re.split('[°\'"]', long_dms)
            long_dd = (float(deg) + float(minutes)/60 + float(seconds)/(60*60)) * (-1 if direction in ['W', 'S'] else 1)

            coords_list.append((lat_dd, long_dd))
        return coords_list
    
    def get_locations(self, filename: str) -> list:
        cords = self.get_coords(filename)
        return rg.search(cords)


class DataHandler:
    def __init__(self) -> None:
        self.xla_headers = [
            "ImgID",
            "NDVI"
        ]
        self.xla_csv_record_id = 0
    
    def get_image_ids(self, filename: str) -> list:
        d = filename
        ids = []
        for path in os.listdir(d):
            id = path[6:10]
            ids.append(id)
        return ids
    
    def get_data_dicts(self, ids, ndvis):
        datas = []
        for i, id in enumerate(ids):
            print(f"{id}, {ndvis[i]}")
            data = {"ImgID": id, "NDVI": ndvis[i]}
            datas.append(data)
        return datas

    def setup_xla_csv(self) -> None:
        """Create AI XLA specific CSV file and write column headers to it.
        """

        # Create empty CSV file for AI XLA Logging.
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