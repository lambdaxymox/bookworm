import command
import os.path


"""
Expand the side of a page by expanding the edges of the page with a fill
color. This function only does this with the color white.
"""
class ExpandPageWithFill(command.PageCommand):
    def __init__(self, source, target, width, height):
        self.command    = 'convert'
        self.extent     = '-extent {}x{}'.format(width, height)
        self.background = '-background white'
        self.gravity    = '-gravity Center'
        self.source     = '\"{}\"'.format(source)
        self.target     = '\"{}\"'.format(target)
        self.width      = width
        self.height     = height

    def as_arg_list(self):
        return [self.command, self.extent, self.background, self.gravity, self.source, self.target]

    def as_terminal_command(self):
        final_arg = '{}[{}x{}]'.format(self.target, self.width, self.height)
        
        return \
            '{} {} {} {} {} {}' \
            .format(self.command, self.extent, self.background, self.gravity, self.source, final_arg)


"""
Expand the side of a page by expanding the edges of the page with a fill
color. This function only does this with the color white.
"""
def expand_page_with_fill(width, height, source, target=''):
    if not target:
        new_target = command.temp_file_name(source)
        return ExpandPageWithFill(source, new_target, width, height)

    return ExpandPageWithFill(source, target, width, height)


def multi_expand_page(width, height, sources, target):
    actions = {}

    for source in sources:
        action = expand_page_with_fill(source, width, height)
        actions[source] = action

    return actions


def process_expand_page(arg_dict):
    try:
        input      = arg_dict['input']
        dimensions = arg_dict['dimensions']
    except KeyError as e:
        raise e

    if os.path.isfile(input):
        try:
            output = arg_dict['output']
        except KeyError as e:
            # Use input as the target file.
            output = input


        return expand_page_with_fill(dimensions[0], dimensions[1], input, output)

    elif os.path.ispath(input):
        try:
            output = arg_dict['output']
        except KeyError as e:
            # Derive output directory from input directory
            output = os.path.join(input, '__bookworm__/')

        files = command.with_extension('.tiff', input)

        return multi_expand_page(resolution, files, output)

    else:
        raise ValueError('File or directory does not exist: {}'.format(input))
