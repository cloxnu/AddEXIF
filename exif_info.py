# import exif
import piexif
from PIL import Image
import datetime


class EXIFInfo:
    def __init__(self, exif_dict, filename):
        self.exif_dict = exif_dict
        self.filename = filename

    @classmethod
    def from_file(cls, filename):
        with Image.open(filename) as img:
            exif_dict = piexif.load(img.info["exif"])
        # with open(filename, 'rb') as image_file:
        #     exif_image = exif.Image(image_file)
        return cls(exif_dict, filename)

    def get_time(self, echo=False):
        time_str = self.exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal].decode('utf-8')
        if echo:
            print("The time is {}".format(time_str))
        time = datetime.datetime.strptime(time_str, "%Y:%m:%d %H:%M:%S")
        timezone_str = self.exif_dict['Exif'].get(piexif.ExifIFD.OffsetTimeOriginal)
        while timezone_str is None:
            timezone_str = self.input_time_zone()

        timezone = datetime.datetime.strptime(timezone_str, "%z")
        return time.replace(tzinfo=timezone.tzinfo)

    def write_gps_info(self, gps_info: dict):
        for key, value in gps_info.items():
            self.exif_dict['GPS'][key] = value
            # self.exif_image.set(key, value)
        exif_bytes = piexif.dump(self.exif_dict)

        with Image.open(self.filename) as img:
            img.save(self.filename, "jpeg", exif=exif_bytes)
        # with open(self.filename, 'wb') as image_file:
        #     image_file.write(self.exif_image.get_file())

    def input_time_zone(self) -> str:
        print("These images have no timezone infomation")
        for i in range(25):
            print("{}: {:+03d}:00".format(i, i - 12))
        print("25: custom")
        choice_input = input("Choose a timezone for these images: ")
        try:
            choice = int(choice_input)
        except ValueError:
            return None

        if choice == 25:
            return input("Input a timezone with format: +08:00: ")
        return "{:+03d}:00".format(choice - 12)
