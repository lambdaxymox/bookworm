import os.path

from bookworm.resolution import Resolution


def temp_file_name(file_name):

    def remove_leading_period(file_ext):
        if file_ext[0] == '.':
            return file_ext[1:]
        else:
            return file_ext


    file, ext = os.path.splitext(file_name)

    # If the file has no name, file and ext must be swapped
    # because os.path.splitext will place the file extension into file.
    if ext == '':
        ext = file
        file = ''

    return '{}.bookworm.{}'.format(file, remove_leading_period(ext))


def default_subdirectory():
    return '__bookworm__/'


def temp_directory(file_name):
    file_path, ext = os.path.splitext(file_name)
    new_path = os.path.dirname(file_path)

    return os.path.join(new_path, default_subdirectory())


def with_extension(extension, file_dict):
    """
    Get the collection of files in a directory with a given file extension.
    """
    def by_ext(extension, file):
        file_extension = os.path.splitext(file)[1]

        return file_extension == extension

    if extension[0] != '.':
        # Prepend a leading period.
        extension = '.' + extension

    try:
        path  = file_dict['path']
        files = file_dict['files']
    except KeyError as e:
        raise e

    return {'path': path, 'files': list(filter(lambda file: by_ext(extension, file), files))}


def files_exist(files):
    """
    Check that the files actually exist.
    """
    for file in files:
        if not os.path.isfile(file):
            return False

    return True


def make_resolution(resolution_val, unit_str):
    return Resolution.make_resolution(resolution_val, unit_str)


def quoted_string(string):
    """
    The function ``quoted_string`` determines whether a string begins and ends
    with quotes or not. If not, it closes the input ``string`` in quotes.
    """
    if string:
        new_string = string

        if string[0] != '\"':
            new_string = '\"' + new_string
    
        if string[len(string)-1] != '\"':
            new_string = new_string + '\"'

    else:
        new_string = "\"\""
    
    return new_string

