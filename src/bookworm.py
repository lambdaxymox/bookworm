import bookworm.execute_commands  as execute_commands
import bookworm.unpack_pdf        as unpack_pdf
import bookworm.expand_page       as expand_page
import bookworm.change_resolution as change_resolution
import bookworm.detect_user       as detect_user
import bookworm.resample_page     as resample_page
import argparse
import sys


def arg_processor():
    """ 
    Generate an argument parser for command line argument processing.
    The help menu is generated automatically.
    """
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(
        title='subcommands', 
        description='valid subcommands', 
        help='subcommand help'
    )

    # Subparser for the unpack-pdf command.
    parser_unpack_pdf = subparsers.add_parser(
        'unpack-pdf', 
        help='Unpack an input PDF file to the output directory'
    )
    parser_unpack_pdf.add_argument(
        '-i', '--input',
        help='Input file'
    )
    parser_unpack_pdf.add_argument(
        '-o', '--output',
        help='Output directory', required=False
    )

    # Subparser for the change-resolution command.
    parser_change_resolution = subparsers.add_parser(
        'change-resolution', 
        help='Change the resolution of the TIFF files in the input directory to RESOLUTION in UNITS'
    )
    parser_change_resolution.add_argument(
        '-r', '--resolution', 
        help='The value for RESOLUTION', 
        type=check_positive
    )
    parser_change_resolution.add_argument(
        '-u', '--units',
        help='The units for RESOLUTION',
        choices=['PixelsPerInch', 'PixelsPerCentimeter']
    )
    parser_change_resolution.add_argument(
        '-i', '--input',
        help='Input file'
    )
    parser_change_resolution.add_argument(
        '-o', '--output',
        help='Output file'
    )

    # Subparser for the expand-page command.
    parser_expand_page = subparsers.add_parser(
        'expand-page', 
        help='Expand the TIFF files in the the input directory to target WIDTH and HEIGHT in pixels'
    )
    parser_expand_page.add_argument(
        '-i', '--input',
        help='Input file'
    )
    parser_expand_page.add_argument(
        '-o', '--output',
        help='Output file'
    )
    parser_expand_page.add_argument(
        '-d', '--dimensions',
        help='Dimensions to set the page to',
        type=check_dims
    )

    # Subparser for the resample-page command.
    parser_resample_page = subparsers.add_parser(
        'resample-page',
        help='Rescale a page by changing its resolution and resampling the image'
    )
    parser_resample_page.add_argument(
        '-i', '--input',
        help='Input file'
    )
    parser_resample_page.add_argument(
        '-o', '--output',
        help='Output file'
    )
    parser_resample_page.add_argument(
        '-r', '--resolution', 
        help='The value for RESOLUTION', 
        type=check_positive
    )
    parser_resample_page.add_argument(
        '-u', '--units',
        help='The units for RESOLUTION',
        choices=['PixelsPerInch', 'PixelsPerCentimeter']
    )

    return parser


def check_positive(value):
    """
    Determine whether the input value is a positive integer.
    """
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(
            f'{ivalue} needs to be a positive integer'
        )

    return ivalue


def check_dims(value):
    """
    Check that the input dimensions for a page are valid.
    """
    dims = value.split('x')
    if len(dims) != 2:
        raise argparse.ArgumentTypeError(
            f'{value} needs to be of the form WIDTHxHEIGHT'
        )

    try:
        iwidth  = int(dims[0])
    except ValueError as ve:
        raise argparse.ArgumentTypeError(
            f'{dims[0]} needs to be an integer'
        )

    try:
        iheight = int(dims[1])
    except ValueError as ve:
        raise argparse.ArgumentTypeError(
            f'{dims[1]} needs to be an integer'
        )

    if iwidth < 0:
        raise argparse.ArgumentTypeError(
            f'{iwidth} needs to be positive'
        )

    if iheight < 0:
        raise argparse.ArgumentTypeError(
            f'{iheight} needs to be positive'
        ) 

    return (iwidth, iheight)


def help_text(parser):
    """
    Return the help information for how to use the interface.
    """
    return parser.parse_args(['--help'])


def warning(*objs):
    """
    A helper method for printing warnings.
    """
    print('WARNING: ', *objs, file=sys.stderr)


def load_module(module):
    ALLOWED_COMMANDS = {
        'unpack-pdf': unpack_pdf,
        'change-resolution': change_resolution,
        'expand-page': expand_page,
        'resample-page': resample_page,
    }

    return ALLOWED_COMMANDS[module]


def process_command(command_dict):
    """
    Unpack the command and the arguments.
    """
    try:
        command = command_dict['command']
        arg_dict = command_dict['args']
    except KeyError as e:
        raise e

    try:
        module = load_module(command)
    except:
        raise ValueError(f'Invalid command: {command}')

    try:
        action = module.process_args(arg_dict)
    except:
        raise ValueError(f'Invalid arguments. Got: {arg_dict}')

    return action


def main():
    """
    The main pdf operations are:

    1. Unpack a PDF.
    2. Change image resolution.
    3. Rescale image.
    4. Expand image with fill.
    """
    if detect_user.is_admin():
        warning('You are currently running as superuser. '
                'You really should not run this program with elevated privileges.')

    if len(sys.argv) < 2:
        help_text(parser)

    parser = arg_processor()
    args = parser.parse_args(sys.argv[1:])
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

