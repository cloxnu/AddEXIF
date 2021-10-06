import math
import gpxpy


class Point:
    def __init__(self, latitude, longitude, elevation, time):
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation
        self.time = time

    @classmethod
    def between(cls, from_point, to_point, time):
        ratio = (time - from_point.time) / (to_point.time - from_point.time)
        print(ratio)
        latitude = from_point.latitude + (to_point.latitude - from_point.latitude) * ratio
        longitude = from_point.longitude + (to_point.longitude - from_point.longitude) * ratio
        elevation = from_point.elevation + (to_point.elevation - from_point.elevation) * ratio
        return cls(latitude, longitude, elevation, time)

    @property
    def lat_direction(self):
        return "N" if self.latitude >= 0 else "S"

    @property
    def lon_direction(self):
        return "E" if self.longitude >= 0 else "W"

    @property
    def lat_degree(self):
        lat_decimal, lat_deg = math.modf(abs(self.latitude))
        lat_min = lat_decimal * 60
        lat_sec, lat_min = math.modf(lat_min)
        return (int(lat_deg), 1), (int(lat_min), 1), (int(round(lat_sec * 60, 2) * 100), 100)

    @property
    def lon_degree(self):
        lon_decimal, lon_deg = math.modf(abs(self.longitude))
        lon_min = lon_decimal * 60
        lon_sec, lon_min = math.modf(lon_min)
        return (int(lon_deg), 1), (int(lon_min), 1), (int(round(lon_sec * 60, 2) * 100), 100)


class TrackSegment:
    def __init__(self):
        self.points = {}
        self.time = []

    def add_point(self, point: Point):
        self.points[point.time] = point
        self.time.append(point.time)

    def count(self):
        return len(self.time)

    @property
    def start_time(self):
        return self.time[0] if len(self.time) != 0 else None

    @property
    def end_time(self):
        return self.time[-1] if len(self.time) != 0 else None

    @classmethod
    def get_list_from_file(cls, filename, echo=False):
        segments = []
        with open(filename, 'r') as gpx_file:
            gpx_raw = gpxpy.parse(gpx_file)

            for track in gpx_raw.tracks:
                for segment in track.segments:
                    trkseg = cls()
                    for point in segment.points:
                        trkseg.add_point(Point(point.latitude, point.longitude, point.elevation, point.time))
                        if echo:
                            print(point.time)
                    segments.append(trkseg)

        return segments

    def find_point(self, time) -> Point:
        if time < self.start_time or time > self.end_time:
            return None
        left, right = 0, len(self.time) - 1
        while left <= right:
            mid = left + (right - left) // 2
            if self.time[mid] == time:
                return self.points[time]
            elif self.time[mid] > time:
                right = mid - 1
            else:
                left = mid + 1
        return Point.between(self.points[self.time[left - 1]], self.points[self.time[left]], time)


def find_segment_with_time(time, sorted_segments) -> TrackSegment:
    time_list = []
    if len(sorted_segments) == 0 or time < sorted_segments[0].start_time or time > sorted_segments[-1].end_time:
        return None
    for seg in sorted_segments:
        time_list.append(seg.start_time)
        time_list.append(seg.end_time)

    left, right = 0, len(time_list) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if time_list[mid] == time:
            return sorted_segments[mid // 2]
        elif time_list[mid] > time:
            right = mid - 1
        else:
            left = mid + 1
    if left % 2 == 0:
        return None
    return sorted_segments[left // 2]
