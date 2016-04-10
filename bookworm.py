import argparse
import sys
import execute_commands
import unpack_pdf
import pack_pdf
import expand_page
import change_resolution
import os.path

"""
The main pdf operations are:

1. Unpack a PDF.
2. Repack a PDF.
2. Pack a directory of images into a PDF.
3. Change image resolution.
4. Rescale image.
5. Expand image with fill.

"""

""" 
Generate an argument parser.
"""
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


def process_command(command_dict):
    # Unpack the command and the arguments
    try:
        command = command_dict['command']
        args = command_dict['args']
    except KeyError as e:
        raise e

    # Unpack the command arguments
    if command == 'unpack-pdf':
        return  unpack_pdf.process_args(args)

    elif command == 'pack-pdf':
        return pack_pdf.process_args(args)
    
    elif command == 'change-resolution':
        return change_resolution.process_args(args)

    elif command == 'expand-page':
        return expand_page.process_args(args)

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