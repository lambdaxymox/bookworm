import bookworm.abstract as abstract
import bookworm.util     as util
import subprocess
import os.path


class UnpackPDF(abstract.Command):
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

    def as_subprocess(self):
        return [self.command] + self.args + [self.source_pdf]

    def as_terminal_command(self):
        return '{} {} {}'.format(
            self.command,
            ' '.join(self.args),
            util.quoted_string(self.source_pdf)
        )

    @property
    def image_dir(self):
        return self.target_dir


class Runner(abstract.Runner):

    def setup(command):
        """
        Prepare an action for execution by setting up folders and I/O.
        """
        # The input file does not exist.
        if (not os.path.isfile(command.source_pdf)) and os.path.isdir(command.target_dir):
            raise FileNotFoundError(
                f'Input file does not exist: {command.source_pdf}'
            )

        # The output folder does not exist.
        elif (os.path.isfile(command.source_pdf)) and (not os.path.isdir(command.target_dir)):
            os.mkdir(command.target_dir)

        else:
            # Nothing needs to be done.
            return

    def execute(command):
        # The target directory should be empty.
        if not os.listdir(command.target_dir):
            subprocess.run(command.as_subprocess())
        else:
            raise FileExistsError(
                'This directory contains other files. '
                'Unpack PDF will not write to an occupied directory.'
            )

    def cleanup(command):
        """
        The ``cleanup`` method is applied after a failure occurs to clean up
        the target directory by removing the data created during setup or
        execution.
        """
        files = os.listdir(command.target_dir)
        for file in files:
            file_path = os.path.join(command.target_dir, file)
            os.remove(file_path)

        os.rmdir(command.target_dir)


def make(source_pdf, target_dir=''):
    """
    The ``make`` factory method unpacks a PDF file into a collection of TIFF 
    files, one per page, into the target directory. If a target directory is
    not specified, a default one is used in the directory of the source pdf
    file.
    """
    if not target_dir:
        # Use a default directory.
        new_target_dir = os.path.join(
            os.path.dirname(source_pdf), util.default_subdirectory()
        )
        return UnpackPDF(source_pdf, new_target_dir)
    else:
        # use the target directory
        return UnpackPDF(source_pdf, target_dir)


def process_args(arg_dict):
    """
    The ``process_args`` factory method parses the command line arguments in
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

