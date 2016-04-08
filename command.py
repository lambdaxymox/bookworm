import subprocess

from enum import Enum


class ResolutionUnits(Enum):
    PixelsPerInch       = 1
    PixelsPerCentimeter = 2

    def __repr__(self):
        if self == PixelsPerInch:
            return 'PixelsPerInch'
        else:
            return 'PixelsPerCentimeter'

    def __str__(self):
        return repr(self)


class Resolution:
    def __init__(self, resolution, units):
        self.resolution = resolution
        self.units      = units

    def __repr__(self):
        return 'Resolution({}, {})'.format(self.resolution, self, units)

    def __str__(self):
        return '{} {}'.format(self.resolution, self.units)


"""
The main pdf operations. The primary operation are:

1. Unpack a PDF.
2. Repack a PDF.
2. Pack a directory of images into a PDF.
3. Change image resolution.
4. Rescale image.
5. Expand image with fill.

"""
class Command:
    def __init__(self):
        pass

    def as_arg_list(self):
        raise NotImplemented

    def as_terminal_command(self):
        return 'echo NotImplemented'

    def as_arg_list(self):
        return ['echo', 'NotImplemented']

    def __str__(self):
        return self.as_terminal_arg()

    def __repr__(self):
        return 'Command({})'.format(self.as_arg_list())


class ChangeResolution(Command):
    def __init__(source, target, resolution):
        self.command = 'convert'
        self.density = '-density {}'.format(resolution.resolution)
        self.units   = '-units {}'.format(resolution.units)
        self.source  = '\"{}\"'.format(source)
        self.target  = '\"{}\"'.format(target)

    def as_arg_list(self):
        return [self.command, self.density, self.units, self.source, self.target]

    def as_terminal_command(self):
        return  \
            '{} {} {} {} {}'.format(self.command, self.density, self.units, self.source, self.target)


class RescalePage(Command):
    def __init__(source, target, resolution):
        self.command  = 'convert'
        self.units    = '-units {}'.format(resolution.units)
        self.resample = '-resample {}'.format(resolution.resolution)
        self.source   = '\"{}\"'.format(source)
        self.target   = '\"{}\"'.format(target)

    def as_arg_list(self):
        return [self.command, self.units, self.resample, self.source, self.target]

    def as_terminal_command(self):
        return \
            '{} {} {} {} {}' \
            .format(self.command, self.units, self.resample, self.quoted_old_file, self.quoted_new_file)


class ExpandPageWithFill(Command):
    def __init__(source, target, width, height):
        self.command    = 'convert'
        self.extent     = '-extent {}x{}'.format(width, height)
        self.background = '-background white'
        self.gravity    = '-gravity Center'
        self.source     = '\"{}\"'.format(source)
        self.target     = '\"{}\"'.format(target)

    def as_arg_list(self):
        return [self.command, self.extent, self.background, self.gravity, self.source, self.target]

    def as_terminal_command(self):
        final_arg = '{}[{}x{}]'.format(self.source, self.width, self.height)
        
        return \
            '{} {} {} {} {} {}' \
            .format(self.command, self.extent, self.background, self.gravity, self.source, final_arg)


class UnpackPDF(Command):
    pass

class PackPDF(Command):
    pass

def build_command():
    pass

def execute(command):
    try:
        subprocess.run(command.as_arg_list())
    except subprocess.CalledProcessError as e:
        raise e