import getopt
import sys
import execute_commands


def usage():
    return  'USAGE: python3 bookworm.py [-options] /path/to/image/file(s)'

def help():
    return 'Help not available'

def main():
    args = sys.argv[1:]
    print(args)

if __name__ == 'main':
    main()
else:
    main()
