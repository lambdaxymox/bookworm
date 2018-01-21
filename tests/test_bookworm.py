import sys
import pytest
import bookworm_main.bookworm_main as bookworm_main


def test_bookworm_with_no_arguments():
    """
    With no arguments, the bookworm frontend should exit with an error code of
    2. This is standard practice with unix command line utilities that pass
    invalid arguments.
    """
    try:
        bookworm_main.main(['bookworm'])
    except SystemExit as e:
        assert e.code == 2
        
