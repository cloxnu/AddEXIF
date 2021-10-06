from gpx_info import *
from exif_info import *

if __name__ == '__main__':
    segments = TrackSegment.get_list_from_file('Demo/1.gpx', echo=True)
    segments.sort(key=lambda seg: seg.start_time)
    print(len(segments))

    exif_info = EXIFInfo.from_file('Demo/1.jpeg')
    time = exif_info.get_time(echo=True)

    seg = find_segment_with_time(time, segments)
    if seg is None:
        print("There is no corresponding GPS record for the time of image.")
    else:
        point = seg.find_point(time)
        exif_info.write_gps_info({
            piexif.GPSIFD.GPSLatitude: point.lat_degree,
            piexif.GPSIFD.GPSLatitudeRef: point.lat_direction,
            piexif.GPSIFD.GPSLongitude: point.lon_degree,
            piexif.GPSIFD.GPSLongitudeRef: point.lon_direction,
            # piexif.GPSIFD.GPSAltitude: point.elevation,
            # piexif.GPSIFD.GPSAltitudeRef: piexif.GPSIFD.GPSAltitudeRef
        })
