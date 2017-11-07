import subprocess


class Command:

    def __init__(self, **kwargs):
        pass

    def as_arg_list(self):
        return NotImplemented

    def as_terminal_command(self):
        return NotImplemented

    def as_python_subprocess(self):
        return NotImplemented

    def __str__(self):
        return self.as_terminal_command()

    def __repr__(self):
        return f'Command({self.as_python_subprocess()})'


#def setup(self):
#    return NotImplemented
#
#def run(self):
#    """
#    Execute a command in the shell.
#    """
#    subprocess.run(self.as_python_subprocess())
#
#def commit(self):
#    """
#    Commit and clean up after a successful execution.
#    """
#    return NotImplemented

