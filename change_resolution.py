import command
import os.path

from command import Resolution

"""
Change a page's image resolution without modifying the page.
"""
class ChangeResolution(command.PageCommand):
    def __init__(self, source, target, resolution):
        self.command = 'convert'
        self.density = '-density {}'.format(resolution.resolution)
        self.units   = '-units {}'.format(resolution.unit_str())
        self.source  = '\"{}\"'.format(source)
        self.target  = '\"{}\"'.format(target)

    def as_python_subprocess(self):
        return [self.command, self.density, self.units, self.source, self.target]

    def as_terminal_command(self):
        return  \
            '{} {} {} {} {}'.format(self.command, self.density, self.units, self.source, self.target)


"""
Change a page's image resolution without modifying the page.
"""
def change_page_resolution(resolution, source, target=''):
    if resolution.resolution <= 0:
        raise ValueError('Resolution must be positive. Got: {}'.format(resolution))

    if not target:
        new_target = command.temp_file_name(source)
        return ChangeResolution(source, new_target, resolution)

    return ChangeResolution(source, target, resolution)


"""
Change the properties of multiple pages in a single directory.
"""
def multi_change_page_resolution(resolution, sources, target):    
    actions = {}

    for source in sources:
        action = change_page_resolution(source, target, resolution)
        actions[source] = action

    return actions


def process_args(arg_dict):
    try:
        input      = arg_dict['input']
        resolution = arg_dict['resolution']
    except KeyError as e:
        raise e

    if not resolution:
        raise ValueError('Invalid resolution value: {}'.format(resolution))

    if type(resolution) != int:
        raise ValueError('Invalid resolution value: {}'.format(resolution))

    if resolution <= 0:
        raise ValueError('Resolution needs to be a positive integer. Got negative value: {}'.format(resolution))

    resolution = Resolution.make_resolution(resolution, 'PixelsPerInch')

    # We want to make multiple page operations if the input is a directory.
    if os.path.isdir(input):
        files = command.with_extension('.tiff', input)

        return multi_change_page_resolution(resolution, files, output)

    # If the input is one page only, we only need a single page operation.
    elif os.path.isfile(input):
        try:
            output = arg_dict['output']
        except KeyError as e:
            # Use input as the target file.
            output = input

        return change_page_resolution(resolution, input, output)

    else:
        raise FileNotFoundError('File or directory does not exist: {}'.format(input))
