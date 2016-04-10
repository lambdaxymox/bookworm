import subprocess
import os.path


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
        raise NotImplemented

    def as_arg_list(self):
        raise NotImplemented

    def is_page_action(self):
        raise NotImplemented

    def is_pdf_action(self):
        raise NotImplemented

    def __str__(self):
        return self.as_terminal_command()

    def __repr__(self):
        return 'Command({})'.format(self.as_arg_list())


class PageCommand(TerminalCommand):

    def is_page_action(self):
        return True

    def is_pdf_action(self):
        return False


class PDFCommand(TerminalCommand):

    def is_page_action(self):
        return False

    def is_pdf_action(self):
        return True

    def tiff_dir(self):
        raise NotImplemented


"""
Change a page's image resolution without modifying the page.
"""
class ChangeResolution(PageCommand):
    def __init__(self, source, target, resolution):
        self.command = 'convert'
        self.density = '-density {}'.format(resolution)
        self.units   = '-units PixelsPerInch'
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
class RescalePage(PageCommand):
    def __init__(self, source, target, resolution):
        self.command  = 'convert'
        self.units    = '-units PixelsPerInch'
        self.resample = '-resample {}'.format(resolution)
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
class ExpandPageWithFill(PageCommand):
    def __init__(self, source, target, width, height):
        self.command    = 'convert'
        self.extent     = '-extent {}x{}'.format(width, height)
        self.background = '-background white'
        self.gravity    = '-gravity Center'
        self.source     = '\"{}\"'.format(source)
        self.target     = '\"{}\"'.format(target)
        self.width      = width
        self.height     = height

    def as_arg_list(self):
        return [self.command, self.extent, self.background, self.gravity, self.source, self.target]

    def as_terminal_command(self):
        final_arg = '{}[{}x{}]'.format(self.target, self.width, self.height)
        
        return \
            '{} {} {} {} {} {}' \
            .format(self.command, self.extent, self.background, self.gravity, self.source, final_arg)


"""
Unpack a pdf into a collection of TIFF files.
"""
class UnpackPDF(PDFCommand):
    def __init__(self, source_pdf, target_dir, resolution=600):
        self.command    = 'gs'
        self.source_pdf = source_pdf
        self.target_dir = target_dir
        self.args = ['-q', '-dNOPAUSE',   '-dBATCH',
                     '-sDEVICE=tiff24nc', '-sCompression=lzw', 
                     '-r{}x{}'.format(resolution, resolution),
                     '-sOutputFile=' + self.target_dir + '_Page_%4d.tiff'
                    ]

        print(self.target_dir)

    def as_arg_list(self):
        return [self.command] + self.args + [self.source_pdf]

    def as_terminal_command(self):
        return self.command + ' ' + ' '.join(self.args) + ' ' + self.source_pdf

    def tiff_dir(self):
        return self.target_dir


class PackPDF(PDFCommand):
    def __init__(self):
        pass


def temp_file_name(file_name):
    
    def remove_leading_period(file_ext):
        if file_ext[0] == '.':
            return file_ext[1:]
        else:
            return file_ext


    file, ext = os.path.splitext(file_name)

    return '{}.bookworm.{}'.format(file, remove_leading_period(ext))


def temp_directory(file_name):
    file_path, ext = os.path.splitext(file_name)

    new_path = os.path.dirname(file_path)

    return os.path.join(new_path, '__bookworm__/')


"""
Change a page's image resolution without modifying the page.
"""
def change_page_resolution(resolution, source, target=''):
    if target =='':
        new_target = temp_file_name(source)
        return ChangeResolution(source, new_target, resolution)

    return ChangeResolution(source, target, resolution)

"""
Rescale a page by changing it's resolution and  then resampling the image.
"""
def rescale_page(resolution, source, target=''):
    if target == '':
        new_target = temp_file_name(source)
        return RescalePage(source, target, resolution)

    return RescalePage(source, target, resolution)

"""
Expand the side of a page by expanding the edges of the page with a fill
color. This function only does this with the color white.
"""
def expand_page_with_fill(width, height, source, target=''):
    if target == '':
        new_target = temp_file_name(source)
        return ExpandPageWithFill(source, new_target, width, height)

    return ExpandPageWithFill(source, target, width, height)


"""
Change the properties of multiple pages.
"""
def multi_change_page_resolution(sources, target, resolution):    
    actions = {}

    for source in sources:
        action = change_page_resolution(source, target, resolution)
        actions[source] = action

    return actions

def multi_rescale_page(sources, target, resolution):
    actions = {}

    for source in sources:
        action = rescale_page(source, target, resolution)
        actions[source] = action

    return actions

def multi_expand_page(sources, target, width, height):
    actions = {}

    for source in sources:
        action = expand_page_with_fill(source, width, height)
        actions[source] = action

    return actions


"""
Unpack a PDF file into a collection of TIFF files, one for each page, into
a target directory. If a target directory is not specified, a default one is
used in the directory of the source pdf file.
"""
def unpack_pdf(source_pdf, target_dir=''):
    if target_dir == '':
        # Use a default directory.
        new_target_dir = os.path.join(os.path.dirname(source_pdf), '__bookworm__/')
        return UnpackPDF(source_pdf, new_target_dir)
    else:
        # use the target directory
        return UnpackPDF(source_pdf, target_dir)


def pack_pdf():
    raise NotImplemented
