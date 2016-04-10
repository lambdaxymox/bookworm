import argparse
import sys
import execute_commands
import command
import os.path


def arg_processor():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(title='subcommands', description='valid subcommands', help='subcommand help')

    parser_unpack_pdf = subparsers.add_parser('unpack-pdf', 
        help='Unpack an input PDF file to the output directory')
    parser_unpack_pdf.add_argument('-i', '--input',  help='Input file')
    parser_unpack_pdf.add_argument('-o', '--output', help='Output directory')

    parser_change_resolution = subparsers.add_parser('change-resolution', 
        help='Change the resolution of the TIFF files in the input directory to RESOLUTION in UNITS')
    parser_change_resolution.add_argument('-r', '--resolution', help='The value for RESOLUTION', type=check_positive)
    parser_change_resolution.add_argument('-u', '--units',      help='The units for RESOLUTION', choices=['PixelsPerInch', 'PixelsPerCentimeter'])
    parser_change_resolution.add_argument('-i', '--input',      help='Input file')
    parser_change_resolution.add_argument('-o', '--output',     help='Output file')

    parser_pack_pdf = subparsers.add_parser('pack-pdf', 
        help='Pack input directory of TIFF files into an output PDF file. This action is currently disabled.')
    parser_pack_pdf.add_argument('-i', '--input',  help='Input directory')
    parser_pack_pdf.add_argument('-o', '--output', help='Output file')

    parser_expand_page = subparsers.add_parser('expand-page', 
        help='Expand the TIFF files in the the input directory to target WIDTH and HEIGHT in pixels')
    parser_expand_page.add_argument('-i', '--input',      help='Input file')
    parser_expand_page.add_argument('-o', '--output',     help='Output file')
    parser_expand_page.add_argument('-d', '--dimensions', help='Dimensions to set the page to', type=check_dims)

    return parser


def check_positive(value):
    ivalue = int(value)
    if ivalue < 0:
        raise argparse.ArgumentTypeError('{} is needs to be a positive integer'.format(ivalue))
    return ivalue


def check_dims(value):
    dims = value.split('x')
    if len(dims) != 2:
        raise argparse.ArgumentTypeError('{} needs to be of the form WIDTHxHEIGHT'.format(value))

    try:
        iwidth  = int(dims[0])
    except ValueError as ve:
        raise argparse.ArgumentTypeError('{} needs to be an integer'.format(iwidth))

    try:
        iheight = int(dims[1])
    except ValueError as ve:
        raise argparse.ArgumentTypeError('{} needs to be an integer'.format(iheight))

    if iwidth < 0:
        raise argparse.ArgumentTypeError('{} needs to be positive'.format(iwidth))
    if iheight < 0:
        raise argparse.ArgumentTypeError('{} needs to be positive'.format(iheight)) 

    return (iwidth, iheight)


"""
Build a command from a dictionary with a command string and a list of command arguments.
"""
def with_extension(extension, file_dict):
    def by_ext(extension, file):
        file_extension = os.path.splitext(file)[1]

        return extension == file_extension

    try:
        path = file_dict['path']
        files = file_dict['files']
    except KeyError as e:
        raise e

    return {'path': path, 'files': filter(lambda f: by_ext('tiff', f), files)}


def process_unpack_pdf(arg_dict):
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


"""
Repacking a PDF is not presently implemented. This can always be done after editing and OCRing with
Adobe Acrobat or a similar program.
"""
def process_pack_pdf(arg_dict):
    raise ValueError('Command not implemented')


# Output should be file or directory.
def process_change_resolution(arg_dict):
    try:
        input = arg_dict['input']
        resolution = arg_dict['resolution']
    except KeyError as e:
        raise e

    try:
        output = arg_dict['output']
    except KeyError as e:
        output = ''

    # We want to make multiple page operations if the input is a directory.
    if os.path.isdir(input):
        files = with_extension('.tiff', input)

        return multi_change_page_resolution(files, output, resolution)

    # If the input is one page only, we only need a single page operation.
    elif os.path.isfile(input):
        return change_page_resolution(input, output, resolution)

    else:
        raise ValueError('File or directory does not exist: {}'.format(input))

    

def process_expand_page(arg_dict):
    try:
        input      = arg_dict['input']
        dimensions = arg_dict['dimensions']
    except KeyError as e:
        raise e

    try:
        output = arg_dict['output']
    except KeyError as e:
        output = ''

    if os.path.isfile(input):
        return expand_page_with_fill(input, output, resolution)

    elif os.path.ispath(input):
        files = with_extension('.tiff', input)

        return multi_expand_page(files, output, resolution)

    else:
        raise ValueError('File or directory does not exist: {}'.format(input))


def process_command(command_dict):
    # Unpack the command and the arguments
    try:
        command = command_dict['command']
        args = command_dict['args']
    except KeyError as e:
        raise e

    # Unpack the command arguments
    if command == 'unpack-pdf':
        return process_unpack_pdf(args)

    elif command == 'pack-pdf':
        return process_pack_pdf(args)
    
    elif command == 'change-resolution':
        return process_change_resolution(args)

    elif command == 'expand-page':
        return process_expand_page(args)

    else:
        raise ValueError('Invalid command: {}'.format(command))


def main():
    parser = arg_processor()
    
    if len(sys.argv) < 2:
        parser.parse_args(['--help'])

    args = parser.parse_args(sys.argv[1:])
    command = sys.argv[1]

    action = process_command({'command': command, 'args': vars(args)})
    print(action)


if __name__ == 'main':
    main()
else:
    main()