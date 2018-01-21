import bookworm.execute_command    as execute_command
import bookworm.unpack_pdf         as unpack_pdf
import bookworm.expand_page        as expand_page
import bookworm.change_resolution  as change_resolution
import bookworm.detect_user        as detect_user
import bookworm.resample_page      as resample_page
import bookworm_main.arg_processor as arg_processor
import sys


def help_text(parser):
    """
    Return the help information for how to use the interface.
    """
    return parser.parse_args(['--help'])


def warning(*objs):
    """
    The function ``warning`` is a helper method for printing warnings.
    """
    print('WARNING: ', *objs, file=sys.stderr)


def main():
    """
    The main pdf operations are:

    1. Unpack a PDF.
    2. Change image resolution.
    3. Rescale image.
    4. Expand image with fill.
    """
    parser = arg_processor.arg_processor()

    if detect_user.is_admin():
        warning('You are currently running bookworm as superuser. '
                'You really should not run this program with elevated privileges.')

    if len(sys.argv) < 2:
        help_text(parser)

    args = parser.parse_args(sys.argv[1:])
    command = sys.argv[1]

    try:
        command_dict = dict(command=command, args=vars(args))
        action = execute_command.process_command(command_dict)
        execute_command.run_command([action])
    except Exception as e:
        print(e)
        sys.exit(1)
    except ValueError as e:
        print(e)
        sys.exit(2)

