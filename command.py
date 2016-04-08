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


"""
Change a page's image resolution without modifying the page.
"""
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


"""
Rescale a page by changing it's resolution and  then resampling the image.
"""
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


"""
Expand the side of a page by expanding the edges of the page with a fill
color. This function only does this with the color white.
"""
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

    return '{}.bookworm.{}'.format(file, remove_leading_period(ext))


"""
Generate the same action across multiple pages.
"""
def generate_multiple_page_actions(command, sources, **kwargs):
    actions = {}

    for source in sources:
        action = command(source, kwargs)
        actions[source] = action

    return action

"""
Change a page's image resolution without modifying the page.
"""
def change_resolution(source, resolution, units):
    target = temp_file_name(source)

    return ChangeResolution(source, target, Resolution(resolution, units))

"""
Rescale a page by changing it's resolution and  then resampling the image.
"""
def rescale_page(source, resolution):
    target = temp_file_name(source)

    return RescalePage(source, target, Resolution(resolution, units))

"""
Expand the side of a page by expanding the edges of the page with a fill
color. This function only does this with the color white.
"""
def expand_page_with_fill(source, width, height):
    target = temp_file_name(source)

    return ExpandPageWithFill(source, target, width, height)


"""
Change the properties of multiple pages.
"""
def multi_change_page_resolutions(sources, resolution, units):    
    return generate_multiple_page_actions(change_resolution, sources, resolution, units)

def multi_rescale_page(sources, resolution, units):
    return generate_multiple_page_actions(rescale_page, sources, resolution, units)

def multi_expand_page(sources, width, height):
    return generate_multiple_page_actions(expand_page_with_fill, sources, resolution, units)


"""
Unpack a PDF file into a collection of TIFF files, one for each page, into
a target directory.
"""
def unpack_pdf(file_name, target_dir):
    pass

def pack_pdf():
    pass

"""
Execute a command in the shell.
"""
def execute(command):
    subprocess.run(command.as_arg_list())