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
    def get_images(self) -> list:
        d = "interest-points"
        paths = []
        for path in os.listdir(d):
            full_path = os.path.abspath(os.path.join(d, path))
            if os.path.isfile(full_path):
                paths.append(full_path)
        return paths
    
    def get_coords(self) -> list:
        coords_list = []
        for path in self.get_images():
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
    
    def get_locations(self) -> list:
        cords = self.get_coords()
        return rg.search(cords)