import bookworm.command as command
import bookworm.util    as util
import os.path


class UnpackPDF(command.Command):
    """
    Unpack a pdf into a collection of TIFF files inside a target directory.
    """
    def __init__(self, source_pdf, target_dir, resolution=600):
        self.command = 'gs'
        self.source_pdf = source_pdf
        self.target_dir = target_dir
        self.args = [
            '-q', '-dNOPAUSE',   '-dBATCH',
            '-sDEVICE=tiff24nc', '-sCompression=lzw', 
            f'-r{resolution}x{resolution}',
            '-sOutputFile={}'.format(os.path.join(self.target_dir, '_Page_%04d.tiff'))
        ]

    def as_python_subprocess(self):
        return [self.command] + self.args + [self.source_pdf]

    def as_terminal_command(self):
        return self.command + ' ' + ' '.join(self.args) + ' ' + util.quoted_string(self.source_pdf)

    def image_dir(self):
        return self.target_dir

    def setup(self):
        """
        Prepare an action for execution by setting up folders and IO.
        """
        # The input file does not exist.
        if (not os.path.isfile(self.source_pdf)) and os.path.isdir(self.target_dir):
            raise FileNotFoundError('Input file does not exist: {}'.format(self.source_pdf))

        # The output file does not exist.
        elif (os.path.isfile(self.source_pdf)) and (not os.path.isdir(self.target_dir)):
            os.mkdir(self.target_dir)

        else:
            # Nothing needs to be done.
            return

    def commit(self):
        pass


def make(source_pdf, target_dir=''):
    """
    Unpack a PDF file into a collection of TIFF files, one for each page, into
    a target directory. If a target directory is not specified, a default one is
    used in the directory of the source pdf file.
    """
    if not target_dir:
        # Use a default directory.
        new_target_dir = os.path.join(os.path.dirname(source_pdf), util.default_subdirectory())
        return UnpackPDF(source_pdf, new_target_dir)
    else:
        # use the target directory
        return UnpackPDF(source_pdf, target_dir)


def process_args(arg_dict):
    """
    The ``process_args`` method parses the command line arguments in
    ``arg_dict`` and uses them to construct a page command. In particular,
    parse through the command line arguments to product an ``UnpackPDF``
    command.
    """
    try:
        input = arg_dict['input']
        output = arg_dict['output']
    except KeyError as e:
        raise e

    try:
        output = arg_dict['output']
        if not output:
            # Derive a default output directory from the input file.
            output = util.temp_directory(input)
    except KeyError as e:
        # Derive a default output directory from the input file.
        output = util.temp_directory(input)

    return make(input, output)

