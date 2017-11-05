import bookworm.command as command
import bookworm.util    as util


class ResamplePage(command.PageCommand):
    """
    Rescale a page by changing its resolution and then resampling the image.
    """
    def __init__(self, source, target, resolution):
        self.command  = 'convert'
        self.units    = '-units PixelsPerInch'
        self.resample = '-resample {}'.format(resolution)
        self.source   = '\"{}\"'.format(source)
        self.target   = '\"{}\"'.format(target)

    def as_python_subprocess(self):
        return [self.command, self.units, self.resample, self.source, self.target]

    def as_terminal_command(self):
        return \
            '{} {} {} {} {}' \
            .format(self.command, self.units, self.resample, self.quoted_old_file, self.quoted_new_file)


def resample_page(resolution, source, target=''):
    """
    The function ``resample_page`` is a factory method that generates a
    ``ResamplePage`` command.
    """
    if not target:
        new_target = command.temp_file_name(source)
        return ResamplePage(source, new_target, resolution)

    return ResamplePage(source, target, resolution)


def multi_resample_page(resolution, source_path, source_files, target):
    """
    Resample multiple pages.
    """
    actions = {}

    for source in sources:
        action = resample_page(resolution, os.path.join(source_path, source), target)
        actions[source] = action

    return actions


def process_args(arg_dict):
    """
    The ``process_args`` method parses the command line arguments in ``arg_dict`` and 
    uses them to construct a ``ResamplePage`` command.
    """
    try:
        input = arg_dict['input']
        resolution_val = arg_dict['resolution']
        units = arg_dict['units'] 
    except KeyError as e:
        raise e

    print("foo")
    if resolution_val <= 0:
        raise ValueError(
            'Resolution needs to be a positive integer.' 
            'Got nonpositive value: {}'
            .format(resolution_val)
        )

    try:
        resolution = util.make_resolution(resolution_val, units)
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

        return resample_page(resolution, input, output)

    else:
        raise FileNotFoundError('File or directory does not exist: {}'.format(input))

