import os.path


def temp_file_name(file_path):

    def remove_leading_period(file_ext):
        if file_ext[0] == '.':
            return file_ext[1:]
        else:
            return file_ext

    def split_on_leading_periods(file_name):
        count = 0
        for ch in file_name:
            if ch == '.':
                count += 1
            else:
                break

        return file_name[0:count-1], file_name[count-1:]


    prefix, file = os.path.split(file_path)
    file_name, file_ext = os.path.splitext(file)
    # If file_name  is empty, there are two possible scenarios: 
    #
    # (1) the file name contains leading periods;
    # (2) the file name is empty.
    #
    # In the case of (2) file_name and file_ext must be swapped because 
    # splitext() will place file extension into file_name. In the case of (1),
    # we need to apply another split to extract the leading periods to yield
    # a correct ultimate file name.
    if file_ext == '':
        file_name, file_ext = split_on_leading_periods(file_name)

    trimmed_ext = remove_leading_period(file_ext)
    new_file_name = f'{file_name}.bookworm.{trimmed_ext}'

    return os.path.join(prefix, new_file_name)


def default_subdirectory():
    return '__bookworm__/'


def temp_directory(file_path):
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
        try:
            if not os.path.isfile(file):
                return False
        except ValueError as e:
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

