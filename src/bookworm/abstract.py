import abc


class Command(abc.ABC):
    """
    The ``Command`` class defines the necessary functionality for constructing
    an executable pdf or page action. The abstract class is an interface for
    creating and storing the necessary functionality necessary to execute the
    action it embodies.
    """
    @abc.abstractmethod
    def as_terminal_command(self):
        return NotImplemented

    @abc.abstractmethod
    def as_subprocess(self):
        return NotImplemented

    def __str__(self):
        return self.as_terminal_command()


class Runner(abc.ABC):
    """
    The ``Runner`` class is an abstract class that defines the required
    methods necessary to successfully execute a ``Command``, and the handle
    cleanup after a success or failure. The exact details are left to the
    implementors of the abstract class. 
    """
    @classmethod
    @abc.abstractmethod
    def setup(command):
        """
        The ``setup`` method performs the necessary actions to setup
        execution of a ``Command``.
        """
        return NotImplemented

    @classmethod
    @abc.abstractmethod
    def execute(command):
        """
        The ``execute`` method executes a ``Command``.
        """
        return NotImplemented

    @classmethod
    @abc.abstractmethod
    def commit(command):
        """
        The commit method performs cleanup after a successful execution.
        """
        return NotImplemented

