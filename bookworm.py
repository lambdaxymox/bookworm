import argparse
import sys
import execute_commands


def arg_processor():
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', '--unpack-pdf',        help='Unpack an input PDF file to the output directory')
    parser.add_argument('-r', '--change-resolution', help='Change the resolution of the TIFF files in the input'
                                                         +'directory to RESOLUTION in UNITS', type=int)
    parser.add_argument('-u', '--units',             help='The units for RESOLUTION', choices=['PixelsPerInch', 'PixelsPerCentimeter'])
    parser.add_argument('-e', '--expand',            help='Expand the TIFF files in the the input directory to target \n'
                                                         +'WIDTH and HEIGHT in pixels')
    parser.add_argument('-p', '--pack-pdf',          help='Pack input directory of TIFF files into an output PDF file')
    parser.add_argument(      '--test',              help='Run Bookworm\'s tests')
    parser.add_argument('-i', '--input',             help='Input file or directory')
    parser.add_argument('-o', '--output',            help='Output file or directory')

    return parser

#def is_valid_combination():

#def more_than_one_of(name_space):
#    vars = vars(name_space)
def get_args():
    parser = arg_processor()

    args = parser.parse_args(sys.argv)

    return args


def main():

    def more_than_one_of(name_space):
        
    parser = arg_processor()

    args = parser.parse_args()
    print(args)
    # Check for a valid combination of arguments
    #if valid_combination(args):


if __name__ == 'main':
    main()
else:
    get_args()