import argparse
import sys
import execute_commands
import os.path


def arg_processor():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(help='subcommand help')

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
    parser_expand_page.add_argument('-d', '--dimensions', help='Dimensions to set the page to')

    return parser


def check_positive(value):
    ivalue = int(value)
    if ivalue < 0:
        raise argparse.ArgumentTypeError('{} is needs to be a positive integer'.format(ivalue))
    return ivalue

def get_args(argv):
    parser = arg_processor()

    args = parser.parse_args(argv)

    return args


def main():
        
    parser = arg_processor()

    args = parser.parse_args(sys.argv)
    print(args)


if __name__ == 'main':
    main()
else:
    get_args(sys.argv[1:])