import bookworm.command as command
import bookworm.util    as util
import os.path

from bookworm.resolution import Resolution


class ChangeResolution(command.PageCommand):
    """
    Change a page's image resolution without modifying the page contents.
    """
    def __init__(self, source, target, resolution):
        self.command = 'convert'
        self.density = '-density {}'.format(resolution.value)
        self.units = '-units {}'.format(resolution.unit_str())
        self.source = source
        self.target = target
        self.resolution = resolution

    def as_python_subprocess(self):
        return [
            self.command,
            self.density,
            self.units,
            util.quoted_string(self.source),
            util.quoted_string(self.target)
        ]

    def as_terminal_command(self):
        return '{} {} {} {} {}'.format(
            self.command,
            self.density,
            self.units,
            util.quoted_string(self.source),
            util.quoted_string(self.target)
        )

    def setup(self):
        return NotImplemented

    def commit(self):
        return NotImplemented


def change_page_resolution(resolution, source, target=''):
    """
    The function ``change_page_resolution`` is a factory method that
    generates a ``ChangePageResolution`` command.
    """
    if resolution.value <= 0:
        raise ValueError(
            'Resolution must be positive. Got: {}'
            .format(resolution)
        )

    if not target:
        new_target = util.temp_file_name(source)
        return ChangeResolution(source, new_target, resolution)

    return ChangeResolution(source, target, resolution)


def multi_change_page_resolution(resolution, source_path, source_files, target):
    """
    Change the properties of multiple pages in a single directory.
    """
    actions = {}

    for source in source_files:
        action = change_page_resolution(resolution, os.path.join(source_path, source), target)
        actions[source] = action

    return actions


def process_args(arg_dict):
    """
    The ``process_args`` method parses the command line arguments in ``arg_dict`` and 
    uses them to construct a page command.
    """
    try:
        input      = arg_dict['input']
        resolution = arg_dict['resolution']
    except KeyError as e:
        raise e
    
    try:
        if resolution <= 0:
            raise ValueError('Resolution needs to be a positive integer. Got negative value: {}'.format(resolution))

        resolution = Resolution.make(resolution, 'PixelsPerInch')
    except TypeError as e:
        raise e
    except ValueError as e:
        raise e

    # We want to make multiple page operations if the input is a directory.
    if os.path.isdir(input):
        try:
            output = arg_dict['output']
        except KeyError as e:
            # Use input as the target file.
            output = input
        
        files_dict = {'path': input, 'files': os.listdir(input)}

        tiff_files_dict = util.with_extension('.tiff', files_dict)

        return multi_change_page_resolution(resolution, tiff_files_dict['path'], tiff_files_dict['files'], output)

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

