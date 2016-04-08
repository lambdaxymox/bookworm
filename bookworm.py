import subprocess
import os.path

from enum import Enum


class ResolutionUnits(Enum):
    PixelsPerInch       = 1
    PixelsPerCentimeter = 2

    def __repr__(self):
        if self == PixelsPerInch:
            return "PixelsPerInch"
        else:
            return "PixelsPerCentimeter"

    def as_terminal_arg(self):
        return repr(self)


class Resolution:
    def __init__(resolution, units):
        self.resolution = resolution
        self.units = units


def temp_filename(file_name):
    return "{}.tmp".format(file_name)


def cleanup(file_name):
    os.remove(file_name)


"""
The main pdf operations. The primary operation are:
1. Unpack a PDF.
2. Pack a directory of images into a PDF.
3. Change image resolution.
4. Rescale image.
5. Expand image with fill.
"""

def unpack_pdf(file_name):
    pass

def pack_pdf(directory):
    pass

def change_resolution(resolution, image_file):
    new_image_file = temp_filename(image_file)
    density = "-density {}".format(resolution.resolution)
    units = "-units {}".format(resolution.units)

    try:
        subprocess.run(["convert", density, units, new_image_file])
    except subprocess.CalledProcessError as e:
        cleanup(new_image_file)
        raise e
    
    os.remove(image_file)
    os.rename(new_image_file, image_file)
    
        
def rescale(resolution, image_file):
    gravity = "-gravity center"


def expand_file_with_fill(dimensions, image_file):
    pass


def usage():
    return  'USAGE:\n' \
            'python3 bookworm.py [-options] /path/to/image/files/\n' \
            'or\n' \
            'python3 bookworm.py [-options] /path/to/pdf/file\n'


def main():
    print(usage())


if __name__ == 'main':
    main()
else:
    main()