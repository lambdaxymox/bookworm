import subprocess
import command


"""
Action cleanup handlers.
"""
def handle_cleanup_file(target_file):
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


def handle_cleanup(target):
    if os.path.exists(target):
        if os.path.isdir(target):
            handle_cleanup_dir(target)
        elif os.path.isfile(target):
            handle_cleanup_file(target)
        else:
            # Do nothing
            return
    else:
        # Do nothing
        return


def run_command(action):
    """
    Run a terminal command, catching for runtime errors.
    """
    try:
        print(action.as_terminal_command())
        execute(action)
    except subprocess.CalledProcessError as e:
        handle_cleanup(action.target)
        raise e

    action.commit()

def run_multi_page_commands(action_dict):
    for page in action_dict.keys():
        run_command(action_dict['page'])
