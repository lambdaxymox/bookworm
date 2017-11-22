import os.path


def temp_file_name(file_path):

    def remove_leading_period(file_ext):
        if file_ext[0] == '.':
            return file_ext[1:]
        else:
            return file_ext


    prefix, file = os.path.split(file_path)
    file_name, file_ext = os.path.splitext(file)

    # If the file has no name, file and ext must be swapped
    # because os.path.splitext will place the file extension into file.
    if file_ext == '':
        file_ext = file_name
        file_name = ''

    trimmed_ext = remove_leading_period(file_ext)
    temp_file = f'{file_name}.bookworm.{trimmed_ext}'

    return os.path.join(prefix, temp_file)


def default_subdirectory():
    return '__bookworm__/'


def temp_directory(file_path):
    #file_path, _ = os.path.split(file_name_or_file_path)
    return os.path.join(file_path, default_subdirectory())


def with_extension(extension, file_dict):
    """
    Get the collection of files in a directory with a given file extension.
    """
    def by_ext(extension, file):
        file_extension = os.path.splitext(file)[1]

        return file_extension == extension


    if extension[0] != '.':
        # We are missing the leading period.
        extension = '.' + extension

    try:
        path  = file_dict['path']
        files = file_dict['files']
    except KeyError as e:
        raise e

    return dict(
        path = path, 
        files = list(filter(lambda file: by_ext(extension, file), files))
    )


def files_exist(files):
    """
    Check that the files actually exist.
    """
    for file in files:
        if not os.path.isfile(file):
            return False

    return True


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

