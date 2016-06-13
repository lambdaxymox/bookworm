import subprocess
import bookworm.command as command


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


def run_command(actions):
    """
    Run a terminal command, catching for runtime errors.
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

