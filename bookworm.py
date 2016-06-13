import bookworm.execute_commands  as execute_commands
import bookworm.unpack_pdf        as unpack_pdf
import bookworm.expand_page       as expand_page
import bookworm.change_resolution as change_resolution
import bookworm.detect_user       as detect_user
import argparse
import os
import sys


"""
The main pdf operations are:

1. Unpack a PDF.
3. Change image resolution.
4. Rescale image.
5. Expand image with fill.

"""
def arg_processor():
    """ 
    Generate an argument parser for command line argument processing. The help menu is generated automatically.
    """
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(title='subcommands', description='valid subcommands', help='subcommand help')

    parser_unpack_pdf = subparsers.add_parser('unpack-pdf', 
        help='Unpack an input PDF file to the output directory')
    parser_unpack_pdf.add_argument('-i', '--input',  help='Input file')
    parser_unpack_pdf.add_argument('-o', '--output', help='Output directory', required=False)

    parser_change_resolution = subparsers.add_parser('change-resolution', 
        help='Change the resolution of the TIFF files in the input directory to RESOLUTION in UNITS')
    parser_change_resolution.add_argument('-r', '--resolution', help='The value for RESOLUTION', type=check_positive)
    parser_change_resolution.add_argument('-u', '--units',      help='The units for RESOLUTION', choices=['PixelsPerInch', 'PixelsPerCentimeter'])
    parser_change_resolution.add_argument('-i', '--input',      help='Input file')
    parser_change_resolution.add_argument('-o', '--output',     help='Output file')

    parser_expand_page = subparsers.add_parser('expand-page', 
        help='Expand the TIFF files in the the input directory to target WIDTH and HEIGHT in pixels')
    parser_expand_page.add_argument('-i', '--input',      help='Input file')
    parser_expand_page.add_argument('-o', '--output',     help='Output file')
    parser_expand_page.add_argument('-d', '--dimensions', help='Dimensions to set the page to', type=check_dims)

    return parser


def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError('{} needs to be a positive integer'.format(ivalue))
    return ivalue


def check_dims(value):
    dims = value.split('x')
    if len(dims) != 2:
        raise argparse.ArgumentTypeError('{} needs to be of the form WIDTHxHEIGHT'.format(value))

    try:
        iwidth  = int(dims[0])
    except ValueError as ve:
        raise argparse.ArgumentTypeError('{} needs to be an integer'.format(dims[0]))

    try:
        iheight = int(dims[1])
    except ValueError as ve:
        raise argparse.ArgumentTypeError('{} needs to be an integer'.format(dims[1]))

    if iwidth < 0:
        raise argparse.ArgumentTypeError('{} needs to be positive'.format(iwidth))
    if iheight < 0:
        raise argparse.ArgumentTypeError('{} needs to be positive'.format(iheight)) 

    return (iwidth, iheight)


def help_text(parser):
    return parser.parse_args(['--help'])

def warning(*objs):
    print('WARNING: ', *objs, file=sys.stderr)

def process_command(command_dict):
    """
    Unpack the command and the arguments
    """
    try:
        command  = command_dict['command']
        arg_dict = command_dict['args']
    except KeyError as e:
        raise e

    try:
        input = arg_dict['input']
    except KeyError as e:
        raise ValueError('Input file or directory not specified.')

    # Unpack the command arguments
    if command == 'unpack-pdf':
        return unpack_pdf.process_args(arg_dict)
    
    elif command == 'change-resolution':
        return change_resolution.process_args(arg_dict)

    elif command == 'expand-page':
        return expand_page.process_args(arg_dict)

    else:
        raise ValueError('Invalid command: {}'.format(command))


def main():
    parser = arg_processor()
    
    if detect_user.is_admin():
        warning('You are currently running as superuser. You really should not run this program with root privileges.')

    if len(sys.argv) < 2:
        help_text(parser)

    args    = parser.parse_args(sys.argv[1:])
    command = sys.argv[1]
    
    try:
        action = process_command({'command': command, 'args': vars(args)})
        execute_commands.run_command([action])
    except Exception as e:
        print(e)
        sys.exit(1)
    except ValueError as e:
        print(e)
        sys.exit(1)


if __name__ == 'main':
    main()
else:
    main()
