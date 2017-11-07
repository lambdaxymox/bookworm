import subprocess
import os


# Action cleanup handlers.
def handle_cleanup_file(target_file):
    """
    Handle the cleanup of a file after an error occurs.
    """
    try:
        os.remove(target_file)
    except OSError as e:
        # File does not exist, or it is a directory, so nothing needs to be done.
        return


def handle_cleanup_dir(target_dir):
    """
    Handle cleaning up a directory after an error occurs.
    """
    try:
        os.rmdir(target_dir)
    except OSError as e:
        # Directory does not exist, so nothing needs to be done.
        return


def handle_cleanup(target):
    """
    Handle cleaning up an action that fails.
    """
    if os.path.exists(target):
        if os.path.isdir(target):
            handle_cleanup_dir(target)
        elif os.path.isfile(target):
            handle_cleanup_file(target)
        else:
            return
    else:
        return


def run_command(actions):
    """
    Run a pdf or page action catching for runtime errors.
    """
    try:
        for action in actions:
            print(action.as_terminal_command())
            action.setup()
            action.run()
            action.commit()
    except subprocess.CalledProcessError as e:
        handle_cleanup(action.target)
        raise e

