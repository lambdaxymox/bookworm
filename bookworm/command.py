import os.path
import enum
import subprocess


@enum.unique
class ResolutionUnits(enum.Enum):
    PixelsPerInch       = 1
    PixelsPerCentimeter = 2

    def __str__(self):
        return self.name


class Resolution:

    def __init__(self, resolution, units):
        self.resolution = resolution
        self.units      = units

    def make_resolution(resolution_val, unit_str):
        if unit_str not in ResolutionUnits.__members__.keys():
            raise ValueError('\'unit_str\' must be one of: {}'.format(ResolutionUnits.__members__.keys()))
        
        if type(resolution_val) is not int:
            raise TypeError('\'resolution_val\' must be a positive integer')

        if resolution_val <= 0:
            raise ValueError('\'resolution_val\' must be a positive integer')
        
        return Resolution(resolution_val, ResolutionUnits.__members__[unit_str])

    def unit_str(self):
        return str(self.units)

    def __repr__(self):
        return 'Resolution({}, {})'.format(self.resolution, self.units)

    def __str__(self):
        return '{} {}'.format(self.resolution, self.units)


class TerminalCommand:

    def __init__(self, **kwargs):
        pass

    def as_arg_list(self):
        return NotImplemented

    def as_terminal_command(self):
        return NotImplemented

    def as_python_subprocess(self):
        return NotImplemented

    def setup(self):
        return NotImplemented

    def run(self):
        """
        Execute a command in the shell.
        """
        subprocess.run(self.as_python_subprocess())

    def commit(self):
        """
        Commit and clean up after a successful execution
        """
        return NotImplemented

    def __str__(self):
        return self.as_terminal_command()

    def __repr__(self):
        return 'Command({})'.format(self.as_python_subprocess())


class PageCommand(TerminalCommand):
    def commit(self):
        return NotImplemented


class PDFCommand(TerminalCommand):

    def commit(self):
        return NotImplemented

    def image_dir(self):
        return NotImplemented


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


def default_subdirectory():
    return '__bookworm__/'


def with_extension(extension, file_dict):
    """
    Get the collection of files in a directory with a given file extension.
    """
    def by_ext(extension, file):
        file_extension = os.path.splitext(file)[1]

        return file_extension == extension

    if extension[0] != '.':
        # Prepend a leading period.
        extension = '.' + extension

    try:
        path  = file_dict['path']
        files = file_dict['files']
    except KeyError as e:
        raise e

    return {'path': path, 'files': list(filter(lambda file: by_ext(extension, file), files))}


def files_exist(files):
    """
    Check that the files actually exist.
    """
    for file in files:
        if not os.path.isfile(file):
            return False

    return True


def make_resolution(resolution_val, unit_str):
    return Resolution.make_resolution(resolution_val, unit_str)


def quoted_string(string):
    """
    Determines whether a string begins and ends with quotes or not. If not, it closes
    the input string in quotes.
    """
    new_string = string

    if string[0] != '\"':
        new_string = '\"' + new_string
    
    if string[len(string)-1] != '\"':
        new_string = new_string + '\"'

    return new_string

