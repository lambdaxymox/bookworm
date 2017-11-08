import bookworm.abstract as abstract
import bookworm.util     as util
import os.path
import os
import subprocess


class ExpandPageWithFill(abstract.Command):
    """
    Expand the side of a page by expanding the edges of the page with a fill
    color. This function only does this with the color white. This action does
    NOT resample the page at a different resolution.
    """
    def __init__(self, source_file, target_file, width, height):
        self.command = 'convert'
        self.extent_flag = '-extent' 
        self.extent = f'{width}x{height}'
        self.background_flag = '-background' 
        self.background = 'white'
        self.gravity_flag = '-gravity'
        self.gravity = 'Center'
        self.source_file = source_file
        self.target_file = target_file
        self.target_path = os.path.split(target_file)[0]
        self.width = width
        self.height = height

    def as_subprocess(self):
        quoted_source = f'./{self.source_file}'
        quoted_target = f'./{self.target_file}'
        final_arg = f'{quoted_target}[{self.width}x{self.height}]'

        return [
            self.command,
            self.extent_flag,
            self.extent,
            self.background_flag,
            self.background,
            self.gravity_flag,
            self.gravity,
            quoted_source,
            final_arg
        ]

    def as_terminal_command(self):
        quoted_source = util.quoted_string(f'./{self.source_file}')
        quoted_target = util.quoted_string(f'./{self.target_file}')
        final_arg = f'{quoted_target}[{self.width}x{self.height}]'
        
        return '{} {} {} {} {} {} {} {} {}'.format(
            self.command,
            self.extent_flag,
            self.extent,
            self.background_flag,
            self.background,
            self.gravity_flag,
            self.gravity,
            quoted_source,
            final_arg
        )


def make(width, height, source_file, target_file=''):
    """
    The ``make`` function is a factory method that constructs an 
    ``ExpandPageWIithFill`` action. It expands the side of a page by 
    expanding the edges of the page with a fill color. This function only does
    this with the color white.
    """
    if not target_file:
        new_target_file = util.temp_file_name(source_file)
        return ExpandPageWithFill(source_file, new_target_file, width, height)

    return ExpandPageWithFill(source_file, target_file, width, height)


def multi_expand_page(width, height, source_path, source_files, target):
    """
    Create multiple ExpandPageWithFill actions, one per page, in a single
    directory.
    """
    actions = {}
    for source_file in source_files:
        action = make(
            width, height, os.path.join(source_path, source_file), target
        )
        actions[source_file] = action

    return actions


def process_args(arg_dict):
    """
    The ``process_args`` factory method parses the command line arguments in
    ``arg_dict`` and uses them to construct a page command.
    """
    try:
        input = arg_dict['input']
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
        raise ValueError(
            f'Dimensions must be positive integers: Got {width}x{height}'
        )

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

        return multi_expand_page(
            width, 
            height,
            new_files_dict['path'],
            new_files_dict['files'], 
            output
        )

    else:
        raise FileNotFoundError(f'File or directory does not exist: {input}')


class Runner(abstract.Runner):

    def setup(command):
        """
        Prepare an action for execution by setting up folders and I/O.
        """
        if os.path.isfile(command.source_file):
            if not os.path.isdir(command.target_path):
                os.mkdir(command.target_path)
        else:
            raise FileNotFoundError(
                f'File does not exist: {command.source_file}'
            )

    def execute(command):
        print(command.as_terminal_command())
        subprocess.run(command.as_subprocess())

    def cleanup(command):
        return

