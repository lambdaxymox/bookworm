import subprocess
import os.path
import command


def expand_file_with_fill(width, height, image_file):
    new_image_file = temp_filename(image_file)
    gravity        = '-gravity Center'
    background     = '-background white'
    extent         = '-extent {}x{}'.format(width, height)
    quoted_old_file = '\"{}\"'.format(image_file)
    quoted_new_file = '\"{}\"'.format(new_image_file)
    final_arg      = '{}[{}x{}]'.format(quoted_new_file, width, height)

    try:
        print('{} {} {} {} {}'.format('convert', extent, background, gravity, quoted_old_file, final_arg))
        subprocess.run(['convert', extent, background, gravity, quoted_old_file, final_arg])
    except subprocess.CalledProcessError as e:
        cleanup(new_image_file)
        raise e
    
    os.remove(image_file)
    os.rename(new_image_file, image_file)



def files_exist(files):
    # Check  that files actually exist
    for file in files:
        if not os.path.isfile(file):
            return False

    return True


def run_command(action):
    try:
        print(action.as_terminal_command())
        command.execute(action)
    except subprocess.CalledProcessError as e:
        raise e

def usage():
    return  'USAGE: python3 bookworm.py [-options] /path/to/image/file(s)'

def help():
    return 'Help not available'

def main():
    print(usage())


if __name__ == 'main':
    main()
else:
    main()
