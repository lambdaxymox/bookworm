import bookworm_main.bookworm_main as bookworm_main
import sys


def main():
    """
    The main pdf operations are:

    1. Unpack a PDF.
    2. Change image resolution.
    3. Rescale image.
    4. Expand image with fill.
    """
    errno = bookworm_main.main()
    sys.exit(errno)


if __name__ == 'main':
    main()
else:
    main()
