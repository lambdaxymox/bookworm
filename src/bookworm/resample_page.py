import bookworm.command as command


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


def multi_rescale_page(resolution, sources, target):
    """
    Resample multiple pages.
    """
    actions = {}

    for source in sources:
        action = resample_page(source, target, resolution)
        actions[source] = action

    return actions


def process_args(arg_dict):
    """
    The ``process_args`` method parses the command line arguments in ``arg_dict`` and 
    uses them to construct a ``ResamplePage`` command.
    """
    return NotImplemented

