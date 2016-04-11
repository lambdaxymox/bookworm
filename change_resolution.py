import command
import os.path

from command import Resolution


class ChangeResolution(command.PageCommand):
    """
    Change a page's image resolution without modifying the page.
    """
    def __init__(self, source, target, resolution):
        self.command = 'convert'
        self.density = '-density {}'.format(resolution.resolution)
        self.units   = '-units {}'.format(resolution.unit_str())
        self.source  = source
        self.target  = target

    def as_python_subprocess(self):
        return [self.command, self.density, self.units, 
                    command.quoted_string(self.source), command.quoted_string(self.target)]

    def as_terminal_command(self):
        return  '{} {} {} {} {}'.format(self.command, self.density, self.units, 
                    command.quoted_string(self.source), command.quoted_string(target))

    def setup(self):
        pass


def change_page_resolution(resolution, source, target=''):
    """
    Change a page's image resolution without modifying the page.
    """
    if resolution.resolution <= 0:
        raise ValueError('Resolution must be positive. Got: {}'.format(resolution))

    if not target:
        new_target = command.temp_file_name(source)
        return ChangeResolution(source, new_target, resolution)

    return ChangeResolution(source, target, resolution)


def multi_change_page_resolution(resolution, sources, target):    
    """
    Change the properties of multiple pages in a single directory.
    """
    actions = {}

    for source in sources:
        action = change_page_resolution(resolution, source, target)
        actions[source] = action

    return actions


def process_args(arg_dict):
    try:
        input      = arg_dict['input']
        resolution = arg_dict['resolution']
    except KeyError as e:
        raise e
    
    try:
        if resolution <= 0:
            raise ValueError('Resolution needs to be a positive integer. Got negative value: {}'.format(resolution))

        resolution = Resolution.make_resolution(resolution, 'PixelsPerInch')
    except TypeError as e:
        raise e
    except ValueError as e:
        raise e

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
