import bookworm.unpack_pdf        as unpack_pdf
import bookworm.expand_page       as expand_page
import bookworm.change_resolution as change_resolution
import bookworm.resample_page     as resample_page
import subprocess
import os


ALLOWED_COMMANDS = {
    'unpack-pdf': unpack_pdf,
    'change-resolution': change_resolution,
    'expand-page': expand_page,
    'resample-page': resample_page,
}


def load_module(module):
    return ALLOWED_COMMANDS[module]


def process_command(command_dict):
    """
    Unpack the command and the arguments.
    """
    try:
        command = command_dict['command']
        arg_dict = command_dict['args']
    except KeyError as e:
        raise e

    try:
        module = load_module(command)
    except:
        raise ValueError(f'Invalid command: {command}')

    try:
        action = module.process_args(arg_dict)
    except:
        raise ValueError(f'Invalid arguments. Got: {arg_dict}')

    return (action, module.Runner)


def run_command(actions):
    """
    Run a pdf or page action catching for runtime errors.
    """
    for action, runner in actions:
        try:
            runner.setup(action)
            runner.execute(action)
        except subprocess.CalledProcessError as e:
            runner.cleanup(action)
            raise e

