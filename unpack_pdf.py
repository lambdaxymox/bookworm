import command
import os.path


class UnpackPDF(command.PDFCommand):
    """
    Unpack a pdf into a collection of TIFF files.
    """
    def __init__(self, source_pdf, target_dir, resolution=600):
        self.command    = 'gs'
        self.source_pdf = source_pdf
        self.target_dir = target_dir
        self.args = ['-q', '-dNOPAUSE',   '-dBATCH',
                     '-sDEVICE=tiff24nc', '-sCompression=lzw', 
                     '-r{}x{}'.format(resolution, resolution),
                     '-sOutputFile=' + self.target_dir + '_Page_%4d.tiff'
                    ]

    def as_python_subprocess(self):
        return [self.command] + self.args + [self.source_pdf]

    def as_terminal_command(self):
        return self.command + ' ' + ' '.join(self.args) + ' ' + self.source_pdf

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
        elif (os.path.isfile(self)) and (not os.path.isdir(self.target_dir)):
            os.mkdir(self.target_dir)

        else:
            #raise FileNotFoundError('File or directory does not exist: \nInput: {}\nOutput: {}'.format(input, output))
            # Nothing needs to be done.
            return


def unpack_pdf(source_pdf, target_dir=''):
    """
    Unpack a PDF file into a collection of TIFF files, one for each page, into
    a target directory. If a target directory is not specified, a default one is
    used in the directory of the source pdf file.
    """
    if not target_dir:
        # Use a default directory.
        new_target_dir = os.path.join(os.path.dirname(source_pdf), command.default_subdirectory())
        return UnpackPDF(source_pdf, new_target_dir)
    else:
        # use the target directory
        return UnpackPDF(source_pdf, target_dir)


def process_args(arg_dict):
    """
    Parse through the command line arguments for unpack-pdf.
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
            output = command.temp_directory(input)
    except KeyError as e:
        # Derive a default output directory from the input file.
        output = command.temp_directory(input)

    return unpack_pdf(input, output)
"""
    if os.path.isfile(input) and os.path.isdir(output):
        return unpack_pdf(input, output)

    # The input file does not exist.
    elif (not os.path.isfile(input)) and os.path.isdir(output):
        raise FileNotFoundError('Input file does not exist: {}'.format(input))

    # The output file does not exist.
    elif (os.path.isfile(input)) and (not os.path.isdir(output)):
        #raise FileNotFoundError('Output directory does not exist: {}'.format(output))
        os.mkdir(output)

        return unpack_pdf(input, output)
    else:
        raise FileNotFoundError('File or directory does not exist: \nInput: {}\nOutput: {}'.format(input, output))
"""

