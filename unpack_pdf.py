import command
import os.path

"""
Unpack a pdf into a collection of TIFF files.
"""
class UnpackPDF(command.PDFCommand):
    def __init__(self, source_pdf, target_dir, resolution=600):
        self.command    = 'gs'
        self.source_pdf = source_pdf
        self.target_dir = target_dir
        self.args = ['-q', '-dNOPAUSE',   '-dBATCH',
                     '-sDEVICE=tiff24nc', '-sCompression=lzw', 
                     '-r{}x{}'.format(resolution, resolution),
                     '-sOutputFile=' + self.target_dir + '_Page_%4d.tiff'
                    ]

        print(self.target_dir)

    def as_arg_list(self):
        return [self.command] + self.args + [self.source_pdf]

    def as_terminal_command(self):
        return self.command + ' ' + ' '.join(self.args) + ' ' + self.source_pdf

    def tiff_dir(self):
        return self.target_dir


"""
Unpack a PDF file into a collection of TIFF files, one for each page, into
a target directory. If a target directory is not specified, a default one is
used in the directory of the source pdf file.
"""
def unpack_pdf(source_pdf, target_dir=''):
    if not target_dir:
        # Use a default directory.
        new_target_dir = os.path.join(os.path.dirname(source_pdf), '__bookworm__/')
        return UnpackPDF(source_pdf, new_target_dir)
    else:
        # use the target directory
        return UnpackPDF(source_pdf, target_dir)


def process_args(arg_dict):
    try:
        input = arg_dict['input']
    except KeyError as e:
        raise e

    try:
        output = arg_dict['output']
    except KeyError as e:
        # Derive a default output directory from the input file.
        output = temp_directory(input)

    if os.path.isfile(input) and os.path.isdir(output):
        return unpack_pdf(input, output)

    # The input file does not exist.
    elif (not os.path.isfile(input)) and os.path.isdir(output):
        raise ValueError('Output directory does not exist: {}'.format(output))
    # The output file does not exist.
    elif (os.path.isfile(input)) and (not os.path.isdir(output)):
        raise ValueError('Input file does not exist: {}'.format(input))
    else:
        raise ValueError('File or directory does not exist: \nInput: {}\nOutput: {}'.format(input, output))