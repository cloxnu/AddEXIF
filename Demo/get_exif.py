from PIL import Image, ExifTags
import piexif
import exif

filename = "6.jpeg"

# with open(filename, "rb") as image_file:
#     img = exif.Image(image_file)
#
# img.gps_latitude = (41.0, 29.0, 57.48)
# img.gps_latitude_ref = "N"
# img.gps_longitude = (81.0, 41.0, 39.84)
# img.gps_longitude_ref = "W"
# img.gps_altitude = 199.034  # in meters
# img.gps_altitude_ref = exif.GpsAltitudeRef.ABOVE_SEA_LEVEL

img = Image.open(filename)
exif = {}

exif = piexif.load(img.info['exif'])

# for key, value in img._getexif().items():
#     if key not in ExifTags.TAGS:
#         print("{} is not in ExifTags".format(key))
#         continue
#     if ExifTags.TAGS[key] == "GPSInfo":
#         for gps_key, gps_value in value.items():
#             if gps_key not in ExifTags.GPSTAGS:
#                 print("{} is not in GPSTags".format(gps_key))
#                 continue
#             exif.setdefault("GPSInfo", {})[ExifTags.GPSTAGS[gps_key]] = gps_value
#     else:
#         exif[ExifTags.TAGS[key]] = value

pass

# with open(filename, "rb") as image_file:
#     exif_image = exif.Image(image_file)
    
# e = exif_image.get_all()
# print(e)