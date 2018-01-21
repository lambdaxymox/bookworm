import argparse


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

