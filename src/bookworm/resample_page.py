import os
import bookworm.abstract as abstract
import bookworm.util     as util

from bookworm.resolution import Resolution


class ResamplePage(abstract.Command):
    """
    Rescale a page by changing its resolution and then resampling the image.
    """
    def __init__(self, source, target, resolution):
        self.command  = 'convert'
        self.units    = '-units {}'.format(resolution.unit_str())
        self.resample = '-resample {}'.format(resolution.value)
        self.source   = '\"{}\"'.format(source)
        self.target   = '\"{}\"'.format(target)

    def as_python_subprocess(self):
        return [
            self.command,
            self.units,
            self.resample,
            self.source,
            self.target
        ]

    def as_terminal_command(self):
        return \
            '{} {} {} {} {}' \
            .format(self.command, self.units, self.resample, self.quoted_old_file, self.quoted_new_file)


def make(resolution, source, target=''):
    """
    The ``make`` factory method that generates a ``ResamplePage`` command.
    """
    if not target:
        new_target = util.temp_file_name(source)
        return ResamplePage(source, new_target, resolution)

    return ResamplePage(source, target, resolution)


def multi_resample_page(resolution, source_path, source_files, target):
    """
    Resample multiple pages.
    """
    actions = {}
    for source_file in source_files:
        action = resample_page(resolution, os.path.join(source_path, source_file), target)
        actions[source_file] = action

    return actions


def process_args(arg_dict):
    """
    The ``process_args`` factory method parses the command line arguments in 
    ``arg_dict`` and uses them to construct a ``ResamplePage`` command.
    """
    try:
        input = arg_dict['input']
        resolution_val = arg_dict['resolution']
        unit_str = arg_dict['units'] 
    except KeyError as e:
        raise e

    if resolution_val <= 0:
        raise ValueError(
            'Resolution needs to be a positive integer.' 
            'Got nonpositive value: {}'
            .format(resolution_val)
        )

    try:
        resolution = Resolution.make(resolution_val, unit_str)
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

        return multi_resample_page(resolution, tiff_files_dict['path'], tiff_files_dict['files'], output)

    # If the input is one page only, we only need a single resample page operation.
    elif os.path.isfile(input):
        try:
            output = arg_dict['output']
        except KeyError as e:
            # Use input as the target file.
            output = input

        return make(resolution, input, output)

    else:
        raise FileNotFoundError(f'File or directory does not exist: {input}')

