import bookworm_main.bookworm_main as bookworm_main
import sys


def main():
    """
    Main is a wrapper for bookworm's main interface.
    """
    errno = bookworm_main.main()
    sys.exit(errno)


if __name__ == 'main':
    main()
else:
    main()
