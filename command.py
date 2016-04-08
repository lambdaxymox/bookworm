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
class TerminalCommand:
    def __init__(self, **kwargs):
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


class ChangeResolution(TerminalCommand):
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


class RescalePage(TerminalCommand):
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


class ExpandPageWithFill(TerminalCommand):
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


class UnpackPDF(TerminalCommand):
    pass

class PackPDF(TerminalCommand):
    pass


def temp_file_name(file_name):
    
    def remove_leading_period(file_ext):
        if file_ext[0] == '.':
            return file_ext[1:]
        else:
            return file_ext


    file, ext = os.path.splitext(file_name)

    return '{}.tmp.{}'.format(file, remove_leading_period(ext))


def change_resolution(source, resolution, units):
    target = temp_file_name(source)

    return ChangeResolution(source, target, Resolution(resolution, units))


def rescale_page(source, resolution):
    target = temp_file_name(source)

    return RescalePage(source, target, Resolution(resolution, units))


def expand_page_with_fill(source, width, height):
    target = temp_file_name(source)

    return ExpandPageWithFill(source, target, width, height)


def multi_change_page_resolutions(sources, resolution, units):    
    actions = {}

    for source in sources.keys():
        action = change_page_resolution(source, resolution, units)
        actions[source] = action

    return actions

def multi_rescale_page(sources, resolution, units):
    actions = {}

    for source in sources.keys():
        action = rescale_page(source, resolution, units)
        actions[source] = action

    return actions

def multi_expand_page(sources, width, height):
    actions = {}

    for source in sources.keys():
        action = expand_page_with_fill(source, width, height)
        actions[source] = action

    return actions
    

def unpack_pdf():
    pass

def pack_pdf():
    pass

def execute(command):
    subprocess.run(command.as_arg_list())