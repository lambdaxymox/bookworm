import os.path
import enum


class Resolution:
    def __init__(self, resolution, units):
        self.resolution = resolution
        self.units      = units

    def __repr__(self):
        return 'Resolution({}, {})'.format(self.resolution, self, units)

    def __str__(self):
        return '{} {}'.format(self.resolution, self.units)


class TerminalCommand:
    def __init__(self, **kwargs):
        pass

    def as_arg_list(self):
        raise NotImplemented

    def as_terminal_command(self):
        raise NotImplemented

    def as_python_subprocess(self):
        raise NotImplemented

    def commit(self):
        raise NotImplemented

    def __str__(self):
        return self.as_terminal_command()

    def __repr__(self):
        return 'Command({})'.format(self.as_python_subprocess())


class PageCommand(TerminalCommand):
    def commit(self):
        os.remove(action.source)
        os.rename(action.target, action.source)


class PDFCommand(TerminalCommand):

    def commit(self):
        pass

    def image_dir(self):
        raise NotImplemented



def temp_file_name(file_name):
    
    def remove_leading_period(file_ext):
        if file_ext[0] == '.':
            return file_ext[1:]
        else:
            return file_ext


    file, ext = os.path.splitext(file_name)

    return '{}.bookworm.{}'.format(file, remove_leading_period(ext))


def temp_directory(file_name):
    file_path, ext = os.path.splitext(file_name)

    new_path = os.path.dirname(file_path)

    return os.path.join(new_path, '__bookworm__/')


"""
Build a command from a dictionary with a command string and a list of command arguments.
"""
def with_extension(extension, file_dict):
    def by_ext(extension, file):
        file_extension = os.path.splitext(file)[1]

        return file_extension == extension

    try:
        path = file_dict['path']
        files = file_dict['files']
    except KeyError as e:
        raise e

    return {'path': path, 'files': list(filter(lambda f: by_ext(extension, f), files))}
