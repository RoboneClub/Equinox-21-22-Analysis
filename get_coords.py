"""input:
GPS Latitude Ref - South
GPS Latitude - 51 deg 21' 50.20"
GPS Longitude Ref - West
GPS Longitude - 73 deg 26' 15.40"
"""

import pyperclip
import PIL.Image
import PIL.ExifTags
from pathlib import Path
import re
lat = '''51°36'9.18"N'''
deg, minutes, seconds, direction =  re.split('[°\'"]', lat)
(float(deg) + float(minutes)/60 + float(seconds)/(60*60)) * (-1 if direction in ['W', 'S'] else 1)

route = True if str(input("exif?> ")) == "" else False
if route:
    img_id = input("img_id> ")
    path = f"{Path(__file__).parent.resolve()}\\{str(img_id).zfill(4)}.jpg"
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

    coords = f"{lat_dd}, {long_dd}"
else:
    lat_ref = str(input("> "))
    lat = str(input("> "))
    long_ref = str(input("> "))
    long = str(input("> "))

    lat_ref, long_ref = lat_ref[19], long_ref[20]

    lat = lat[15:].replace(" ", "").replace("deg", "°")
    long = long[15:].replace(" ", "").replace("deg", "°")

    coords = f"{lat}{lat_ref}, {long}{long_ref}"

print(coords)

pyperclip.copy(coords)
