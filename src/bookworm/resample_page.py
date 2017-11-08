import os
import bookworm.abstract as abstract
import bookworm.util     as util

from bookworm.resolution import Resolution


class ResamplePage(abstract.Command):
    """
    Rescale a page by changing its resolution and then resampling the image.
    """
    def __init__(self, source_file, target_file, resolution):
        self.command = 'convert'
        self.units = f'-units {resolution.unit_str()}'
        self.resample = f'-resample {resolution.value}'
        self.source_file = f'\"{source_file}\"'
        self.target_file = f'\"{target_file}\"'

    def as_subprocess(self):
        return [
            self.command,
            self.units,
            self.resample,
            self.source_file,
            self.target_file
        ]

    def as_terminal_command(self):
        return '{} {} {} {} {}'.format(
            self.command, 
            self.units, 
            self.resample, 
            self.source_file, 
            self.target_file
        )


def make(resolution, source_file, target_file=''):
    """
    The ``make`` factory method that generates a ``ResamplePage`` command.
    """
    if not target_file:
        new_target_file = util.temp_file_name(source_file)
        return ResamplePage(source_file, new_target_file, resolution)

    return ResamplePage(source_file, target_file, resolution)


def multi_resample_page(resolution, source_path, source_files, target):
    """
    Resample multiple pages.
    """
    actions = {}
    for source_file in source_files:
        action = resample_page(
            resolution,
            os.path.join(source_path, source_file),
            target
        )
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
            'Resolution needs to be a positive integer. '
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

        return multi_resample_page(
            resolution,
            tiff_files_dict['path'],
            tiff_files_dict['files'],
            output
        )

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


class Runner(abstract.Runner):

    def setup(command):
        """
        Prepare an action for execution by setting up folders and I/O.
        """
        if os.path.isfile(command.source_file):
            if not os.path.isdir(command.target_path):
                os.mkdir(command.target_path)
        else:
            raise FileNotFoundError(
                f'File does not exist: {command.source_file}'
            )

    def execute(command):
        subprocess.run(command.as_subprocess())

    def cleanup(command):
        return

