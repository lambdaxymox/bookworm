import subprocess
import os.path
import command


def commit_action(action):
    os.remove(action.source)
    os.rename(action.target, action.source)


def handle_cleanup_file(target):
    try:
        os.remove(target)
    except OSError as e:
        # File does not exist, or it is a directory, so nothing needs to be done.
        return

def handle_cleanup_dir(target_dir):
    try:
        os.rmdir(target_dir)
    except OSError as e:
        # Directory does not exist, so nothing needs to be done.
        return


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
        handle_cleanup(action.target)
        raise e

    commit_action(action)


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
