import bookworm.command as command
import bookworm.util    as util
import os.path


class ExpandPageWithFill(command.Command):
    """
    Expand the side of a page by expanding the edges of the page with a fill
    color. This function only does this with the color white.
    """
    def __init__(self, source, target, width, height):
        self.command = 'convert'
        self.extent = '-extent {}x{}'.format(width, height)
        self.background = '-background white'
        self.gravity = '-gravity Center'
        self.source = source
        self.target = target
        self.width = width
        self.height = height

    def as_python_subprocess(self):
        quoted_source = util.quoted_string(self.source)
        quoted_target = util.quoted_string(self.target)

        return [
            self.command,
            self.extent,
            self.background,
            self.gravity,
            quoted_source,
            quoted_target
        ]

    def as_terminal_command(self):
        quoted_source = util.quoted_string(self.source)
        quoted_target = util.quoted_string(self.target)
        final_arg = '{}[{}x{}]'.format(quoted_target, self.width, self.height)
        
        return \
            '{} {} {} {} {} {}' \
            .format(self.command, self.extent, self.background, self.gravity, quoted_source, final_arg)


def make(width, height, source, target=''):
    """
    The ``make`` function is a factory method that constructs an 
    ``ExpandPageWIithFill`` action. It expands the side of a page by 
    expanding the edges of the page with a fill color. This function only does
    this with the color white.
    """
    if not target:
        new_target = util.temp_file_name(source)
        return ExpandPageWithFill(source, new_target, width, height)

    return ExpandPageWithFill(source, target, width, height)


def multi_expand_page(width, height, source_path, source_files, target):
    """
    Create multiple ExpandPageWithFill actions, one per page, in a single
    directory.
    """
    actions = {}
    for source in source_files:
        action = make(width, height, os.path.join(source_path, source), target)
        actions[source] = action

    return actions


def process_args(arg_dict):
    """
    The ``process_args`` factory method parses the command line arguments in
    ``arg_dict`` and uses them to construct a page command.
    """
    try:
        input      = arg_dict['input']
        dimensions = arg_dict['dimensions']
    except KeyError as e:
        raise e

    try: 
        width  = dimensions[0]
        height = dimensions[1]
    except TypeError as e:
        raise e
    except ValueError as e:
        raise e

    if width <= 0 or height <= 0:
        raise ValueError('Dimensions must be positive integers: Got {}x{}'.format(width, height))

    if os.path.isfile(input):
        try:
            output = arg_dict['output']
        except KeyError as e:
            # Use input as the target file.
            output = input


        return make(width, height, input, output)

    elif os.path.isdir(input):
        try:
            output = arg_dict['output']
        except KeyError as e:
            # Derive output directory from input directory
            output = os.path.join(input, util.default_subdirectory())

        files_dict = {'path': input, 'files': os.listdir(input)}

        new_files_dict = util.with_extension('.tiff', files_dict)

        return multi_expand_page(width, height, new_files_dict['path'], new_files_dict['files'], output)

    else:
        raise FileNotFoundError('File or directory does not exist: {}'.format(input))

